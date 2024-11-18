const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Get all risk ratings
router.get('/list/all', async function (req, res) {
    try {
        const connection = await db.connect();
        const [rows] = await db.query(`SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings`);
        
        if (rows.length > 0) {
            res.status(200).json(rows.slice(0, 100000)); // limit to 100000 rows
        } else {
            res.status(200).json([]);
        }
        
        connection.release();
    } catch (err) {
        console.error('Database connection error:', err.message);
        res.status(500).json({ error: 'Failed to retrieve risk ratings' });
    }
});

// Get a specific risk rating by ID
router.get('/fetch/id/:id', async function (req, res, next) {
    try {
        const connection = await db.connect();
        var id = req.params.id;
        const [rows] = await db.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings WHERE database_key_id_10000000000001 = '${id}'`
        );
        
        if (rows.length > 0) {
            res.status(200).json(rows[0]);
        } else {
            res.status(404).json({ error: 'Risk rating not found' });
        }
        
        connection.release();
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to retrieve risk rating' });
    }
});

module.exports = router;
