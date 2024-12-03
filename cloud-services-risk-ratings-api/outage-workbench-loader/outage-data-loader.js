const dotenv = require('dotenv');
dotenv.config({ path: '.env' });
const fs = require('fs');
const { Pool } = require('pg');
const csv = require('csv-parser');

// Set up PostgreSQL connection pool
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT,
  schema: process.env.DB_NAME,
  search_path: process.env.DB_NAME,
  max: 100,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: true } : false,
});

async function transformAndInsertData(sourceTable, targetTable, transformationRules) {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');

    // Read data from source table
    const sourceQuery = `SELECT * FROM "${process.env.DB_NAME}"."${sourceTable}"`;
    const { rows: sourceData } = await client.query(sourceQuery);

    // Transform data according to rules
    const transformedRows = sourceData.map(row => {
      const transformedRow = {};
      for (const [targetField, rule] of Object.entries(transformationRules)) {
        if (typeof rule === 'function') {
          transformedRow[targetField] = rule(row);
        } else if (typeof rule === 'string') {
          transformedRow[targetField] = row[rule]; // Direct field mapping
        }
      }
      return transformedRow;
    });

    // Insert transformed data
    for (const row of transformedRows) {
      const columns = Object.keys(row).join(', ');
      const values = Object.values(row).map(val => 
        val === null ? 'NULL' : `'${val}'`
      ).join(', ');

      const insertQuery = `
        INSERT INTO "${process.env.DB_NAME}"."${targetTable}" (${columns})
        VALUES (${values})
      `;
      await client.query(insertQuery);
    }

    await client.query('COMMIT');
    console.log(`Successfully transformed and inserted ${transformedRows.length} rows`);
    
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

async function main() {
  // Example transformation rules
  const transformationRules = {
    'new_field': 'old_field',
    'calculated_field': (row) => row.value * 2,
    'status': (row) => {
      if (row.risk_score > 80) return 'HIGH';
      if (row.risk_score > 50) return 'MEDIUM';
      return 'LOW';
    }
  };

  try {
    await transformAndInsertData(
      'outage_report_summaries', //source tables
      'service_risk_ratings', //target table
      transformationRules
    );
  } catch (error) {
    console.error('Error during transformation:', error);
    process.exit(1);
  }
}

// Validate environment variables
// ... existing validation code ...

main().catch(console.error);
