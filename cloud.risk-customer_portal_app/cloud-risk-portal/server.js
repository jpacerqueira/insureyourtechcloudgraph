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
    key: fs.readFileSync('/app/certs/server8184.key'),
    cert: fs.readFileSync('/app/certs/server8184.cert')
  };

const isProd = process.env.IS_PROD === "true";

// Middleware
app.use(express.json());
app.use(express.static('public'));
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: false
}));

// Simplified headers middleware
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    next();
});

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

function generateCypherQuery(data) {
    const { companyName, projectName, services, metrics } = data;
    let cypher = '';

    // Sanitize company name for Cypher
    const companyId = companyName.replace(/[^a-zA-Z0-9]/g, '_');

    // Create customer node with all metrics
    cypher += `
CREATE (cust_${companyId}:CUSTOMER_NAME {
    name: '${companyName}',
    project_name: '${projectName}',
    median_sla_usage_percentage: '${metrics.customerMedian.slaUsage}%',
    median_sla_deviation_risk: '${metrics.customerMedian.slaDeviation}',
    median_traffic_coefficient: '${metrics.customerMedian.trafficCoef}%',
    median_usage_risk: '${metrics.customerMedian.usageRisk}',
    median_service_sla: '${metrics.customerMedian.serviceSla}%',
    median_annual_downtime: '${metrics.customerMedian.annualDowntime}',
    submission_date: '${new Date().toISOString()}'
})
`;

    // Add vendor and service nodes with complete metrics
    services.forEach(service => {
        const serviceId = service.name.replace(/[^a-zA-Z0-9]/g, '_');
        const vendorId = service.vendor.replace(/[^a-zA-Z0-9]/g, '_');

        cypher += `
CREATE (${serviceId}:TECHNOLOGY_SERVICE {
    name: '${service.name}',
    region: '${service.region}',
    monthly_cost: ${service.monthlyCost},
    sla_usage: '${service.metrics.slaUsage}%',
    sla_deviation_risk: '${service.metrics.slaDeviation}',
    traffic_coefficient: '${service.metrics.trafficCoef}%',
    usage_risk: '${service.metrics.usageRisk}',
    annual_downtime_minutes: '${service.metrics.annualDowntime}',
    service_sla_tier1: '${service.metrics.serviceSla}%',
    service_credit_back_tier1: '${service.metrics.creditBack}%'
})

CREATE (${vendorId}:TECHNOLOGY_PROVIDER {
    name: '${service.vendor}',
    vendor_median_sla_usage_percentage: '${metrics.vendorMedians[service.vendor].slaUsage}%',
    vendor_median_sla_deviation_risk: '${metrics.vendorMedians[service.vendor].slaDeviation}',
    vendor_median_traffic_coefficient: '${metrics.vendorMedians[service.vendor].trafficCoef}%',
    vendor_median_usage_risk: '${metrics.vendorMedians[service.vendor].usageRisk}',
    vendor_median_service_sla: '${metrics.vendorMedians[service.vendor].serviceSla}%',
    vendor_median_annual_downtime: '${metrics.vendorMedians[service.vendor].annualDowntime}'
})

CREATE (cust_${companyId})-[:CUSTOMER_USES_SERVICE {
    monthly_cost: ${service.monthlyCost},
    region: '${service.region}'
}]->(${serviceId})

CREATE (${vendorId})-[:CONNECTED_RISK {
    sla_usage: '${service.metrics.slaUsage}%',
    sla_deviation_risk: '${service.metrics.slaDeviation}',
    traffic_coefficient: '${service.metrics.trafficCoef}%',
    usage_risk: '${service.metrics.usageRisk}'
}]->(${serviceId})
`;
    });

    return cypher;
}

// Middleware to handle sessions
const session = require('express-session');
app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: isProd }
}));

// Function to delete previous Neo4j data
async function deletePreviousNeo4jData(sessionId) {
    const driver = await initNeo4jConnection();
    if (driver) {
        const session = driver.session();
        try {
            const deleteQuery = `
                MATCH (c:CUSTOMER_NAME {session_id: '${sessionId}'})-[r:CUSTOMER_USES_SERVICE]->(s:TECHNOLOGY_SERVICE)
                DETACH DELETE c, r, s
            `;
            await session.run(deleteQuery);
            console.log('Previous Neo4j data deleted successfully');
        } catch (error) {
            console.error('Error deleting previous Neo4j data:', error);
        } finally {
            await session.close();
        }
    }
}

