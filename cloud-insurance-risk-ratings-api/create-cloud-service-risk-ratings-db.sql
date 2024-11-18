CREATE DATABASE cloud_service_risk_ratings;
 \c cloud_service_risk_ratings;
CREATE TABLE service_risk_ratings (
    database_key_id_10000000000001 text,
    service_name text,
    service_provider text,
    region_or_global text,
    service_load_at_customer_low_medium_high_very_high_1_2_3_4 text,
    customer_service_type_b2c_or_b2b_1_yes_0_no text,
    customer_service_up_hours_8h_day_12h_day_24h_day text,
    customer_service_anual_days_daily_or_weekly_or_weekends_365_261 text,
    service_sla_0_99_9999_for_60min_times_24h_365days text,
    webscraper_annual_period_service_down_per_year_in_minutes text,
    annual_service_minutes_up_365_24_60_equals_525600 text,
    expected_by_sla_annual_service_minutes_up_365_times_24_60_equal text,
    expected_annual_service_minutes_down text,
    service_debit_credit_anual_sla_minutes_in_positive_credit_or_ne text,
    expected_percentage_mins_down_on_agreed_sla text,
    actual_percentage_total_mins_down_from_webscraping text,
    actual_percentage_mins_down_on_agreed_sla text,
    gap_time_percent_between_SLA_down_actual_down text,
    riskcoef_per_service_from_gap_expected_actual_time_down text,
    service_sla_usage_percentage text,
    Service_traffic_coef_by_percent_down text,
    SLA_Deviation_Connected_RISK_0_999 text ,
    USAGE_Connected_RISK_0_999 text,
    NOTES text
);

--
-- Truncated variable names
--
-- postgres-db  | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/create_database.sql
-- postgres-db  | CREATE DATABASE
-- postgres-db  | You are now connected to database "cloud_service_risk_ratings" as user "dbusername".
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:28: NOTICE:  identifier "customer_service_anual_days_daily_or_weekly_or_weekends_365_261_104" will be truncated to "customer_service_anual_days_daily_or_weekly_or_weekends_365_261"
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:28: NOTICE:  identifier "expected_by_sla_annual_service_minutes_up_365_times_24_60_equals_525600" will be truncated to "expected_by_sla_annual_service_minutes_up_365_times_24_60_equal"
-- postgres-db  | psql:/docker-entrypoint-initdb.d/create_database.sql:28: NOTICE:  identifier "service_debit_credit_anual_sla_minutes_in_positive_credit_or_negative_debit_more_than_sla" will be truncated to "service_debit_credit_anual_sla_minutes_in_positive_credit_or_ne"
-- postgres-db  | CREATE TABLE
--

SELECT session_user, current_database();

SELECT table_catalog, table_schema, table_name, column_name, column_default, is_nullable 
    FROM information_schema.columns 
    WHERE table_schema like '%'
    ORDER BY table_schema, table_name, ordinal_position;

SELECT * FROM pg_tables;

INSERT INTO service_risk_ratings
(database_key_id_10000000000001, service_name, service_provider, region_or_global, service_load_at_customer_low_medium_high_very_high_1_2_3_4, customer_service_type_b2c_or_b2b_1_yes_0_no, customer_service_up_hours_8h_day_12h_day_24h_day, customer_service_anual_days_daily_or_weekly_or_weekends_365_261, service_sla_0_99_9999_for_60min_times_24h_365days, webscraper_annual_period_service_down_per_year_in_minutes, annual_service_minutes_up_365_24_60_equals_525600, expected_by_sla_annual_service_minutes_up_365_times_24_60_equal, expected_annual_service_minutes_down, service_debit_credit_anual_sla_minutes_in_positive_credit_or_ne, expected_percentage_mins_down_on_agreed_sla, actual_percentage_total_mins_down_from_webscraping, actual_percentage_mins_down_on_agreed_sla, gap_time_percent_between_SLA_down_actual_down, riskcoef_per_service_from_gap_expected_actual_time_down, service_sla_usage_percentage, Service_traffic_coef_by_percent_down, SLA_Deviation_Connected_RISK_0_999, USAGE_Connected_RISK_0_999, NOTES)
 VALUES ('10000000000000', 'autonomousdb_21c', 'oci', 'global', '3', '0', '24', '365', '99.99', '360', '525600.000', '525547.440', '52.560', '-307.440', '0.01%', '0.07%', '0.07%', '-0.06%', '0.06%', '684.93%', '0.05%', '991.373', '997.118', '') ;
 
SELECT * FROM service_risk_ratings;
