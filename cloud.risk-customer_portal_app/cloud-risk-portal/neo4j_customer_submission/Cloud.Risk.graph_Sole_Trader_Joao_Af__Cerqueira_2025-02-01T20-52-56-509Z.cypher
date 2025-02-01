
CREATE (cust_sessionid_Zfa_PmkU9MtnCu_xINSHITgrAeeiKxNJ_name_Sole_Trader_Joao_Af__Cerqueira:CUSTOMER_NAME {
    name: 'Sole Trader Joao Af. Cerqueira',
    project_name: 'Sole Trader Joao Af. Cerqueira',
    median_sla_usage_percentage: '163.89473275%',
    median_sla_deviation_risk: '996.0450000000001',
    median_traffic_coefficient: '0.081906392695%',
    median_usage_risk: '996.5450000000001',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '430.5',
    submission_date: '2025-02-01T20:52:56.509Z'
})
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '163.89473275%',
    median_sla_deviation_risk: '996.0450000000001',
    median_traffic_coefficient: '0.081906392695%',
    median_usage_risk: '996.5450000000001',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '430.5'
})
CREATE (Google_Cloud_VertexAI:TECHNOLOGY_SERVICE {
    name: 'Google Cloud VertexAI',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719',
    annual_downtime_minutes: '400',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_Zfa_PmkU9MtnCu_xINSHITgrAeeiKxNJ_name_Sole_Trader_Joao_Af__Cerqueira)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_VertexAI)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719'
}]->(Google_Cloud_VertexAI)
CREATE (Google_Cloud_Run:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Run',
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
CREATE (cust_sessionid_Zfa_PmkU9MtnCu_xINSHITgrAeeiKxNJ_name_Sole_Trader_Joao_Af__Cerqueira)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Run)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.5063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08770928463%',
    usage_risk: '996.371'
}]->(Google_Cloud_Run)