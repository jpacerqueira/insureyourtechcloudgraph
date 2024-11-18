const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Get all risk ratings
router.get('/list/all', async function (req, res) {
    let connection;
    try {
        connection = await db.connect();
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings`
        );
        
        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            res.status(200).json(rows.slice(0, 100000)); // limit to 100000 rows
        } else {
            res.status(200).json([]);
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve risk ratings' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

// Get a specific risk rating by ID
router.get('/fetch/id/:id', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var id = req.params.id;
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings WHERE database_key_id_10000000000001 = '${id}'`
        );

        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;

        if (rows && rows.length > 0) {
            res.status(200).json(rows[0]);
        } else {
            res.status(404).json({ error: 'Risk rating not found' });
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve risk rating' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

module.exports = router;
