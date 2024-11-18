
const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Get all risk ratings
router.get('/list/all', function (req, res) {
    db.query(`SELECT * FROM service_risk_ratings `)
        .then(function ([rows]) {
            res.json(rows);
        })
        .catch(function (err) {
            console.error(err);
            res.status(500).json({ error: 'Failed to retrieve risk ratings' });
        });
});

// Get a specific risk rating by ID
router.get('/id=:id', function (req, res) {
    const { id } = req.params;
    db.query(`SELECT * FROM service_risk_ratings WHERE database_key_id_10000000000001 = ? `, [id])
        .then(function ([rows]) {
            if (rows.length > 0) {
                res.json(rows[0]);
            } else {
                res.status(404).json({ error: 'Risk rating not found' });
            }
        })
        .catch(function (err) {
            console.error(err);
            res.status(500).json({ error: 'Failed to retrieve risk rating' });
        });
});

module.exports = router;
