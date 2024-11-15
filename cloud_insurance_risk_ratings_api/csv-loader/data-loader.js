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
});

function loadCSV(filePath, callback) {
  const results = [];
  
  // Read and parse the CSV file
  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (row) => {
      results.push(row); // Collect each row from CSV
    })
    .on('end', function () {
      console.log('CSV file successfully processed');
      callback(null, results); // Pass the parsed results to the callback
    })
    .on('error', function (err) {
      callback(err); // Pass error to the callback
    });
}

function insertData(rows, callback) {
  pool.connect(function (err, client, release) {
    if (err) {
      return callback(err); // Error connecting to DB
    }

    client.query('BEGIN', function (err) {
      if (err) {
        release();
        return callback(err); // Error starting transaction
      }

      // Iterate over each row in the CSV and insert it into the database
      let insertPromises = rows.map(function (row) {
        const columns = Object.keys(row).join(', ');
        const values = Object.values(row).map(function (val) {
          return `'${val}'`; // Wrap each value in single quotes for SQL
        }).join(', ');

        const query = `INSERT INTO risk_ratings (${columns}) VALUES (${values})`;
        return client.query(query);
      });

      // Execute all insert queries in parallel
      Promise.all(insertPromises)
        .then(function () {
          return client.query('COMMIT'); // Commit the transaction
        })
        .then(function () {
          release();
          callback(null, 'Data successfully inserted');
        })
        .catch(function (err) {
          client.query('ROLLBACK', function () { release(); }); // Rollback on error
          callback(err);
        });
    });
  });
}

function main(filePath) {
  loadCSV(filePath, function (err, rows) {
    if (err) {
      console.error('Error loading CSV:', err);
      return;
    }
    insertData(rows, function (err, result) {
      if (err) {
        console.error('Error inserting data:', err);
        return;
      }
      console.log(result);
    });
  });
}

// Execute the main function with the provided CSV file path
const filePath = process.argv[2]; // Get the CSV file path from command-line arguments
main(filePath);
