const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');

// Load environment variables
dotenv.config({ path: '.env' });

var https = require('https');
var http = require('http');
var fs = require('fs');

var options = {
  key: fs.readFileSync('/app/certs/server8183.key'),
  cert: fs.readFileSync('/app/certs/server8183.cert')
};

// Variables to start the server
const PORT = process.env.PORT || 8183;
const DB_HOST = process.env.DB_HOST || 'postgres-db'; // localhost
const DB_PORT = process.env.DB_PORT || 5432;
const DB_USER = process.env.DB_USER || 'dbusername';
const DB_PASSWORD = process.env.DB_PASSWORD || 'password';
const DB_NAME = process.env.DB_NAME || 'cloud_service_risk_ratings';
const DB_NAME_PORTAL = process.env.DB_NAME_PORTAL || 'cloud_risk_portal';
const IS_PROD = process.env.IS_PROD === "true";

const riskRatingsRouter = require('./routes/CloudRiskRatings');
const freemiumRiskRatingsRouter = require('./routes/FreemiumCloudRiskRatings');
const servicesAppRouter = require('./routes/ServicesApp');

const app = express();

app.use(express.json());
app.use(cors({
  origin: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: false,
  exposedHeaders: ['Access-Control-Allow-Origin']
}));

// API Routes
app.use('/cloud-services-risk-ratings/risk-ratings-premium', riskRatingsRouter);
app.use('/cloud-services-risk-ratings/risk-ratings-freemium', freemiumRiskRatingsRouter);
app.use('/cloud-services-risk-ratings/services-app', servicesAppRouter);

//app.listen(PORT, function () {
//console.log(`Server is running on http://localhost:${PORT}`);
//});

// Start server
if (IS_PROD) {
  https.createServer(options, app).listen(PORT);
} else if (process.env.SSL_ENABLED === "true") {
  https.createServer(options, app).listen(PORT);
} else {
  http.createServer(app).listen(PORT);
}
