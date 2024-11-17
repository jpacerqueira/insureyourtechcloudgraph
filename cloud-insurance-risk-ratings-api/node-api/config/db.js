const { Pool } = require('pg');

// Create a pool of connections
const pool = new Pool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    schema: process.env.DB_SCHEMA,
    port: process.env.DB_PORT,
    max: 10, // Maximum number of connections
    idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
    connectionTimeoutMillis: 2000, // Timeout after 2 seconds if no connection
});

module.exports = pool;
