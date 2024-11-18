
const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Get all risk ratings
router.get('/list/all', function (req, res) {
    db.query(`SELECT * FROM "public".service_risk_ratings `)
        .then(function ([rows]) {
            res.status(200).json(rows);
        })
        .catch(function (err) {
            console.error(err);
            res.status(500).json({ error: 'Failed to retrieve risk ratings' });
        });
});

// Get a specific risk rating by ID
router.get('/fetch/id/:id', function (req, res, next) {
    var id = req.params.id;
    db.query(`SELECT * FROM "public".service_risk_ratings WHERE database_key_id_10000000000001 = ${id} `)
        .then(function ([rows]) {
            if (rows.length > 0) {
                res.status(200).json(rows[0]);
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
