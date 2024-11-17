const express = require('express');
const dotenv = require('dotenv');
// Load environment variables
dotenv.config();

const riskRatingsRouter = require('./routes/CloudRiskRatings');

const app = express();
app.use(express.json());

// API Routes
app.use('/api/risk-ratings', riskRatingsRouter);

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, function () {
    console.log(`Server is running on http://localhost:${PORT}`);
});
