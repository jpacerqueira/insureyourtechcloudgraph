
CREATE (cust_sessionid_J5C9nafVTFrkP2kF71aoJf3DuSCM5ZKy_name_Fuel_Data_Science_BigData_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science BigData Limited',
    project_name: 'Project to Insure Test Five',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '995.871',
    median_traffic_coefficient: '0%',
    median_usage_risk: '996.371',
    median_service_sla: '99.95%',
    median_annual_downtime: '461',
    submission_date: '2024-12-13T02:29:40.141Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    vendor_median_sla_usage_percentage: '0%',
    vendor_median_sla_deviation_risk: '995.6110000000001',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '996.1115',
    vendor_median_service_sla: '99.95%',
    vendor_median_annual_downtime: '506.5'
})
CREATE (Amazon_AWS_Lambda:TECHNOLOGY_SERVICE {
    name: 'Amazon AWS Lambda',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '157.99%%',
    sla_deviation_risk: '996.133',
    traffic_coefficient: '0.07896%%',
    usage_risk: '996.633',
    annual_downtime_minutes: '415.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_J5C9nafVTFrkP2kF71aoJf3DuSCM5ZKy_name_Fuel_Data_Science_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_AWS_Lambda)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '157.99%%',
    sla_deviation_risk: '996.133',
    traffic_coefficient: '0.07896%%',
    usage_risk: '996.633'
}]->(Amazon_AWS_Lambda)
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
CREATE (cust_sessionid_J5C9nafVTFrkP2kF71aoJf3DuSCM5ZKy_name_Fuel_Data_Science_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Compute_Cloud)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '227.66%%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.11377%%',
    usage_risk: '995.590'
}]->(Amazon_Elastic_Compute_Cloud)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    vendor_median_sla_usage_percentage: '0%',
    vendor_median_sla_deviation_risk: '995.871',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '996.371',
    vendor_median_service_sla: '99.95%',
    vendor_median_annual_downtime: '461'
})
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
CREATE (cust_sessionid_J5C9nafVTFrkP2kF71aoJf3DuSCM5ZKy_name_Fuel_Data_Science_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Run)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.51%%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371'
}]->(Google_Cloud_Run)
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
CREATE (cust_sessionid_J5C9nafVTFrkP2kF71aoJf3DuSCM5ZKy_name_Fuel_Data_Science_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Compute_Engine)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.51%%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371'
}]->(Google_Cloud_Compute_Engine)