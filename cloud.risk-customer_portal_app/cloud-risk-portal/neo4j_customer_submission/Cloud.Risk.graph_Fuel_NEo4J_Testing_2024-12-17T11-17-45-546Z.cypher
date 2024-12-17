
CREATE (cust_sessionid_3_uQJWBpCnfHr9t6vXeK4F9jmjsUDctP_name_Fuel_NEo4J_Testing:CUSTOMER_NAME {
    name: 'Fuel NEo4J Testing',
    project_name: 'Fuel NEo4J Testing',
    median_sla_usage_percentage: '175.5063224%',
    median_sla_deviation_risk: '995.089',
    median_traffic_coefficient: '0.08770928463%',
    median_usage_risk: '995.59',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '461',
    submission_date: '2024-12-17T11:17:45.546Z'
})
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '175.5063224%',
    median_sla_deviation_risk: '995.871',
    median_traffic_coefficient: '0.08770928463%',
    median_usage_risk: '996.371',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '461'
})
CREATE (Google_Cloud_Compute_Engine:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Compute Engine',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '175.5063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08770928463%',
    usage_risk: '996.371',
    annual_downtime_minutes: '461.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_3_uQJWBpCnfHr9t6vXeK4F9jmjsUDctP_name_Fuel_NEo4J_Testing)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Compute_Engine)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.5063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08770928463%',
    usage_risk: '996.371'
}]->(Google_Cloud_Compute_Engine)
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '227.6632989%',
    median_sla_deviation_risk: '995.089',
    median_traffic_coefficient: '0.1137747336%',
    median_usage_risk: '995.59',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '598'
})
CREATE (Amazon_Elastic_Compute_Cloud:TECHNOLOGY_SERVICE {
    name: 'Amazon Elastic Compute Cloud',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '227.6632989%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.1137747336%',
    usage_risk: '995.590',
    annual_downtime_minutes: '598.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_3_uQJWBpCnfHr9t6vXeK4F9jmjsUDctP_name_Fuel_NEo4J_Testing)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Compute_Cloud)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '227.6632989%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.1137747336%',
    usage_risk: '995.590'
}]->(Amazon_Elastic_Compute_Cloud)