
CREATE (cust_sessionid_u8AMsACnDXhijN_2FhZkwK9GOoZpDlts_name_Fuel_Data_Science:CUSTOMER_NAME {
    name: 'Fuel Data Science',
    project_name: 'Test',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '995.871',
    median_traffic_coefficient: '0%',
    median_usage_risk: '996.371',
    median_service_sla: '99.95%',
    median_annual_downtime: '461',
    submission_date: '2024-12-13T11:00:44.943Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    vendor_median_sla_usage_percentage: '0%',
    vendor_median_sla_deviation_risk: '995.768',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '996.2685',
    vendor_median_service_sla: '99.95%',
    vendor_median_annual_downtime: '479'
})
CREATE (Amazon_Elastic_Compute_Cloud:TECHNOLOGY_SERVICE {
    name: 'Amazon Elastic Compute Cloud',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '227.66%%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.11377%%',
    usage_risk: '995.590',
    annual_downtime_minutes: '598.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_u8AMsACnDXhijN_2FhZkwK9GOoZpDlts_name_Fuel_Data_Science)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Compute_Cloud)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '227.66%%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.11377%%',
    usage_risk: '995.590'
}]->(Amazon_Elastic_Compute_Cloud)
CREATE (Amazon_s3:TECHNOLOGY_SERVICE {
    name: 'Amazon s3',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '137.05%%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849%%',
    usage_risk: '996.947',
    annual_downtime_minutes: '360.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_u8AMsACnDXhijN_2FhZkwK9GOoZpDlts_name_Fuel_Data_Science)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_s3)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '137.05%%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849%%',
    usage_risk: '996.947'
}]->(Amazon_s3)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    vendor_median_sla_usage_percentage: '0%',
    vendor_median_sla_deviation_risk: '995.871',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '996.371',
    vendor_median_service_sla: '99.95%',
    vendor_median_annual_downtime: '461'
})
CREATE (Google_Cloud_Compute_Engine:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Compute Engine',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '175.51%%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371',
    annual_downtime_minutes: '461.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_u8AMsACnDXhijN_2FhZkwK9GOoZpDlts_name_Fuel_Data_Science)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Compute_Engine)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.51%%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371'
}]->(Google_Cloud_Compute_Engine)
CREATE (Google_Cloud_Run:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Run',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '175.51%%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371',
    annual_downtime_minutes: '461.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_u8AMsACnDXhijN_2FhZkwK9GOoZpDlts_name_Fuel_Data_Science)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Run)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.51%%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371'
}]->(Google_Cloud_Run)