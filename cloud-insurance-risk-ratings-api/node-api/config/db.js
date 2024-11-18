const { Pool } = require('pg');

// Create a pool of connections
const pool = new Pool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT,
    max: 10,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: true } : false,
});

// Improve error handling with async/await
pool.on('error', (err, client) => {
    console.error('Unexpected error on idle client', err);
    if (process.env.NODE_ENV !== 'production') {
        process.exit(-1);
    }
});

// Use async/await for initial connection test
const testConnection = async () => {
    try {
        const connection = await pool.connect();
        console.log('Database connected successfully!');
        connection.release();
    } catch (err) {
        console.error('Database connection error:', err.message);
        throw err;
    }
};

testConnection();

module.exports = pool;
