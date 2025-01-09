const express = require('express');
const router = express.Router();
const { poolServiceRiskRatings, poolCloudRiskPortal } = require('../config/db');

// Get all risk ratings
router.get('/freemium/list/all/services', async function (req, res) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, global_or_by_regions, region
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
        connection = await poolServiceRiskRatings.connect();
        var id = req.params.id;
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, global_or_by_regions, region, 
            service_sla_0_99_9999_for_tier1, service_sla_0_99_9999_for_tier2, service_sla_0_99_9999_for_tier3, service_sla_0_99_9999_for_tier4,
            percentage_service_credit_back_tier1, percentage_service_credit_back_tier2, percentage_service_credit_back_tier3, percentage_service_credit_back_tier4,
            expected_annual_service_minutes_down_by_sla_tier1, expected_annual_service_minutes_down_by_sla_tier2, expected_annual_service_minutes_down_by_sla_tier3, expected_annual_service_minutes_down_by_sla_tier4,
            webscraper_annual_period_service_down_per_year_in_minutes,
            expected_percentage_mins_down_inside_agreed_sla_tier1,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage, service_traffic_coef_by_percent_down,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, annual_outage_time_days_hours_mins, remarks_outage_genai 
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

// Get all specific risk rating by service_provider
router.get('/freemium/fetch/service/service_provider/:service_provider', async function (req, res, next) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        var service_provider = req.params.service_provider;
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, global_or_by_regions, region,
            service_sla_0_99_9999_for_tier1, service_sla_0_99_9999_for_tier2, service_sla_0_99_9999_for_tier3, service_sla_0_99_9999_for_tier4,
            percentage_service_credit_back_tier1, percentage_service_credit_back_tier2, percentage_service_credit_back_tier3, percentage_service_credit_back_tier4,
            expected_annual_service_minutes_down_by_sla_tier1, expected_annual_service_minutes_down_by_sla_tier2, expected_annual_service_minutes_down_by_sla_tier3, expected_annual_service_minutes_down_by_sla_tier4,
            webscraper_annual_period_service_down_per_year_in_minutes,
            expected_percentage_mins_down_inside_agreed_sla_tier1,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage, service_traffic_coef_by_percent_down,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, annual_outage_time_days_hours_mins, remarks_outage_genai  
            FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_provider = '${service_provider}'`
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
router.get('/freemium/fetch/service/service_name/:service_name', async function (req, res, next) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        var service_name = req.params.service_name;
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, global_or_by_regions, region,
            service_sla_0_99_9999_for_tier1, service_sla_0_99_9999_for_tier2, service_sla_0_99_9999_for_tier3, service_sla_0_99_9999_for_tier4,
            percentage_service_credit_back_tier1, percentage_service_credit_back_tier2, percentage_service_credit_back_tier3, percentage_service_credit_back_tier4, 
            expected_annual_service_minutes_down_by_sla_tier1, expected_annual_service_minutes_down_by_sla_tier2, expected_annual_service_minutes_down_by_sla_tier3, expected_annual_service_minutes_down_by_sla_tier4,
            webscraper_annual_period_service_down_per_year_in_minutes,
            expected_percentage_mins_down_inside_agreed_sla_tier1,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage, service_traffic_coef_by_percent_down,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, annual_outage_time_days_hours_mins, remarks_outage_genai 
            FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_name = '${service_name}'`
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
router.get('/freemium/fetch/service/service_name/:service_name/global_or_by_regions/:global_or_by_regions', async function (req, res, next) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        var service_name = req.params.service_name;
        var global_or_by_regions = req.params.global_or_by_regions;
        if (global_or_by_regions !== 'global' && global_or_by_regions !== 'regional') {
            res.status(400).json({ error: 'Invalid global_or_by_regions parameter - use either global or regional' });
            return;
        }
        const result = await connection.query(
            `SELECT database_key_id, service_name, service_provider, global_or_by_regions, region,
            service_sla_0_99_9999_for_tier1, service_sla_0_99_9999_for_tier2, service_sla_0_99_9999_for_tier3, service_sla_0_99_9999_for_tier4,
            percentage_service_credit_back_tier1, percentage_service_credit_back_tier2, percentage_service_credit_back_tier3, percentage_service_credit_back_tier4,
            expected_annual_service_minutes_down_by_sla_tier1, expected_annual_service_minutes_down_by_sla_tier2, expected_annual_service_minutes_down_by_sla_tier3, expected_annual_service_minutes_down_by_sla_tier4,
            webscraper_annual_period_service_down_per_year_in_minutes,
            expected_percentage_mins_down_inside_agreed_sla_tier1,
            actual_percentage_total_mins_down_from_webscraping, service_sla_usage_percentage, service_traffic_coef_by_percent_down,
            sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, annual_outage_time_days_hours_mins, remarks_outage_genai 
            FROM "${process.env.DB_NAME}".service_risk_ratings WHERE service_name = '${service_name}' AND global_or_by_regions = '${global_or_by_regions}'`
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
router.get('/freemium/outages/list/all', async function (req, res) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()  = > 01.Jan.2025 0h00
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        // outage_timestamp >= 1727740800 = > Date and time (your time zone): Tuesday, 1 October 2024 01:00:00 GMT+01:00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries
            WHERE outage_timestamp >= 1727740800 AND outage_timestamp <= $1`,
            [now]
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
router.get('/freemium/outages/provider/:provider', async function (req, res) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        const provider = req.params.provider;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()  = > 01.Jan.2025 0h00
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        // outage_timestamp >= 1727740800 = > Date and time (your time zone): Tuesday, 1 October 2024 01:00:00 GMT+01:00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE outage_timestamp >= 1727740800 AND outage_timestamp <= $1 AND cloud_provider = $2`,
            [now, provider]
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
router.get('/freemium/outages/service/:service', async function (req, res) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        const service = req.params.service;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()  = > 01.Jan.2025 0h00
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        // outage_timestamp >= 1727740800 = > Date and time (your time zone): Tuesday, 1 October 2024 01:00:00 GMT+01:00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE outage_timestamp >= 1727740800 AND outage_timestamp <= $1 AND cloud_service = $2`,
            [now, service]
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
router.get('/freemium/outages/region/:region', async function (req, res) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        const region = req.params.region;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()  = > 01.Jan.2025 0h00
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        // outage_timestamp >= 1727740800 = > Date and time (your time zone): Tuesday, 1 October 2024 01:00:00 GMT+01:00
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE outage_timestamp >= 1727740800 AND outage_timestamp <= $1 AND regions LIKE $2`,
            [now, `%${region}%`]
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

// Get all customers
router.get('/freemium/customers/list/all', async function (req, res) {
    let connection;
    try {
        connection = await poolCloudRiskPortal.connect();
        const result = await connection.query(
            `SELECT id, username, email, customername, company, country, customer_type, is_active, is_deleted, created_at, updated_at
             FROM "${process.env.DB_NAME_PORTAL}".customers WHERE customer_type = 'freemium'`
        );
        
        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            res.status(200).json(rows);
        } else {
            res.status(200).json([]);
        }
    } catch (err) {
        console.error('Database connection error:', err);
        res.status(500).json({ error: 'Failed to retrieve customers' });
    } finally {
        if (connection) {
            connection.release();
        }
    }
});

module.exports = router;
