const express = require('express');
const dotenv = require('dotenv');
const path = require('path');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const { createProxyMiddleware } = require('http-proxy-middleware');

// Load environment variables
dotenv.config({ path: '.env' });

var https = require('https');
var http = require('http');
var fs = require('fs');

// Load environment variables
const port = process.env.PORT || 8186;
const is_prod = process.env.IS_PROD === "true";
var options = {
    key: fs.readFileSync('/app/certs/server8186.key'),
    cert: fs.readFileSync('/app/certs/server8186.cert')
  };

// Initialize Express app
const app = express();

// Custom Helmet Configuration
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'", "*"],
      scriptSrc: ["'self'", "'unsafe-inline'", '*'], // Allow inline scripts and any sources
      styleSrc: ["'self'", "'unsafe-inline'", '*'],  // Allow inline styles and any sources
      imgSrc: ["'self'", "https://t0.gstatic.com", "data:", "*"], // Allow external images and data URIs
      connectSrc: ["'self'", "*"],
      fontSrc: ["'self'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com", "*"],
      objectSrc: ["'self'", "*"],
      upgradeInsecureRequests: ["'self'", "*"], // Optional: Enforce HTTPS
    },
  },
}));

// Middleware for CORS
app.use(cors({
  origin: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: false,
  exposedHeaders: ['Access-Control-Allow-Origin']
}));

// Middleware for logging
app.use(morgan('combined'));

// Middleware to parse JSON requests
app.use(express.json());

// Proxy API requests to the Node API
app.use(
  '/api',
  createProxyMiddleware({
    target: 'https://node-api:8183/cloud-services-risk-ratings/services-app',
    changeOrigin: true,
    secure: false,
    pathRewrite: {
      '^/api': '',
    },
    logLevel: 'debug',
  })
);

// Serve static files from the React app
const buildPath = path.join(__dirname, 'build');
app.use(express.static(buildPath));

// Fallback to serve index.html for SPA routes
app.get('/cloud-services-app', (req, res) => {
  res.sendFile(path.join(buildPath, 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// Create HTTPS server and start server
if (is_prod) {
    https.createServer(options, app).listen(port, () => {
        console.log(`AppServices is running securely on HTTPS port ${port}`);
    });
  } else if (process.env.SSL_ENABLED === "true") {
    https.createServer(options, app).listen(port, () => {
        console.log(`AppServices is running securely on HTTPS port ${port}`);
    });
  } else {
    http.createServer(app).listen(port, () => {
        console.log(`AppServices is running on HTTP port ${port}`);
    });
  }
