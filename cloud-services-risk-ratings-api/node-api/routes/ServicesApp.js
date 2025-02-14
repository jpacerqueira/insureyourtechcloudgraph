const express = require('express');
const router = express.Router();

// Create a connection pool to PostgreSQL
// (Adjust your connection settings / environment variables as needed)
const { poolServiceRiskRatings, poolCloudRiskPortal } = require('../config/db');

// Example: region & availability zone dropdown references
// (In real usage, you might load these from a table, config, or a constants file.)
const VALID_REGIONS = [
  'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
  'europe-west1', 'europe-west2', 'asia-southeast1', 'asia-southeast2'
];
const VALID_AVAILABILITY_ZONES = [
  'us-east-1a', 'us-east-1b', 'us-east-1c',
  'us-west-1a', 'us-west-1b', 
  'europe-west1-b', 'europe-west1-c',
  'asia-southeast1-b', 'asia-southeast1-c'
];

// Example set of "public cloud providers" for a dropdown
const VALID_PROVIDERS = ['Amazon AWS', 'Microsoft Azure', 'Google Cloud GCP', 'IBM Cloud', 'Oracle Cloud OCI', 'Cloudflare', 'Akamai', 'Macrometa', 'Salesforce', 'MongoDB', 'Databricks', 'Snowflake'];

// Example formula or derived value option
// Suppose we have a function to do derived calculations for certain columns.
// This function can be called after we receive user inputs for, say, webscraper_annual_period_service_down_per_year_in_minutes
function deriveValuesFromInput(record) {
  // Example: If you want to set "annual_outage_time_days_hours_mins" from a numeric field:
  // In reality, you would adapt these to your formulas from "formulas.csv"
  const minutesDown = parseFloat(record.webscraper_annual_period_service_down_per_year_in_minutes) || 0;
  if (minutesDown > 0) {
    // Example: let's just convert minutesDown to a days/hours/min string
    const days = Math.floor(minutesDown / (24 * 60));
    const hours = Math.floor((minutesDown % (24 * 60)) / 60);
    const mins = Math.floor(minutesDown % 60);
    record.annual_outage_time_days_hours_mins = `${days} days ${hours}h${mins}m`;
  }
  
  // You can add additional derived fields as needed, e.g.:
  // record.riskcoef_per_service_from_gap_expected_actual_time_down = ...
  // record.sla_deviation_connected_risk_0_999 = ...
  // etc. according to your CSV-based formulas
  return record;
}