// Update saveNeo4jQuery function to include session ID
function saveNeo4jQuery(data, sessionId) {
    const outputDir = path.join(__dirname, 'neo4j_customer_submission');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `Cloud.Risk.graph_${data.companyName.replace(/[^a-zA-Z0-9]/g, '_')}_${timestamp}.cypher`;
    const fullPath = path.join(outputDir, filename);

    // Create directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    // Generate Cypher query
    let cypher = generateCypherQuery(data);

    // Add session ID to customer node
    cypher = cypher.replace('CREATE (cust_', `CREATE (cust_${sessionId}_`);
    cypher = cypher.replace('CREATE (cust_', `CREATE (cust_${sessionId}_`);

    // Write to file
    fs.writeFileSync(fullPath, cypher);
    return fullPath;
}

// Update API endpoint to handle Neo4j file generation
app.post('/customer-portal/api/save-neo4j-query', async (req, res) => {
    const sessionId = req.sessionID;
    try {
        // Delete previous data
        await deletePreviousNeo4jData(sessionId);

        // Save new data
        const filePath = saveNeo4jQuery(req.body, sessionId);

        // Execute the new query
        const driver = await initNeo4jConnection();
        if (driver) {
            const cypher = generateCypherQuery(req.body);
            const session = driver.session();
            try {
                await session.run(cypher);
                console.log('Neo4j query executed successfully');
            } catch (error) {
                console.error('Error executing Neo4j query:', error);
            } finally {
                await session.close();
            }
        }

        res.json({ 
            success: true, 
            filePath,
            message: 'Data saved successfully' 
        });
    } catch (error) {
        console.error('Error saving Neo4j query:', error);
        res.status(500).json({ 
            error: error.message,
            details: 'Error saving or executing Neo4j query'
        });
    }
});

// API Routes
const apiRouter = express.Router();

// Routes
app.get('/simulation/', (req, res) => {
    const envVars = {
        apiBaseUrl: process.env.IS_PROD === "true" ? process.env.PROD_API_BASE_URL : process.env.DEV_API_BASE_URL,
        isSSLBypassed: process.env.SSL_BYPASS === "true" ? false : true,
        isDevelopment: process.env.IS_PROD !== "true" ? true : false
    };
    // Serve the chart.js library
    app.use(express.static(path.join(__dirname, 'node_modules', 'chart.js', 'dist')));
    
    // Read the HTML file
    let html = fs.readFileSync(path.join(__dirname, 'public', 'simulation-index.html'), 'utf8');
    
    // Insert the environment variables as a global object
    const envScript = `<script>window.ENV = ${JSON.stringify(envVars)};</script>`;
    
    // Insert the script just after the <head> tag
    html = html.replace('<head>', '<head>' + envScript);
    
    res.send(html);
});

// Routes
app.get('/customer-portal/', (req, res) => {
    const envVars = {
        apiBaseUrl: process.env.IS_PROD === "true" ? process.env.PROD_API_BASE_URL : process.env.DEV_API_BASE_URL,
        isSSLBypassed: process.env.SSL_BYPASS === "true" ? false : true,
        isDevelopment: process.env.IS_PROD !== "true" ? true : false
    };
    // Serve the chart.js library
    app.use(express.static(path.join(__dirname, 'node_modules', 'chart.js', 'dist')));
    
    // Read the HTML file
    let html = fs.readFileSync(path.join(__dirname, 'public', 'customer-portal-index.html'), 'utf8');
    
    // Insert the environment variables as a global object
    const envScript = `<script>window.ENV = ${JSON.stringify(envVars)};</script>`;
    
    // Insert the script just after the <head> tag
    html = html.replace('<head>', '<head>' + envScript);
    
    res.send(html);
});


apiRouter.get('/simulation/customer-portal/api/get/env', async (req, res) => {
    try {
        const apiBaseUrl = process.env.IS_PROD === "true" ? process.env.PROD_API_BASE_URL : process.env.DEV_API_BASE_URL;
        res.status(200).json({ apiBaseUrl: apiBaseUrl });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
// Cloud Risk Data API

// Start server
if (isProd) {
    https.createServer(options, app).listen(port);
} else if (process.env.SSL_ENABLED === "true") {
    https.createServer(options, app).listen(port);
} else {
    http.createServer(app).listen(port);
}
