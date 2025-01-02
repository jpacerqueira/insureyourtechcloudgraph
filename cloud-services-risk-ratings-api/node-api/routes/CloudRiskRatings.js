const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Get all risk ratings
router.get('/premium/list/all/services', async function (req, res) {
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
router.get('/premium/fetch/service/id/:id', async function (req, res, next) {
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

// Get a specific risk rating by service_provider
router.get('/premium/fetch/service/service_provider/:service_provider', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var service_provider = req.params.service_provider;
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_provider = '${service_provider}'`
        );

        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;

        if (rows && rows.length > 0) {
            res.status(200).json(rows.slice(0, 100000)); // limit to 100000 rows
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
router.get('/premium/fetch/service/service_name/:service_name', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var service_name = req.params.service_name;
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_name = '${service_name}'`
        );

        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;

        if (rows && rows.length > 0) {
            res.status(200).json(rows.slice(0, 100000)); // limit to 100000 rows
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

// Get a specific risk rating by service_name and global_or_by_regions
router.get('/premium/fetch/service/service_name/:service_name/global_or_by_regions/:global_or_by_regions', async function (req, res, next) {
    let connection;
    try {
        connection = await db.connect();
        var service_name = req.params.service_name;
        var global_or_by_regions = req.params.global_or_by_regions;
        if (global_or_by_regions !== 'global' && global_or_by_regions !== 'regional') {
            res.status(400).json({ error: 'Invalid global_or_by_regions parameter - use either global or regional' });
            return;
        }
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_name = '${service_name}' AND global_or_by_regions = '${global_or_by_regions}'`
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

// Get all outage reports
router.get('/premium/outages/list/all', async function (req, res) {
    let connection;
    try {
        connection = await db.connect();
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= 1735689600  = > 01.Jan.2025 0h00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries
            WHERE outage_timestamp <= 1735689600`
        );
        
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            res.status(200).json(rows.slice(0, 100000));
        } else {
            res.status(200).json([]);
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve outage reports' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

// Get outage reports by cloud provider
router.get('/premium/outages/provider/:provider', async function (req, res) {
    let connection;
    try {
        connection = await db.connect();
        const provider = req.params.provider;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= 1735689600  = > 01.Jan.2025 0h00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE cloud_provider = $1 AND outage_timestamp <= 1735689600`,
            [provider]
        );
        
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            res.status(200).json(rows);
        } else {
            res.status(404).json({ error: 'No outage reports found for this provider' });
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve outage reports' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

// Get outage reports by service
router.get('/premium/outages/service/:service', async function (req, res) {
    let connection;
    try {
        connection = await db.connect();
        const service = req.params.service;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= 1735689600  = > 01.Jan.2025 0h00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE cloud_service = $1 AND outage_timestamp <= 1735689600`,
            [service]
        );
        
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            res.status(200).json(rows);
        } else {
            res.status(404).json({ error: 'No outage reports found for this service' });
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve outage reports' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

// Get outage reports by region
router.get('/premium/outages/region/:region', async function (req, res) {
    let connection;
    try {
        connection = await db.connect();
        const region = req.params.region;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= 1735689600  = > 01.Jan.2025 0h00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE regions LIKE $1 AND outage_timestamp <= 1735689600`,
            [`%${region}%`]
        );
        
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            res.status(200).json(rows);
        } else {
            res.status(404).json({ error: 'No outage reports found for this region' });
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve outage reports' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

module.exports = router;
