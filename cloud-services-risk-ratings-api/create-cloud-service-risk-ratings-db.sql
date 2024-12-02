CREATE DATABASE cloud_service_risk_ratings; -- from docker-compose.yml
 \c cloud_service_risk_ratings;
CREATE SCHEMA cloud_service_risk_ratings;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cloud_service_risk_ratings TO postgres;
grant all on database cloud_service_risk_ratings to postgres;
grant all on schema "public" to postgres;
grant all on all tables in schema "public" to postgres;
grant all on all sequences in schema "public" to postgres;
grant all on schema "cloud_service_risk_ratings" to postgres;
grant all on all tables in schema "cloud_service_risk_ratings" to postgres;
grant all on all sequences in schema "cloud_service_risk_ratings" to postgres;

--
-- Create the service_risk_ratings table in schema cloud_service_risk_ratings
--
-- truncate_if_exists function
CREATE OR REPLACE FUNCTION public.truncate_if_exists(_table text, _schema text DEFAULT NULL)
  RETURNS text
  LANGUAGE plpgsql AS
$func$
DECLARE
   _qual_tbl text := concat_ws('.', quote_ident(_schema), quote_ident(_table));
   _row_found bool;
BEGIN
   IF to_regclass(_qual_tbl) IS NOT NULL THEN   -- table exists
      EXECUTE 'SELECT EXISTS (SELECT FROM ' || _qual_tbl || ')'
      INTO _row_found;

      IF _row_found THEN                        -- table is not empty
         EXECUTE 'TRUNCATE ' || _qual_tbl;
         RETURN 'Table truncated: ' || _qual_tbl;
      ELSE  -- optional!
         RETURN 'Table exists but is empty: ' || _qual_tbl;
      END IF;
   ELSE  -- optional!
      RETURN 'Table not found: ' || _qual_tbl;
   END IF;
END
$func$;

SELECT public.truncate_if_exists('service_risk_ratings', 'cloud_service_risk_ratings');
DROP TABLE IF EXISTS cloud_service_risk_ratings.service_risk_ratings;

CREATE TABLE cloud_service_risk_ratings.service_risk_ratings (
    database_key_id bigint,
    service_name text,
    service_provider text,
    global_or_by_regions text,
    region text,
    availability_zone text,
    service_load_at_customer_low_medium_high_very_high_1_2_3_4 text,
    customer_service_type_b2c_or_b2b_1_yes_0_no text,
    customer_service_up_hours_8h_day_12h_day_24h_day text,
    customer_service_annual_workdays text,
    service_sla_0_99_9999_for_tier1 text ,
    service_sla_0_99_9999_for_tier2 text,
    service_sla_0_99_9999_for_tier3 text,
    service_sla_0_99_9999_for_tier4 text, 
    percentage_service_credit_back_tier1 text,
    percentage_service_credit_back_tier2 text,
    percentage_service_credit_back_tier3 text,
    percentage_service_credit_back_tier4 text,
    webscraper_annual_period_service_down_per_year_in_minutes text,
    annual_service_minutes_up_365_24_60_equals_525600 text,
    expected_annual_service_minutes_up_by_sla_tier1 text,
    expected_annual_service_minutes_up_by_sla_tier2 text,
    expected_annual_service_minutes_up_by_sla_tier3 text,
    expected_annual_service_minutes_up_by_sla_tier4 text,
    expected_annual_service_minutes_down_by_sla_tier1 text,
    expected_annual_service_minutes_down_by_sla_tier2 text,
    expected_annual_service_minutes_down_by_sla_tier3 text,
    expected_annual_service_minutes_down_by_sla_tier4 text,
    service_debit_debit_more_than_annual_sla_tier1 text,
    expected_percentage_mins_down_inside_agreed_sla_tier1 text,
    actual_percentage_total_mins_down_from_webscraping text,
    actual_percentage_mins_down_on_agreed_sla text,
    gap_time_percent_between_SLA_down_actual_down text,
    riskcoef_per_service_from_gap_expected_actual_time_down text,
    service_sla_usage_percentage text,
    service_traffic_coef_by_percent_down text,
    sla_deviation_connected_risk_0_999 text,
    usage_connected_risk_0_999 text,
    annual_outage_time_days_hours_mins text,
    remarks_outage_genai text,
    public_locationa_and_status_genai text,
    outages_other_impacted_services_genai text,
    notes text
);

CREATE TABLE cloud_service_risk_ratings.outage_report_summaries (
    outage_timestamp DECIMAL(16,6),
    source_outage_report TEXT,
    cloud_provider TEXT,
    cloud_service TEXT,
    regions TEXT,
    availability_zones TEXT,
    start_time TEXT,
    end_time TEXT,
    outage_status TEXT,
    impact TEXT,
    duration TEXT,
    duration_minutes DECIMAL(16,6),
    root_cause TEXT,
    resolution TEXT,
    downtime_period TEXT,
    incident_id TEXT,
    affected_components TEXT,
    mitigation_steps TEXT,
    cloudrisk_genai_output TEXT
);

--
-- Truncated variable names
--
-- postgres-db  | GRANT
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:46: NOTICE:  identifier "customer_service_annual_workdays" will be truncated to "customer_service_anual_days_daily_or_weekly_or_weekends_365_261"
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:46: NOTICE:  identifier "service_debit_debit_more_than_annual_sla_tier1" will be truncated to "service_debit_credit_anual_sla_minutes_in_positive_credit_or_ne"
-- postgres-db  | CREATE TABLE
-- postgres-db  |  session_user |      current_database      
-- postgres-db  | --------------+----------------------------
-- postgres-db  |  postgres     | cloud_service_risk_ratings
-- postgres-db  | (1 row)
--

