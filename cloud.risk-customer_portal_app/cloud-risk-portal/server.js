const express = require('express');
const cors = require('cors');
const neo4j = require('neo4j-driver');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config({ path: '.env' });

var https = require('https');
var http = require('http');
var fs = require('fs');

const app = express();
const port = process.env.PORT || 8184;

var options = {
    key: fs.readFileSync('/app/certs/server.key'),
    cert: fs.readFileSync('/app/certs/server.cert')
  };

const isProd = process.env.IS_PROD === "true";

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
        'https://simulation.localhost',
        'https://api.localhost',
        'https://simulation.cloud.risk.insureyourtech.cloud/',
        'https://api.cloud.risk.insureyourtech.cloud/',
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
    const envVars = {
        apiBaseUrl: process.env.IS_PROD === "true" ? process.env.PROD_API_BASE_URL : process.env.DEV_API_BASE_URL,
        isSSLBypassed: process.env.SSL_BYPASS === "true" ? false : true,
        isDevelopment: process.env.IS_PROD !== "true" ? true : false
    };
    // Serve the chart.js library
    app.use(express.static(path.join(__dirname, 'node_modules', 'chart.js', 'dist')));
    
    // Read the HTML file
    let html = fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8');
    
    // Insert the environment variables as a global object
    const envScript = `<script>window.ENV = ${JSON.stringify(envVars)};</script>`;
    
    // Insert the script just after the <head> tag
    html = html.replace('<head>', '<head>' + envScript);
    
    res.send(html);
});

// API Routes
const apiRouter = express.Router();


apiRouter.get('/api/get/env', async (req, res) => {
    try {
        const apiBaseUrl = process.env.IS_PROD === "true" ? process.env.PROD_API_BASE_URL : process.env.DEV_API_BASE_URL;
        res.status(200).json({ apiBaseUrl: apiBaseUrl });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
// Cloud Risk Data API
apiRouter.get('/cloud-services-risk-ratings/risk-ratings-freemium/freemium/fetch/service/service_name/:serviceName/global_or_by_regions/:regionType', async (req, res) => {
    try {
        const { serviceName, regionType } = req.params;
        // Implement your risk data fetching logic here
        // This would replace the Python fetch_cloud_risk_data function
        const riskData = await fetchCloudRiskData(serviceName, regionType);
        res.status(200).json(riskData);
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
        res.status(200).json(outageData);
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
//app.listen(port, () => {
//    console.log(`Server running on port ${port}`);
//});
// Start server
if (isProd) {
    https.createServer(options, app).listen(port);
} else if (process.env.SSL_ENABLED === "true") {
    https.createServer(options, app).listen(port);
} else {
    http.createServer(app).listen(port);
}