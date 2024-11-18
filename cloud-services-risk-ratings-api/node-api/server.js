const express = require('express');
const dotenv = require('dotenv');
// Load environment variables
dotenv.config({ path: '.env' });

const riskRatingsRouter = require('./routes/CloudRiskRatings');
const freemiumRiskRatingsRouter = require('./routes/FreemiumCloudRiskRatings');

const app = express();
app.use(express.json());

// API Routes
app.use('/cloud-services-risk-ratings/risk-ratings', riskRatingsRouter);
app.use('/cloud-services-risk-ratings/risk-ratings-freemium', freemiumRiskRatingsRouter);

// Start the server
const PORT = process.env.PORT || 8000;
const DB_HOST = process.env.DB_HOST || 'postgres-db'; // localhost
const DB_PORT = process.env.DB_PORT || 5432;
const DB_USER = process.env.DB_USER || 'dbusername';
const DB_PASSWORD = process.env.DB_PASSWORD || 'password';
const DB_NAME = process.env.DB_NAME || 'cloud_service_risk_ratings';

app.listen(PORT, function () {
    console.log(`Server is running on http://localhost:${PORT}`);
});
