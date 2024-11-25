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
    customer_service_anual_days_daily_or_weekly_or_weekends_365_261_104 text,
    service_sla_0_99_9999_for_60min_times_24h_365days text ,
    percentage_service_credit_back text,
    webscraper_annual_period_service_down_per_year_in_minutes text,
    annual_service_minutes_up_365_24_60_equals_525600 text,
    expected_by_sla_annual_service_minutes_up_365_times_24_60_equals_525600 text,
    expected_annual_service_minutes_down text,
    service_debit_credit_anual_sla_minutes_in_positive_credit_or_negative_debit_more_than_sla text,
    expected_percentage_mins_down_on_agreed_sla text,
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


--
-- Truncated variable names
--
-- postgres-db  | GRANT
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:46: NOTICE:  identifier "customer_service_anual_days_daily_or_weekly_or_weekends_365_261_104" will be truncated to "customer_service_anual_days_daily_or_weekly_or_weekends_365_261"
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:46: NOTICE:  identifier "expected_by_sla_annual_service_minutes_up_365_times_24_60_equals_525600" will be truncated to "expected_by_sla_annual_service_minutes_up_365_times_24_60_equal"
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:46: NOTICE:  identifier "service_debit_credit_anual_sla_minutes_in_positive_credit_or_negative_debit_more_than_sla" will be truncated to "service_debit_credit_anual_sla_minutes_in_positive_credit_or_ne"
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

INSERT INTO "cloud_service_risk_ratings".service_risk_ratings (database_key_id, service_name, service_provider, global_or_by_regions, region, availability_zone, service_load_at_customer_low_medium_high_very_high_1_2_3_4, customer_service_type_b2c_or_b2b_1_yes_0_no, customer_service_up_hours_8h_day_12h_day_24h_day, customer_service_anual_days_daily_or_weekly_or_weekends_365_261_104, service_sla_0_99_9999_for_60min_times_24h_365days, percentage_service_credit_back, webscraper_annual_period_service_down_per_year_in_minutes, annual_service_minutes_up_365_24_60_equals_525600, expected_by_sla_annual_service_minutes_up_365_times_24_60_equals_525600, expected_annual_service_minutes_down, service_debit_credit_anual_sla_minutes_in_positive_credit_or_negative_debit_more_than_sla, expected_percentage_mins_down_on_agreed_sla, actual_percentage_total_mins_down_from_webscraping, actual_percentage_mins_down_on_agreed_sla, gap_time_percent_between_SLA_down_actual_down, riskcoef_per_service_from_gap_expected_actual_time_down, service_sla_usage_percentage, service_traffic_coef_by_percent_down, sla_deviation_connected_risk_0_999, usage_connected_risk_0_999, annual_outage_time_days_hours_mins, remarks_outage_genai, public_locationa_and_status_genai, outages_other_impacted_services_genai, notes)
 VALUES (10000000000000, 'worst_possible_technology', 'the_bad_cloud', 'global', '', '', '4', '1', '24', '365', '99.990', '10.000', '520000', '525600.000', '525594.744', '5.256', '-519994.744', '0.00%', '98.93%', '98.93%', '-98.93%', '98.93%', '9893455.10%', '98.93%', '-98824.983', '-1966.068', '', '', '', '', '') ;

SELECT * FROM cloud_service_risk_ratings.service_risk_ratings;

