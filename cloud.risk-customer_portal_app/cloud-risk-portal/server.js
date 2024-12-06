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
    origin: function(origin, callback) {
        // Allow requests with no origin (like mobile apps or curl requests)
        if (!origin) return callback(null, true);
        
        const allowedOrigins = [
            'http://localhost:8184',
            'http://localhost:17474',
            'https://localhost:8184',
            'https://localhost:17474',
            'bolt://localhost:17687',
            'bolt://host.docker.internal:17687',
            'http://host.docker.internal:17474',
            'https://host.docker.internal:17474',
            'https://simulation.localhost',
            'https://api.localhost',
            'https://simulation.cloud.risk.insureyourtech.cloud',
            'https://api.cloud.risk.insureyourtech.cloud',
            'http://cloudriskgraph.insureyourtech.cloud:17474',
            'https://cloudriskgraph.insureyourtech.cloud:17474'
        ];
        
        if (allowedOrigins.indexOf(origin) !== -1 || origin.match(/^https?:\/\/localhost(:\d+)?$/)) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin', 'Origin', 'Accept', 'X-Requested-With'],
    exposedHeaders: ['Access-Control-Allow-Origin'],
    credentials: true,
    preflightContinue: true,
    optionsSuccessStatus: 204
}));

// Add CORS preflight handler
app.options('*', cors());

// Add headers middleware
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', req.headers.origin);
    res.header('Access-Control-Allow-Credentials', true);
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization, Access-Control-Allow-Origin');
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
    let html = fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8');
    
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