SELECT session_user, current_database();

SELECT table_catalog, table_schema, table_name, column_name, column_default, is_nullable 
    FROM information_schema.columns 
    WHERE table_schema like '%'
    ORDER BY table_schema, table_name, ordinal_position;

SELECT * FROM pg_tables;

INSERT INTO "cloud_service_risk_ratings".service_risk_ratings (
   database_key_id, service_name, service_provider, global_or_by_regions, region, availability_zone,
   service_load_at_customer_low_medium_high_very_high_1_2_3_4, customer_service_type_b2c_or_b2b_1_yes_0_no, customer_service_up_hours_8h_day_12h_day_24h_day,
   customer_service_annual_workdays, service_sla_0_99_9999_for_tier1, service_sla_0_99_9999_for_tier2, service_sla_0_99_9999_for_tier3,
   service_sla_0_99_9999_for_tier4, percentage_service_credit_back_tier1, percentage_service_credit_back_tier2, percentage_service_credit_back_tier3, percentage_service_credit_back_tier4,
   webscraper_annual_period_service_down_per_year_in_minutes, annual_service_minutes_up_365_24_60_equals_525600,
   expected_annual_service_minutes_up_by_sla_tier1, expected_annual_service_minutes_up_by_sla_tier2, expected_annual_service_minutes_up_by_sla_tier3, expected_annual_service_minutes_up_by_sla_tier4,
   expected_annual_service_minutes_down_by_sla_tier1, expected_annual_service_minutes_down_by_sla_tier2, expected_annual_service_minutes_down_by_sla_tier3, expected_annual_service_minutes_down_by_sla_tier4,
   service_debit_debit_more_than_annual_sla_tier1, expected_percentage_mins_down_inside_agreed_sla_tier1,
   actual_percentage_total_mins_down_from_webscraping, actual_percentage_mins_down_on_agreed_sla, gap_time_percent_between_SLA_down_actual_down, riskcoef_per_service_from_gap_expected_actual_time_down,
   service_sla_usage_percentage, service_traffic_coef_by_percent_down, sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, annual_outage_time_days_hours_mins, remarks_outage_genai,
   public_locationa_and_status_genai, outages_other_impacted_services_genai, notes)
 VALUES (10000000000000,'Wost Possible Techology','BAD CLOUD EXAMPLE','global','','','4','1','24','365','99.99999','99.99999',
 '99.99999','99.99999','10.000','25.000','50.000','100.000','520000.00','525600.000','525599.947','525599.947','525599.947','525599.947','0.053',
 '0.053','0.053','0.053','-519999.947','0.000010%','98.93455099%','98.93456088%','-98.934551%','98.934551%','989345609.17%','98.93455%','-9883551.992','-1966.069','','','','','') ;

INSERT INTO cloud_service_risk_ratings.outage_report_summaries (
    outage_timestamp,
    source_outage_report,
    cloud_provider,
    cloud_service,
    regions,
    availability_zones,
    start_time,
    end_time,
    outage_status,
    impact,
    duration,
    duration_minutes,
    root_cause,
    resolution,
    downtime_period,
    incident_id,
    affected_components,
    mitigation_steps,
    cloudrisk_genai_output
) VALUES (
   1575244800.0,
   '20190823-Summary of the Amazon EC2 Issues in the Asia Pacific (Tokyo) Region (AP-NORTHEAST-1)',
   'AWS',
   'Amazon Elastic Compute Cloud',
   'AP-NORTHEAST-1 Tokyo',
   'Tokyo (AP-NORTHEAST-1)',
   '2019-12-02T00:00:00+00:00',
   '2019-08-23T00:00:00',
   'resolved',
   '',
   'EC2 instances and degraded EBS volume performance for some resources in the affected area of the Availability Zone: 5 hours and 30 minutes',
   330,
   '"Control system failure that caused multiple, redundant cooling systems to fail in parts of the affected Availability Zone."',
   '',
   'EC2 instances and degraded EBS volume performance for some resources in the affected area of the Availability Zone: 5 hours and 30 minutes',
   '',
   '',
   '',
   '"Source Outage Report: 20190823-Summary of the Amazon EC2 Issues in the Asia Pacific (Tokyo) Region (AP-NORTHEAST-1)
Cloud Provider: AWS
Cloud Services: Amazon Elastic Compute Cloud, Amazon Elastic Block Store, Amazon ElastiCache, Direct Connect, rs
Regions: AP-NORTHEAST-1, Tokyo
Availability Zones: Tokyo (AP-NORTHEAST-1)
Start Time: 2019-12-02 00:00:00+00:00
Outage Status: resolved
Impact Level: 
Duration: EC2 instances and degraded EBS volume performance for some resources in the affected area of the Availability Zone: 5 hours and 30 minutes
Duration (minutes): 330
Root Cause: Control system failure that caused multiple, redundant cooling systems to fail in parts of the affected Availability Zone.
Resolution: 
Downtime Period: EC2 instances and degraded EBS volume performance for some resources in the affected area of the Availability Zone: 5 hours and 30 minutes"'
);

SELECT * FROM cloud_service_risk_ratings.service_risk_ratings;

SELECT * FROM cloud_service_risk_ratings.outage_report_summaries;
