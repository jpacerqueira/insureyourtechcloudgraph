const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Get all risk ratings
router.get('/freemium/list/all/services', async function (req, res) {
    let connection;
    try {
        connection = await db.connect();
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, region_or_global, remarks_outage_genai
              FROM "${process.env.DB_NAME}".service_risk_ratings`
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
router.get('/freemium/fetch/service/id/:id', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var id = req.params.id;
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, region_or_global,
            webscraper_annual_period_service_down_per_year_in_minutes, expected_percentage_mins_down_on_agreed_sla,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, remarks_outage_genai 
               FROM "${process.env.DB_NAME}".service_risk_ratings WHERE database_key_id = '${id}'`
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

// Get a specific risk rating by service_provider
router.get('/freemium/fetch/service/service_provider/:service_provider', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var service_provider = req.params.service_provider;
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, region_or_global,
            webscraper_annual_period_service_down_per_year_in_minutes, expected_percentage_mins_down_on_agreed_sla,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, remarks_outage_genai  
            FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_provider = '${service_provider}'`
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

// Get a specific risk rating by service_name
router.get('/freemium/fetch/service/service_name/:service_name', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var service_name = req.params.service_name;
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, region_or_global,
            webscraper_annual_period_service_down_per_year_in_minutes, expected_percentage_mins_down_on_agreed_sla,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, remarks_outage_genai 
            FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_name = '${service_name}'`
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
