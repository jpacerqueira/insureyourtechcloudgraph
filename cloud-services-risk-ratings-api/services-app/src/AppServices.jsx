import React, { useEffect, useState } from 'react';
import axios from 'axios';

// Update the API base URL from ENV
const API_BASE_URL = window.ENV.apiBaseUrl || '/api';

const PROVIDER_OPTIONS = [
  'Amazon AWS', 'Google Cloud GCP', 'Microsoft Azure', 'IBM Cloud', 'Oracle Cloud OCI', 'Snowflake',
   'Databricks', 'Salesforce', 'MongoDB', 'Cloudflare', 'Akamai'
];
const GLOBAL_OPTIONS = ['global', 'regional'];
const REGION_OPTIONS = [
  'global',
  'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
  'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1',
  'eu-south-1', 'eu-north-1',
  'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
  'sa-east-1', 'ca-central-1', 'ap-south-1', 'me-south-1', 'af-south-1', 
  'ap-east-1', 'ap-northeast-3', 'ap-southeast-3', 'ap-southeast-4',
  'europe-west1', 'europe-west2', 'asia-southeast1', 'asia-southeast2'
];
const AZ_OPTIONS = [
  'us-east-1a', 'us-east-1b', 'us-east-1c',
  'us-west-1a', 'us-west-1b',
  'europe-west1-b', 'europe-west1-c',
  'asia-southeast1-b', 'asia-southeast1-c',
  'eu-west1-b', 'eu-west1-c',
  'eu-west2-b', 'eu-west2-c',
  'eu-west3-b', 'eu-west3-c',
  'eu-central1-b', 'eu-central1-c',
  'eu-north1-b', 'eu-north1-c',
  'ap-northeast1-b', 'ap-northeast1-c',
  'ap-northeast2-b', 'ap-northeast2-c',
  'ap-southeast1-b', 'ap-southeast1-c',
  'ap-southeast2-b', 'ap-southeast2-c',
  'sa-east1-b', 'sa-east1-c',
  'ca-central1-b', 'ca-central1-c',
  'ap-south1-b', 'ap-south1-c',
  'me-south1-b', 'me-south1-c',
  'af-south1-b', 'af-south1-c',
  'ap-east1-b', 'ap-east1-c',
  'ap-northeast3-b', 'ap-northeast3-c',
  'ap-southeast3-b', 'ap-southeast3-c',
  'ap-southeast4-b', 'ap-southeast4-c'
];

