const express = require('express');
const cors = require('cors');
const neo4j = require('neo4j-driver');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config();

var https = require('https');
var http = require('http');
var fs = require('fs');

const app = express();
const port = process.env.PORT || 8184;

var options = {
    key: fs.readFileSync('./certs/key.pem'),
    cert: fs.readFileSync('./certs/cert.pem')
  };
  
http.createServer(app).listen(port);
https.createServer(options, app).listen(443);

// Middleware
app.use(express.json());
app.use(express.static('public'));
app.use(cors({
    origin: [
        'http://localhost:8184',
        'http://localhost:17474',
        'bolt://localhost:17687',
        'bolt://host.docker.internal:17687',
        'http://host.docker.internal:17474',
        'https://customerportal.cloudriskgraph.insureyourtech.cloud',
        'http://cloudriskgraph.insureyourtech.cloud:17474',
        'https://cloudriskgraph.insureyourtech.cloud:17474'
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    exposedHeaders: ['Access-Control-Allow-Origin'],
    credentials: true
}));

// Neo4j connection
const initNeo4jConnection = async () => {
    const uri = process.env.NEO4J_CLIENT_URI || 'bolt://host.docker.internal:17687';
    const user = process.env.NEO4J_USERNAME || 'neo4j';
    const password = process.env.NEO4J_PASSWORD || 'password';
    
    try {
        const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
        await driver.verifyConnectivity();
        return driver;
    } catch (error) {
        console.error('Failed to connect to Neo4j:', error);
        return null;
    }
};

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API Routes
const apiRouter = express.Router();

// Cloud Risk Data API
apiRouter.get('/cloud-services-risk-ratings/risk-ratings-freemium/freemium/fetch/service/service_name/:serviceName/global_or_by_regions/:regionType', async (req, res) => {
    try {
        const { serviceName, regionType } = req.params;
        // Implement your risk data fetching logic here
        // This would replace the Python fetch_cloud_risk_data function
        const riskData = await fetchCloudRiskData(serviceName, regionType);
        res.json(riskData);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Outage Data API
apiRouter.get('/cloud-services-risk-ratings/risk-ratings-freemium/freemium/outages/service/:service', async (req, res) => {
    try {
        const { service } = req.params;
        // Implement your outage data fetching logic here
        // This would replace the Python fetch_outage_data function
        const outageData = await fetchOutageData(service);
        if (!outageData) {
            return res.status(404).json({ message: `Outage not found in database for ${service}` });
        }
        res.json(outageData);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Neo4j Operations
apiRouter.post('/graph/insert', async (req, res) => {
    const { nodeType, properties } = req.body;
    try {
        const driver = await initNeo4jConnection();
        if (!driver) {
            return res.status(500).json({ error: 'Neo4j connection failed' });
        }
        
        const result = await insertRecord(driver, nodeType, properties);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.use('/api', apiRouter);

// Helper Functions
const sanitizeCypherIdentifier = (text) => {
    let sanitized = text.replace(/[^a-zA-Z0-9_]/g, '_');
    if (/^\d/.test(sanitized)) {
        sanitized = 'n' + sanitized;
    }
    return sanitized;
};

const insertRecord = async (driver, nodeType, properties) => {
    const session = driver.session();
    try {
        const query = `CREATE (n:${nodeType} $properties) RETURN n`;
        const result = await session.run(query, { properties });
        return result.records[0].get('n');
    } finally {
        await session.close();
    }
};

// Data fetching functions
const fetchCloudRiskData = async (serviceName, regionType) => {
    // Implement your cloud risk data fetching logic here
    // This could be from a database, external API, etc.
};

const fetchOutageData = async (service) => {
    // Implement your outage data fetching logic here
    // This could be from a database, external API, etc.
};

// Start server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});