// ----------------------------------------------------
// GET /cloud-services-risk-ratings/services-app/get-all-services
// Fetch all records from service_risk_ratings
router.get('/get-all-services', async (req, res) => {
  try {
    connection = await poolServiceRiskRatings.connect();
    const result = await connection.query(`
      SELECT 
        database_key_id,
        service_name,
        service_provider,
        global_or_by_regions,
        region,
        availability_zone,
        service_load_at_customer_low_medium_high_very_high_1_2_3_4,
        customer_service_type_b2c_or_b2b_1_yes_0_no,
        customer_service_up_hours_8h_day_12h_day_24h_day,
        customer_service_annual_workdays,
        service_sla_0_99_9999_for_tier1,
        service_sla_0_99_9999_for_tier2,
        service_sla_0_99_9999_for_tier3,
        service_sla_0_99_9999_for_tier4,
        percentage_service_credit_back_tier1,
        percentage_service_credit_back_tier2,
        percentage_service_credit_back_tier3,
        percentage_service_credit_back_tier4,
        webscraper_annual_period_service_down_per_year_in_minutes,
        annual_service_minutes_up_365_24_60_equals_525600,
        expected_annual_service_minutes_up_by_sla_tier1,
        expected_annual_service_minutes_up_by_sla_tier2,
        expected_annual_service_minutes_up_by_sla_tier3,
        expected_annual_service_minutes_up_by_sla_tier4,
        expected_annual_service_minutes_down_by_sla_tier1,
        expected_annual_service_minutes_down_by_sla_tier2,
        expected_annual_service_minutes_down_by_sla_tier3,
        expected_annual_service_minutes_down_by_sla_tier4,
        service_debit_credit_more_than_annual_sla_tier1,
        expected_percentage_mins_down_inside_agreed_sla_tier1,
        actual_percentage_total_mins_down_from_webscraping,
        actual_percentage_mins_down_on_agreed_sla,
        gap_time_percent_between_SLA_down_actual_down,
        riskcoef_per_service_from_gap_expected_actual_time_down,
        service_sla_usage_percentage,
        service_traffic_coef_by_percent_down,
        sla_deviation_connected_risk_0_999,
        usage_connected_risk_0_999,
        annual_outage_time_days_hours_mins,
        remarks_outage_genai,
        public_locationa_and_status_genai,
        outages_other_impacted_services_genai,
        notes
      FROM cloud_service_risk_ratings.service_risk_ratings
      ORDER BY database_key_id ASC
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error retrieving service_risk_ratings:', error);
    res.status(500).json({ error: 'Failed to retrieve data.' });
  }
});

// ----------------------------------------------------
// POST /cloud-services-risk-ratings/services-app/insert-new-service
// Insert a new record
router.post('/insert-new-service', async (req, res) => {
  try {
    const data = deriveValuesFromInput(req.body); // Apply formula-based derivations

    // Here we explicitly list columns we create:
    const insertQuery = `
      INSERT INTO cloud_service_risk_ratings.service_risk_ratings (
        service_name,
        service_provider,
        global_or_by_regions,
        region,
        availability_zone,
        service_load_at_customer_low_medium_high_very_high_1_2_3_4,
        customer_service_type_b2c_or_b2b_1_yes_0_no,
        customer_service_up_hours_8h_day_12h_day_24h_day,
        customer_service_annual_workdays,
        service_sla_0_99_9999_for_tier1,
        service_sla_0_99_9999_for_tier2,
        service_sla_0_99_9999_for_tier3,
        service_sla_0_99_9999_for_tier4,
        percentage_service_credit_back_tier1,
        percentage_service_credit_back_tier2,
        percentage_service_credit_back_tier3,
        percentage_service_credit_back_tier4,
        webscraper_annual_period_service_down_per_year_in_minutes,
        annual_outage_time_days_hours_mins,
        remarks_outage_genai,
        notes
      ) 
      VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21)
      RETURNING database_key_id
    `;
    const params = [
      data.service_name || null,
      data.service_provider || null,
      data.global_or_by_regions || null,
      data.region || null,
      data.availability_zone || null,
      data.service_load_at_customer_low_medium_high_very_high_1_2_3_4 || null,
      data.customer_service_type_b2c_or_b2b_1_yes_0_no || null,
      data.customer_service_up_hours_8h_day_12h_day_24h_day || null,
      data.customer_service_annual_workdays || null,
      data.service_sla_0_99_9999_for_tier1 || null,
      data.service_sla_0_99_9999_for_tier2 || null,
      data.service_sla_0_99_9999_for_tier3 || null,
      data.service_sla_0_99_9999_for_tier4 || null,
      data.percentage_service_credit_back_tier1 || null,
      data.percentage_service_credit_back_tier2 || null,
      data.percentage_service_credit_back_tier3 || null,
      data.percentage_service_credit_back_tier4 || null,
      data.webscraper_annual_period_service_down_per_year_in_minutes || null,
      data.annual_outage_time_days_hours_mins || null,
      data.remarks_outage_genai || null,
      data.notes || null,
    ];

    // Validate some fields if needed, e.g.:
    if (data.service_provider && !VALID_PROVIDERS.includes(data.service_provider)) {
      return res.status(400).json({ error: 'Invalid service_provider value.' });
    }
    if (data.global_or_by_regions && !['global', 'regional'].includes(data.global_or_by_regions)) {
      return res.status(400).json({ error: 'global_or_by_regions should be "global" or "regional".' });
    }
    if (data.region && !VALID_REGIONS.includes(data.region)) {
      return res.status(400).json({ error: 'Invalid region from the standard list.' });
    }
    if (data.availability_zone && !VALID_AVAILABILITY_ZONES.includes(data.availability_zone)) {
      return res.status(400).json({ error: 'Invalid availability_zone from the standard list.' });
    }

    connection = await poolServiceRiskRatings.connect();

    const result = await connection.query(insertQuery, params);
    res.status(201).json({
      message: 'Record inserted successfully.',
      newId: result.rows[0].database_key_id
    });
  } catch (error) {
    console.error('Error inserting new service_risk_ratings record:', error);
    res.status(500).json({ error: 'Failed to insert new record.' });
  }
});

// ----------------------------------------------------
// PUT /cloud-services-risk-ratings/services-app/update-existing-service/:database_key_id
// Update an existing record
router.put('/update-existing-service/:database_key_id', async (req, res) => {
  const { database_key_id } = req.params;
  try {
    const data = deriveValuesFromInput(req.body); // apply formula-based derivations

    const updateQuery = `
      UPDATE cloud_service_risk_ratings.service_risk_ratings
      SET 
        service_name = $1,
        service_provider = $2,
        global_or_by_regions = $3,
        region = $4,
        availability_zone = $5, 
        service_load_at_customer_low_medium_high_very_high_1_2_3_4 = $6,
        customer_service_type_b2c_or_b2b_1_yes_0_no = $7,
        customer_service_up_hours_8h_day_12h_day_24h_day = $8,
        customer_service_annual_workdays = $9,
        service_sla_0_99_9999_for_tier1 = $10,
        service_sla_0_99_9999_for_tier2 = $11,
        service_sla_0_99_9999_for_tier3 = $12,
        service_sla_0_99_9999_for_tier4 = $13,
        percentage_service_credit_back_tier1 = $14,
        percentage_service_credit_back_tier2 = $15,
        percentage_service_credit_back_tier3 = $16,
        percentage_service_credit_back_tier4 = $17,
        webscraper_annual_period_service_down_per_year_in_minutes = $18,
        annual_outage_time_days_hours_mins = $19,
        remarks_outage_genai = $20,
        notes = $21
      WHERE database_key_id = $22
      RETURNING database_key_id
    `;
    const params = [
      data.service_name || null,
      data.service_provider || null,
      data.global_or_by_regions || null,
      data.region || null,
      data.availability_zone || null,
      data.service_load_at_customer_low_medium_high_very_high_1_2_3_4 || null,
      data.customer_service_type_b2c_or_b2b_1_yes_0_no || null,
      data.customer_service_up_hours_8h_day_12h_day_24h_day || null,
      data.customer_service_annual_workdays || null,
      data.service_sla_0_99_9999_for_tier1 || null,
      data.service_sla_0_99_9999_for_tier2 || null,
      data.service_sla_0_99_9999_for_tier3 || null,
      data.service_sla_0_99_9999_for_tier4 || null,
      data.percentage_service_credit_back_tier1 || null,
      data.percentage_service_credit_back_tier2 || null,
      data.percentage_service_credit_back_tier3 || null,
      data.percentage_service_credit_back_tier4 || null,
      data.webscraper_annual_period_service_down_per_year_in_minutes || null,
      data.annual_outage_time_days_hours_mins || null,
      data.remarks_outage_genai || null,
      data.notes || null,
      database_key_id
    ];

    // Validate some fields again if needed
    if (data.service_provider && !VALID_PROVIDERS.includes(data.service_provider)) {
      return res.status(400).json({ error: 'Invalid service_provider value.' });
    }
    if (data.global_or_by_regions && !['global', 'regional'].includes(data.global_or_by_regions)) {
      return res.status(400).json({ error: 'global_or_by_regions should be "global" or "regional".' });
    }

    connection = await poolServiceRiskRatings.connect();
    const result = await connection.query(updateQuery, params);
    if (result.rowCount === 0) {
      return res.status(404).json({ error: 'Record not found or not updated.' });
    }
    res.json({
      message: 'Record updated successfully.',
      updatedId: result.rows[0].database_key_id
    });
  } catch (error) {
    console.error('Error updating service_risk_ratings record:', error);
    res.status(500).json({ error: 'Failed to update record.' });
  }
});

module.exports = router;