function AppServices() {
  const [ratings, setRatings] = useState([]);
  const [newRecord, setNewRecord] = useState({
    database_key_id: '',
    service_name: '',
    service_provider: '',
    global_or_by_regions: '',
    region: '',
    availability_zone: '',
    service_load_at_customer_low_medium_high_very_high_1_2_3_4: '',
    customer_service_type_b2c_or_b2b_1_yes_0_no: '',
    customer_service_up_hours_8h_day_12h_day_24h_day: '',
    customer_service_annual_workdays: '',
    service_sla_0_99_9999_for_tier1: '',
    service_sla_0_99_9999_for_tier2: '',
    service_sla_0_99_9999_for_tier3: '',
    service_sla_0_99_9999_for_tier4: '',
    percentage_service_credit_back_tier1: '',
    percentage_service_credit_back_tier2: '',
    percentage_service_credit_back_tier3: '',
    percentage_service_credit_back_tier4: '',
    webscraper_annual_period_service_down_per_year_in_minutes: '',
    annual_service_minutes_up_365_24_60_equals_525600: '',
    expected_annual_service_minutes_up_by_sla_tier1: '',
    expected_annual_service_minutes_up_by_sla_tier2: '',
    expected_annual_service_minutes_up_by_sla_tier3: '',
    expected_annual_service_minutes_up_by_sla_tier4: '',
    expected_annual_service_minutes_down_by_sla_tier1: '',
    expected_annual_service_minutes_down_by_sla_tier2: '',
    expected_annual_service_minutes_down_by_sla_tier3: '',
    expected_annual_service_minutes_down_by_sla_tier4: '',
    service_debit_credit_more_than_annual_sla_tier1: '',
    expected_percentage_mins_down_inside_agreed_sla_tier1: '',
    actual_percentage_total_mins_down_from_webscraping: '',
    actual_percentage_mins_down_on_agreed_sla: '',
    gap_time_percent_between_SLA_down_actual_down: '',
    riskcoef_per_service_from_gap_expected_actual_time_down: '',
    service_sla_usage_percentage: '',
    service_traffic_coef_by_percent_down: '',
    sla_deviation_connected_risk_0_999: '',
    usage_connected_risk_0_999: '',
    annual_outage_time_days_hours_mins: '',
    remarks_outage_genai: '',
    public_locationa_and_status_genai: '',
    outages_other_impacted_services_genai: '',
    notes: ''
  });

  const [selectedRecord, setSelectedRecord] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/get-all-services`
      );
      setRatings(response.data);
    } catch (err) {
      console.error(err);
    }
  }

  function handleNewFieldChange(e) {
    setNewRecord({ ...newRecord, [e.target.name]: e.target.value });
  }

  async function handleCreate() {
    try {
      await axios.post(
        `${API_BASE_URL}/insert-new-service`,
        newRecord
      );
      alert('New record inserted!');
      setNewRecord({
        database_key_id: '',
        service_name: '',
        service_provider: '',
        global_or_by_regions: '',
        region: '',
        availability_zone: '',
        service_load_at_customer_low_medium_high_very_high_1_2_3_4: '',
        customer_service_type_b2c_or_b2b_1_yes_0_no: '',
        customer_service_up_hours_8h_day_12h_day_24h_day: '',
        customer_service_annual_workdays: '',
        service_sla_0_99_9999_for_tier1: '',
        service_sla_0_99_9999_for_tier2: '',
        service_sla_0_99_9999_for_tier3: '',
        service_sla_0_99_9999_for_tier4: '',
        percentage_service_credit_back_tier1: '',
        percentage_service_credit_back_tier2: '',
        percentage_service_credit_back_tier3: '',
        percentage_service_credit_back_tier4: '',
        webscraper_annual_period_service_down_per_year_in_minutes: '',
        annual_service_minutes_up_365_24_60_equals_525600: '',
        expected_annual_service_minutes_up_by_sla_tier1: '',
        expected_annual_service_minutes_up_by_sla_tier2: '',
        expected_annual_service_minutes_up_by_sla_tier3: '',
        expected_annual_service_minutes_up_by_sla_tier4: '',
        expected_annual_service_minutes_down_by_sla_tier1: '',
        expected_annual_service_minutes_down_by_sla_tier2: '',
        expected_annual_service_minutes_down_by_sla_tier3: '',
        expected_annual_service_minutes_down_by_sla_tier4: '',
        service_debit_credit_more_than_annual_sla_tier1: '',
        expected_percentage_mins_down_inside_agreed_sla_tier1: '',
        actual_percentage_total_mins_down_from_webscraping: '',
        actual_percentage_mins_down_on_agreed_sla: '',
        gap_time_percent_between_SLA_down_actual_down: '',
        riskcoef_per_service_from_gap_expected_actual_time_down: '',
        service_sla_usage_percentage: '',
        service_traffic_coef_by_percent_down: '',
        sla_deviation_connected_risk_0_999: '',
        usage_connected_risk_0_999: '',
        annual_outage_time_days_hours_mins: '',
        remarks_outage_genai: '',
        public_locationa_and_status_genai: '',
        outages_other_impacted_services_genai: '',
        notes: ''
      });
      loadData();
    } catch (err) {
      console.error(err);
      alert('Failed to create record.');
    }
  }

  function handleSelectRecord(record) {
    setSelectedRecord({ ...record });
  }

  function handleSelectedFieldChange(e) {
    if (!selectedRecord) return;
    setSelectedRecord({
      ...selectedRecord,
      [e.target.name]: e.target.value
    });
  }

  async function handleUpdate() {
    if (!selectedRecord) return;
    try {
      await axios.put(
        `${API_BASE_URL}/update-existing-service/${selectedRecord.database_key_id}`,
        selectedRecord
      );
      alert('Record updated!');
      setSelectedRecord(null);
      loadData();
    } catch (err) {
      console.error(err);
      alert('Failed to update record.');
    }
  }

  const renderInputField = (name, label, type = 'text', options = null) => {
    if (options) {
      return (
        <div>
          <label>{label}:</label>
          <select name={name} value={selectedRecord[name] || ''} onChange={handleSelectedFieldChange}>
            <option value="">--Select--</option>
            {options.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
      );
    }
    return (
      <div>
        <label>{label}:</label>
        <input
          type={type}
          name={name}
          value={selectedRecord[name] || ''}
          onChange={handleSelectedFieldChange}
        />
      </div>
    );
  };

  return (
    <div style={{ margin: '1rem' }}>
      <h1>Service Ratings</h1>

      {/* List all existing records */}
      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>ID</th>
            <th>Service Name</th>
            <th>Provider</th>
            <th>Global/Regional</th>
            <th>Region</th>
            <th>AZ</th>
            <th>Service Load</th>
            <th>Customer Service Type</th>
            <th>Service Up Hours</th>
            <th>Annual Workdays</th>
            <th>SLA Tier1</th>
            <th>SLA Tier2</th>
            <th>SLA Tier3</th>
            <th>SLA Tier4</th>
            <th>Credit Back Tier1</th>
            <th>Credit Back Tier2</th>
            <th>Credit Back Tier3</th>
            <th>Credit Back Tier4</th>
            <th>Webscraper Down Minutes</th>
            <th>Annual Service Minutes Up</th>
            <th>Expected SLA Up Tier1</th>
            <th>Expected SLA Up Tier2</th>
            <th>Expected SLA Up Tier3</th>
            <th>Expected SLA Up Tier4</th>
            <th>Expected SLA Down Tier1</th>
            <th>Expected SLA Down Tier2</th>
            <th>Expected SLA Down Tier3</th>
            <th>Expected SLA Down Tier4</th>
            <th>Debit Credit SLA Tier1</th>
            <th>Expected % Mins Down SLA Tier1</th>
            <th>Actual % Total Mins Down</th>
            <th>Actual % Mins Down SLA</th>
            <th>Gap Time % Between SLA</th>
            <th>Risk Coef</th>
            <th>SLA Usage %</th>
            <th>Traffic Coef % Down</th>
            <th>SLA Deviation Risk</th>
            <th>Usage Connected Risk</th>
            <th>Annual Outage Time</th>
            <th>Remarks</th>
            <th>Public Locations & Status</th>
            <th>Other Impacted Services</th>
            <th>Notes</th>
            <th>Select</th>
          </tr>
        </thead>
        <tbody>
          {ratings.map((r) => (
            <tr key={r.database_key_id}>
              <td>{r.database_key_id}</td>
              <td>{r.service_name}</td>
              <td>{r.service_provider}</td>
              <td>{r.global_or_by_regions}</td>
              <td>{r.region}</td>
              <td>{r.availability_zone}</td>
              <td>{r.service_load_at_customer_low_medium_high_very_high_1_2_3_4}</td>
              <td>{r.customer_service_type_b2c_or_b2b_1_yes_0_no}</td>
              <td>{r.customer_service_up_hours_8h_day_12h_day_24h_day}</td>
              <td>{r.customer_service_annual_workdays}</td>
              <td>{r.service_sla_0_99_9999_for_tier1}</td>
              <td>{r.service_sla_0_99_9999_for_tier2}</td>
              <td>{r.service_sla_0_99_9999_for_tier3}</td>
              <td>{r.service_sla_0_99_9999_for_tier4}</td>
              <td>{r.percentage_service_credit_back_tier1}</td>
              <td>{r.percentage_service_credit_back_tier2}</td>
              <td>{r.percentage_service_credit_back_tier3}</td>
              <td>{r.percentage_service_credit_back_tier4}</td>
              <td>{r.webscraper_annual_period_service_down_per_year_in_minutes}</td>
              <td>{r.annual_service_minutes_up_365_24_60_equals_525600}</td>
              <td>{r.expected_annual_service_minutes_up_by_sla_tier1}</td>
              <td>{r.expected_annual_service_minutes_up_by_sla_tier2}</td>
              <td>{r.expected_annual_service_minutes_up_by_sla_tier3}</td>
              <td>{r.expected_annual_service_minutes_up_by_sla_tier4}</td>
              <td>{r.expected_annual_service_minutes_down_by_sla_tier1}</td>
              <td>{r.expected_annual_service_minutes_down_by_sla_tier2}</td>
              <td>{r.expected_annual_service_minutes_down_by_sla_tier3}</td>
              <td>{r.expected_annual_service_minutes_down_by_sla_tier4}</td>
              <td>{r.service_debit_credit_more_than_annual_sla_tier1}</td>
              <td>{r.expected_percentage_mins_down_inside_agreed_sla_tier1}</td>
              <td>{r.actual_percentage_total_mins_down_from_webscraping}</td>
              <td>{r.actual_percentage_mins_down_on_agreed_sla}</td>
              <td>{r.gap_time_percent_between_SLA_down_actual_down}</td>
              <td>{r.riskcoef_per_service_from_gap_expected_actual_time_down}</td>
              <td>{r.service_sla_usage_percentage}</td>
              <td>{r.service_traffic_coef_by_percent_down}</td>
              <td>{r.sla_deviation_connected_risk_0_999}</td>
              <td>{r.usage_connected_risk_0_999}</td>
              <td>{r.annual_outage_time_days_hours_mins}</td>
              <td>{r.remarks_outage_genai}</td>
              <td>{r.public_locationa_and_status_genai}</td>
              <td>{r.outages_other_impacted_services_genai}</td>
              <td>{r.notes}</td>
              <td>
                <button onClick={() => handleSelectRecord(r)}>
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Form to create a new record */}
      <h2>Create New Record</h2>
      <div style={{ border: '1px solid gray', padding: '1rem' }}>
        {/* Database Key ID */}
        <div>
          <label>Database Key ID:</label>
          <input
            name="database_key_id"
            value={newRecord.database_key_id}
            onChange={handleNewFieldChange}
            type="number"
          />
        </div>
        {/* Service Name */}
        <div>
          <label>Service Name:</label>
          <input
            name="service_name"
            value={newRecord.service_name}
            onChange={handleNewFieldChange}
          />
        </div>
        {/* Service Provider */}
        <div>
          <label>Provider:</label>
          <select
            name="service_provider"
            value={newRecord.service_provider}
            onChange={handleNewFieldChange}
          >
            <option value="">--Select--</option>
            {PROVIDER_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
        {/* Global/Regional */}
        <div>
          <label>Global/Regional:</label>
          <select
            name="global_or_by_regions"
            value={newRecord.global_or_by_regions}
            onChange={handleNewFieldChange}
          >
            <option value="">--Select--</option>
            {GLOBAL_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
        {/* Region */}
        <div>
          <label>Region:</label>
          <select
            name="region"
            value={newRecord.region}
            onChange={handleNewFieldChange}
          >
            <option value="">--Select--</option>
            {REGION_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
        {/* Availability Zone */}
        <div>
          <label>Availability Zone:</label>
          <select
            name="availability_zone"
            value={newRecord.availability_zone}
            onChange={handleNewFieldChange}
          >
            <option value="">--Select--</option>
            {AZ_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
        {/* Service Load */}
        <div>
          <label>Service Load:</label>
          <input
            name="service_load_at_customer_low_medium_high_very_high_1_2_3_4"
            value={newRecord.service_load_at_customer_low_medium_high_very_high_1_2_3_4}
            onChange={handleNewFieldChange}
            type="number"
            min="1"
            max="4"
          />
        </div>
        {/* Customer Service Type */}
        <div>
          <label>Customer Service Type (B2C=1, B2B=0):</label>
          <select
            name="customer_service_type_b2c_or_b2b_1_yes_0_no"
            value={newRecord.customer_service_type_b2c_or_b2b_1_yes_0_no}
            onChange={handleNewFieldChange}
          >
            <option value="">--Select--</option>
            <option value="1">B2C</option>
            <option value="0">B2B</option>
          </select>
        </div>
        {/* Service Up Hours */}
        <div>
          <label>Service Up Hours:</label>
          <select
            name="customer_service_up_hours_8h_day_12h_day_24h_day"
            value={newRecord.customer_service_up_hours_8h_day_12h_day_24h_day}
            onChange={handleNewFieldChange}
          >
            <option value="">--Select--</option>
            <option value="8">8h day</option>
            <option value="12">12h day</option>
            <option value="24">24h day</option>
          </select>
        </div>
        {/* Annual Workdays */}
        <div>
          <label>Annual Workdays:</label>
          <input
            name="customer_service_annual_workdays"
            value={newRecord.customer_service_annual_workdays}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* SLA Tier1 */}
        <div>
          <label>SLA Tier1:</label>
          <input
            name="service_sla_0_99_9999_for_tier1"
            value={newRecord.service_sla_0_99_9999_for_tier1}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* SLA Tier2 */}
        <div>
          <label>SLA Tier2:</label>
          <input
            name="service_sla_0_99_9999_for_tier2"
            value={newRecord.service_sla_0_99_9999_for_tier2}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* SLA Tier3 */}
        <div>
          <label>SLA Tier3:</label>
          <input
            name="service_sla_0_99_9999_for_tier3"
            value={newRecord.service_sla_0_99_9999_for_tier3}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* SLA Tier4 */}
        <div>
          <label>SLA Tier4:</label>
          <input
            name="service_sla_0_99_9999_for_tier4"
            value={newRecord.service_sla_0_99_9999_for_tier4}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Percentage Service Credit Back Tier1 */}
        <div>
          <label>Percentage Service Credit Back Tier1:</label>
          <input
            name="percentage_service_credit_back_tier1"
            value={newRecord.percentage_service_credit_back_tier1}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Percentage Service Credit Back Tier2 */}
        <div>
          <label>Percentage Service Credit Back Tier2:</label>
          <input
            name="percentage_service_credit_back_tier2"
            value={newRecord.percentage_service_credit_back_tier2}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Percentage Service Credit Back Tier3 */}
        <div>
          <label>Percentage Service Credit Back Tier3:</label>
          <input
            name="percentage_service_credit_back_tier3"
            value={newRecord.percentage_service_credit_back_tier3}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Percentage Service Credit Back Tier4 */}
        <div>
          <label>Percentage Service Credit Back Tier4:</label>
          <input
            name="percentage_service_credit_back_tier4"
            value={newRecord.percentage_service_credit_back_tier4}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Webscraper Annual Period Service Down Minutes */}
        <div>
          <label>Webscraper Down Minutes:</label>
          <input
            type="number"
            name="webscraper_annual_period_service_down_per_year_in_minutes"
            value={newRecord.webscraper_annual_period_service_down_per_year_in_minutes}
            onChange={handleNewFieldChange}
          />
        </div>
        {/* Annual Service Minutes Up */}
        <div>
          <label>Annual Service Minutes Up:</label>
          <input
            name="annual_service_minutes_up_365_24_60_equals_525600"
            value={newRecord.annual_service_minutes_up_365_24_60_equals_525600}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Up by SLA Tier1 */}
        <div>
          <label>Expected SLA Up Tier1:</label>
          <input
            name="expected_annual_service_minutes_up_by_sla_tier1"
            value={newRecord.expected_annual_service_minutes_up_by_sla_tier1}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Up by SLA Tier2 */}
        <div>
          <label>Expected SLA Up Tier2:</label>
          <input
            name="expected_annual_service_minutes_up_by_sla_tier2"
            value={newRecord.expected_annual_service_minutes_up_by_sla_tier2}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Up by SLA Tier3 */}
        <div>
          <label>Expected SLA Up Tier3:</label>
          <input
            name="expected_annual_service_minutes_up_by_sla_tier3"
            value={newRecord.expected_annual_service_minutes_up_by_sla_tier3}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Up by SLA Tier4 */}
        <div>
          <label>Expected SLA Up Tier4:</label>
          <input
            name="expected_annual_service_minutes_up_by_sla_tier4"
            value={newRecord.expected_annual_service_minutes_up_by_sla_tier4}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Down by SLA Tier1 */}
        <div>
          <label>Expected SLA Down Tier1:</label>
          <input
            name="expected_annual_service_minutes_down_by_sla_tier1"
            value={newRecord.expected_annual_service_minutes_down_by_sla_tier1}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Down by SLA Tier2 */}
        <div>
          <label>Expected SLA Down Tier2:</label>
          <input
            name="expected_annual_service_minutes_down_by_sla_tier2"
            value={newRecord.expected_annual_service_minutes_down_by_sla_tier2}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Down by SLA Tier3 */}
        <div>
          <label>Expected SLA Down Tier3:</label>
          <input
            name="expected_annual_service_minutes_down_by_sla_tier3"
            value={newRecord.expected_annual_service_minutes_down_by_sla_tier3}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Expected Annual Service Minutes Down by SLA Tier4 */}
        <div>
          <label>Expected SLA Down Tier4:</label>
          <input
            name="expected_annual_service_minutes_down_by_sla_tier4"
            value={newRecord.expected_annual_service_minutes_down_by_sla_tier4}
            onChange={handleNewFieldChange}
            type="number"
            min="0"
          />
        </div>
        {/* Service Debit Credit More Than Annual SLA Tier1 */}
        <div>
          <label>Debit Credit SLA Tier1:</label>
          <input
            name="service_debit_credit_more_than_annual_sla_tier1"
            value={newRecord.service_debit_credit_more_than_annual_sla_tier1}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Expected Percentage Mins Down Inside Agreed SLA Tier1 */}
        <div>
          <label>Expected % Mins Down SLA Tier1:</label>
          <input
            name="expected_percentage_mins_down_inside_agreed_sla_tier1"
            value={newRecord.expected_percentage_mins_down_inside_agreed_sla_tier1}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Actual Percentage Total Mins Down from Webscraping */}
        <div>
          <label>Actual % Total Mins Down:</label>
          <input
            name="actual_percentage_total_mins_down_from_webscraping"
            value={newRecord.actual_percentage_total_mins_down_from_webscraping}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Actual Percentage Mins Down on Agreed SLA */}
        <div>
          <label>Actual % Mins Down SLA:</label>
          <input
            name="actual_percentage_mins_down_on_agreed_sla"
            value={newRecord.actual_percentage_mins_down_on_agreed_sla}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Gap Time Percent Between SLA Down Actual Down */}
        <div>
          <label>Gap Time % Between SLA:</label>
          <input
            name="gap_time_percent_between_SLA_down_actual_down"
            value={newRecord.gap_time_percent_between_SLA_down_actual_down}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Risk Coef Per Service */}
        <div>
          <label>Risk Coef:</label>
          <input
            name="riskcoef_per_service_from_gap_expected_actual_time_down"
            value={newRecord.riskcoef_per_service_from_gap_expected_actual_time_down}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* SLA Usage Percentage */}
        <div>
          <label>SLA Usage %:</label>
          <input
            name="service_sla_usage_percentage"
            value={newRecord.service_sla_usage_percentage}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Traffic Coef by Percent Down */}
        <div>
          <label>Traffic Coef % Down:</label>
          <input
            name="service_traffic_coef_by_percent_down"
            value={newRecord.service_traffic_coef_by_percent_down}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* SLA Deviation Connected Risk */}
        <div>
          <label>SLA Deviation Risk:</label>
          <input
            name="sla_deviation_connected_risk_0_999"
            value={newRecord.sla_deviation_connected_risk_0_999}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Usage Connected Risk */}
        <div>
          <label>Usage Connected Risk:</label>
          <input
            name="usage_connected_risk_0_999"
            value={newRecord.usage_connected_risk_0_999}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Annual Outage Time */}
        <div>
          <label>Annual Outage Time:</label>
          <input
            name="annual_outage_time_days_hours_mins"
            value={newRecord.annual_outage_time_days_hours_mins}
            onChange={handleNewFieldChange}
            type="text"
          />
        </div>
        {/* Remarks */}
        <div>
          <label>Remarks:</label>
          <textarea
            name="remarks_outage_genai"
            value={newRecord.remarks_outage_genai}
            onChange={handleNewFieldChange}
          />
        </div>
        {/* Public Locations and Status */}
        <div>
          <label>Public Locations & Status:</label>
          <textarea
            name="public_locationa_and_status_genai"
            value={newRecord.public_locationa_and_status_genai}
            onChange={handleNewFieldChange}
          />
        </div>
        {/* Other Impacted Services */}
        <div>
          <label>Other Impacted Services:</label>
          <textarea
            name="outages_other_impacted_services_genai"
            value={newRecord.outages_other_impacted_services_genai}
            onChange={handleNewFieldChange}
          />
        </div>
        {/* Notes */}
        <div>
          <label>Notes:</label>
          <textarea
            name="notes"
            value={newRecord.notes}
            onChange={handleNewFieldChange}
          />
        </div>
        <button onClick={handleCreate}>Insert New Record</button>
      </div>

      {/* If a record is selected, show an edit form */}
      {selectedRecord && (
        <div>
          <h2>Editing Record ID: {selectedRecord.database_key_id}</h2>
          <div style={{ border: '1px solid gray', padding: '1rem' }}>
            {/* Database Key ID */}
            <div>
              <label>Database Key ID:</label>
              <input
                name="database_key_id"
                value={selectedRecord.database_key_id}
                onChange={handleSelectedFieldChange}
                type="number"
              />
            </div>
            {/* Service Name */}
            <div>
              <label>Service Name:</label>
              <input
                name="service_name"
                value={selectedRecord.service_name || ''}
                onChange={handleSelectedFieldChange}
              />
            </div>
            {/* Service Provider */}
            <div>
              <label>Provider:</label>
              <select
                name="service_provider"
                value={selectedRecord.service_provider || ''}
                onChange={handleSelectedFieldChange}
              >
                <option value="">--Select--</option>
                {PROVIDER_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
            {/* Global/Regional */}
            <div>
              <label>Global/Regional:</label>
              <select
                name="global_or_by_regions"
                value={selectedRecord.global_or_by_regions || ''}
                onChange={handleSelectedFieldChange}
              >
                <option value="">--Select--</option>
                {GLOBAL_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
            {/* Region */}
            <div>
              <label>Region:</label>
              <select
                name="region"
                value={selectedRecord.region || ''}
                onChange={handleSelectedFieldChange}
              >
                <option value="">--Select--</option>
                {REGION_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
            {/* Availability Zone */}
            <div>
              <label>Availability Zone:</label>
              <select
                name="availability_zone"
                value={selectedRecord.availability_zone || ''}
                onChange={handleSelectedFieldChange}
              >
                <option value="">--Select--</option>
                {AZ_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
            {/* Service Load */}
            <div>
              <label>Service Load:</label>
              <input
                name="service_load_at_customer_low_medium_high_very_high_1_2_3_4"
                value={selectedRecord.service_load_at_customer_low_medium_high_very_high_1_2_3_4 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="1"
                max="4"
              />
            </div>
            {/* Customer Service Type */}
            <div>
              <label>Customer Service Type (B2C=1, B2B=0):</label>
              <select
                name="customer_service_type_b2c_or_b2b_1_yes_0_no"
                value={selectedRecord.customer_service_type_b2c_or_b2b_1_yes_0_no || ''}
                onChange={handleSelectedFieldChange}
              >
                <option value="">--Select--</option>
                <option value="1">B2C</option>
                <option value="0">B2B</option>
              </select>
            </div>
            {/* Service Up Hours */}
            <div>
              <label>Service Up Hours:</label>
              <select
                name="customer_service_up_hours_8h_day_12h_day_24h_day"
                value={selectedRecord.customer_service_up_hours_8h_day_12h_day_24h_day || ''}
                onChange={handleSelectedFieldChange}
              >
                <option value="">--Select--</option>
                <option value="8">8h day</option>
                <option value="12">12h day</option>
                <option value="24">24h day</option>
              </select>
            </div>
            {/* Annual Workdays */}
            <div>
              <label>Annual Workdays:</label>
              <input
                name="customer_service_annual_workdays"
                value={selectedRecord.customer_service_annual_workdays || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* SLA Tier1 */}
            <div>
              <label>SLA Tier1:</label>
              <input
                name="service_sla_0_99_9999_for_tier1"
                value={selectedRecord.service_sla_0_99_9999_for_tier1 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* SLA Tier2 */}
            <div>
              <label>SLA Tier2:</label>
              <input
                name="service_sla_0_99_9999_for_tier2"
                value={selectedRecord.service_sla_0_99_9999_for_tier2 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* SLA Tier3 */}
            <div>
              <label>SLA Tier3:</label>
              <input
                name="service_sla_0_99_9999_for_tier3"
                value={selectedRecord.service_sla_0_99_9999_for_tier3 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* SLA Tier4 */}
            <div>
              <label>SLA Tier4:</label>
              <input
                name="service_sla_0_99_9999_for_tier4"
                value={selectedRecord.service_sla_0_99_9999_for_tier4 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Percentage Service Credit Back Tier1 */}
            <div>
              <label>Percentage Service Credit Back Tier1:</label>
              <input
                name="percentage_service_credit_back_tier1"
                value={selectedRecord.percentage_service_credit_back_tier1 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Percentage Service Credit Back Tier2 */}
            <div>
              <label>Percentage Service Credit Back Tier2:</label>
              <input
                name="percentage_service_credit_back_tier2"
                value={selectedRecord.percentage_service_credit_back_tier2 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Percentage Service Credit Back Tier3 */}
            <div>
              <label>Percentage Service Credit Back Tier3:</label>
              <input
                name="percentage_service_credit_back_tier3"
                value={selectedRecord.percentage_service_credit_back_tier3 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Percentage Service Credit Back Tier4 */}
            <div>
              <label>Percentage Service Credit Back Tier4:</label>
              <input
                name="percentage_service_credit_back_tier4"
                value={selectedRecord.percentage_service_credit_back_tier4 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Webscraper Annual Period Service Down Minutes */}
            <div>
              <label>Webscraper Down Minutes:</label>
              <input
                type="number"
                name="webscraper_annual_period_service_down_per_year_in_minutes"
                value={selectedRecord.webscraper_annual_period_service_down_per_year_in_minutes || ''}
                onChange={handleSelectedFieldChange}
              />
            </div>
            {/* Annual Service Minutes Up */}
            <div>
              <label>Annual Service Minutes Up:</label>
              <input
                name="annual_service_minutes_up_365_24_60_equals_525600"
                value={selectedRecord.annual_service_minutes_up_365_24_60_equals_525600 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Up by SLA Tier1 */}
            <div>
              <label>Expected SLA Up Tier1:</label>
              <input
                name="expected_annual_service_minutes_up_by_sla_tier1"
                value={selectedRecord.expected_annual_service_minutes_up_by_sla_tier1 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Up by SLA Tier2 */}
            <div>
              <label>Expected SLA Up Tier2:</label>
              <input
                name="expected_annual_service_minutes_up_by_sla_tier2"
                value={selectedRecord.expected_annual_service_minutes_up_by_sla_tier2 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Up by SLA Tier3 */}
            <div>
              <label>Expected SLA Up Tier3:</label>
              <input
                name="expected_annual_service_minutes_up_by_sla_tier3"
                value={selectedRecord.expected_annual_service_minutes_up_by_sla_tier3 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Up by SLA Tier4 */}
            <div>
              <label>Expected SLA Up Tier4:</label>
              <input
                name="expected_annual_service_minutes_up_by_sla_tier4"
                value={selectedRecord.expected_annual_service_minutes_up_by_sla_tier4 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Down by SLA Tier1 */}
            <div>
              <label>Expected SLA Down Tier1:</label>
              <input
                name="expected_annual_service_minutes_down_by_sla_tier1"
                value={selectedRecord.expected_annual_service_minutes_down_by_sla_tier1 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Down by SLA Tier2 */}
            <div>
              <label>Expected SLA Down Tier2:</label>
              <input
                name="expected_annual_service_minutes_down_by_sla_tier2"
                value={selectedRecord.expected_annual_service_minutes_down_by_sla_tier2 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Down by SLA Tier3 */}
            <div>
              <label>Expected SLA Down Tier3:</label>
              <input
                name="expected_annual_service_minutes_down_by_sla_tier3"
                value={selectedRecord.expected_annual_service_minutes_down_by_sla_tier3 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Expected Annual Service Minutes Down by SLA Tier4 */}
            <div>
              <label>Expected SLA Down Tier4:</label>
              <input
                name="expected_annual_service_minutes_down_by_sla_tier4"
                value={selectedRecord.expected_annual_service_minutes_down_by_sla_tier4 || ''}
                onChange={handleSelectedFieldChange}
                type="number"
                min="0"
              />
            </div>
            {/* Service Debit Credit More Than Annual SLA Tier1 */}
            <div>
              <label>Debit Credit SLA Tier1:</label>
              <input
                name="service_debit_credit_more_than_annual_sla_tier1"
                value={selectedRecord.service_debit_credit_more_than_annual_sla_tier1 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Expected Percentage Mins Down Inside Agreed SLA Tier1 */}
            <div>
              <label>Expected % Mins Down SLA Tier1:</label>
              <input
                name="expected_percentage_mins_down_inside_agreed_sla_tier1"
                value={selectedRecord.expected_percentage_mins_down_inside_agreed_sla_tier1 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Actual Percentage Total Mins Down from Webscraping */}
            <div>
              <label>Actual % Total Mins Down:</label>
              <input
                name="actual_percentage_total_mins_down_from_webscraping"
                value={selectedRecord.actual_percentage_total_mins_down_from_webscraping || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Actual Percentage Mins Down on Agreed SLA */}
            <div>
              <label>Actual % Mins Down SLA:</label>
              <input
                name="actual_percentage_mins_down_on_agreed_sla"
                value={selectedRecord.actual_percentage_mins_down_on_agreed_sla || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Gap Time Percent Between SLA Down Actual Down */}
            <div>
              <label>Gap Time % Between SLA:</label>
              <input
                name="gap_time_percent_between_SLA_down_actual_down"
                value={selectedRecord.gap_time_percent_between_SLA_down_actual_down || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Risk Coef Per Service */}
            <div>
              <label>Risk Coef:</label>
              <input
                name="riskcoef_per_service_from_gap_expected_actual_time_down"
                value={selectedRecord.riskcoef_per_service_from_gap_expected_actual_time_down || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* SLA Usage Percentage */}
            <div>
              <label>SLA Usage %:</label>
              <input
                name="service_sla_usage_percentage"
                value={selectedRecord.service_sla_usage_percentage || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Traffic Coef by Percent Down */}
            <div>
              <label>Traffic Coef % Down:</label>
              <input
                name="service_traffic_coef_by_percent_down"
                value={selectedRecord.service_traffic_coef_by_percent_down || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* SLA Deviation Connected Risk */}
            <div>
              <label>SLA Deviation Risk:</label>
              <input
                name="sla_deviation_connected_risk_0_999"
                value={selectedRecord.sla_deviation_connected_risk_0_999 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Usage Connected Risk */}
            <div>
              <label>Usage Connected Risk:</label>
              <input
                name="usage_connected_risk_0_999"
                value={selectedRecord.usage_connected_risk_0_999 || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Annual Outage Time */}
            <div>
              <label>Annual Outage Time:</label>
              <input
                name="annual_outage_time_days_hours_mins"
                value={selectedRecord.annual_outage_time_days_hours_mins || ''}
                onChange={handleSelectedFieldChange}
                type="text"
              />
            </div>
            {/* Remarks */}
            <div>
              <label>Remarks:</label>
              <textarea
                name="remarks_outage_genai"
                value={selectedRecord.remarks_outage_genai || ''}
                onChange={handleSelectedFieldChange}
              />
            </div>
            {/* Public Locations and Status */}
            <div>
              <label>Public Locations & Status:</label>
              <textarea
                name="public_locationa_and_status_genai"
                value={selectedRecord.public_locationa_and_status_genai || ''}
                onChange={handleSelectedFieldChange}
              />
            </div>
            {/* Other Impacted Services */}
            <div>
              <label>Other Impacted Services:</label>
              <textarea
                name="outages_other_impacted_services_genai"
                value={selectedRecord.outages_other_impacted_services_genai || ''}
                onChange={handleSelectedFieldChange}
              />
            </div>
            {/* Notes */}
            <div>
              <label>Notes:</label>
              <textarea
                name="notes"
                value={selectedRecord.notes || ''}
                onChange={handleSelectedFieldChange}
              />
            </div>
            <button onClick={handleUpdate}>Update Record</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default AppServices;