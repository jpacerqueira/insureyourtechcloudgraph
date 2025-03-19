const express = require('express');
const router = express.Router();
const { poolServiceRiskRatings, poolCloudRiskPortal } = require('../config/db');

// NOTE: 
// 1.  Premium tier is not limited to data ranges in outages
// 2.  Premium tier is used in Customer Portal

// Add premium customer validation middleware
const validatePremiumCustomer = async (req, res, next) => {
    let connection;
    try {
        const customerId = req.query.customerId;
        
        if (!customerId) {
            return res.status(401).json({ 
                error: 'Access denied', 
                details: 'Customer ID is required'
            });
        }

        connection = await poolCloudRiskPortal.connect();
        const result = await connection.query(
            `SELECT customer_type, is_active 
             FROM "${process.env.DB_NAME_PORTAL}".customers 
             WHERE id = $1 AND is_deleted = false`,
            [customerId]
        );

        const customer = result.rows[0];

        if (!customer || !customer.is_active) {
            return res.status(403).json({ 
                error: 'Access denied',
                details: 'Customer not found or inactive'
            });
        }

        if (customer.customer_type !== 'premium') {
            return res.status(403).json({ 
                error: 'Premium access required',
                current_subscription: customer.customer_type,
                details: 'This endpoint requires a premium subscription'
            });
        }
        console.log(` FreemiumCloudRiskRatings API  - Customer id=${customerId} login attempt with customer_type: ${customer.customer_type}`);

        // Add customer info to request for logging/tracking
        req.customer = {
            id: customerId,
            type: customer.customer_type
        };

        next();
    } catch (err) {
        console.error('Premium validation error:', err);
        res.status(500).json({ 
            error: 'Internal server error',
            details: 'Failed to validate premium access'
        });
    } finally {
        if (connection) {
            connection.release();
        }
    }
};

// Apply middleware to all premium routes
router.use('/premium', validatePremiumCustomer);

// Get all risk ratings
router.get('/premium/list/all/services', async function (req, res) {
    let connection;
    try {
        connection = await poolServiceRiskRatings.connect();
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".service_risk_ratings`
        );
        
        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            // Log access for tracking
            console.log(`Premium customer id=${req.customer.id} accessed all services data`);
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
        connection = await poolServiceRiskRatings.connect();
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
        connection = await poolServiceRiskRatings.connect();
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
        connection = await poolServiceRiskRatings.connect();
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
        connection = await poolServiceRiskRatings.connect();
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
        connection = await poolServiceRiskRatings.connect();
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries
            WHERE outage_timestamp <= $1`,
            [now]
        );
        
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        if (rows && rows.length > 0) {
            // Log access for tracking
            console.log(`Premium customer id=${req.customer.id} accessed all outages data`);
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
        connection = await poolServiceRiskRatings.connect();
        const provider = req.params.provider;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE cloud_provider = $1 AND outage_timestamp <= $2`,
            [provider, now]
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
        connection = await poolServiceRiskRatings.connect();
        const service = req.params.service;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE cloud_service = $1 AND outage_timestamp <= $2`,
            [service, now]
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
        connection = await poolServiceRiskRatings.connect();
        const region = req.params.region;
        // Avoid LLM alucination records =>  data patch with outage_timestamp <= NOW()
        const now = Math.floor(new Date().getTime() / 1000).toString(); // Convert current time to Unix timestamp
        const result = await connection.query(
            `SELECT * FROM "${process.env.DB_NAME}".outage_report_summaries 
             WHERE regions LIKE $1 AND outage_timestamp <= $2`,
            [`%${region}%`, now]
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

// Get all customers with their submissions
router.get('/premium/customers/list/all', async function (req, res) {
    let connection;
    try {
        connection = await poolCloudRiskPortal.connect();
        const result = await connection.query(
            `SELECT c.id, c.username, c.email, c.customername, c.company, c.country, 
                    c.customer_type, c.is_active, c.is_deleted, c.created_at, c.updated_at,
                    json_agg(cs.*) as submissions
             FROM "${process.env.DB_NAME_PORTAL}".customers c
             LEFT JOIN "${process.env.DB_NAME_PORTAL}".customer_submissions cs ON c.id = cs.user_id
             WHERE c.customer_type = 'premium' or c.customer_type = 'freemium'
             GROUP BY c.id`
        );
        
        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        // Clean up null submissions
        const cleanedRows = rows.map(row => ({
            ...row,
            submissions: row.submissions[0] === null ? [] : row.submissions
        }));
        
        if (cleanedRows && cleanedRows.length > 0) {
            res.status(200).json(cleanedRows);
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

// Get a specific customer by customer_id
router.get('/premium/customers/fetch/customer/:customer_id', async function (req, res) {
    let connection;
    try {
        connection = await poolCloudRiskPortal.connect();
        var customer_id = req.params.customer_id;
        const result = await connection.query(
            `SELECT c.id, c.username, c.email, c.customername, c.company, c.country, 
                    c.customer_type, c.is_active, c.is_deleted, c.created_at, c.updated_at,
                    json_agg(cs.*) as submissions
             FROM "${process.env.DB_NAME_PORTAL}".customers c
             LEFT JOIN "${process.env.DB_NAME_PORTAL}".customer_submissions cs ON c.id = cs.user_id
             WHERE c.id = $1 AND (c.customer_type = 'premium' or c.customer_type = 'freemium')
             GROUP BY c.id`,
            [customer_id]
        );
        
        // Handle result based on the database library's return format
        const rows = Array.isArray(result) ? result[0] : result.rows;
        
        // Clean up null submissions
        const cleanedRows = rows.map(row => ({
            ...row,
            submissions: row.submissions[0] === null ? [] : row.submissions
        }));
        
        if (cleanedRows && cleanedRows.length > 0) {
            res.status(200).json(cleanedRows);
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
