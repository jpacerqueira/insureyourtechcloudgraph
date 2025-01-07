
CREATE (cust_sessionid_Jgccmh3OZDKoMdZj30SeUVWZ9kMTzmYd_name_Fuel_DataScience_BigData:CUSTOMER_NAME {
    name: 'Fuel DataScience BigData',
    project_name: 'Test',
    median_sla_usage_percentage: '152.2831431%',
    median_sla_deviation_risk: '996.219',
    median_traffic_coefficient: '0.07610350076%',
    median_usage_risk: '996.719',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '400',
    submission_date: '2025-01-07T16:13:12.862Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '76.14157155%',
    median_sla_deviation_risk: '498.1095',
    median_traffic_coefficient: '0.03805175038%',
    median_usage_risk: '498.3595',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '200'
})
CREATE (Amazon_Bedrock:TECHNOLOGY_SERVICE {
    name: 'Amazon Bedrock',
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
CREATE (cust_sessionid_Jgccmh3OZDKoMdZj30SeUVWZ9kMTzmYd_name_Fuel_DataScience_BigData)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Bedrock)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719'
}]->(Amazon_Bedrock)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '76.14157155%',
    median_sla_deviation_risk: '498.1095',
    median_traffic_coefficient: '0.03805175038%',
    median_usage_risk: '498.3595',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '200'
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
CREATE (cust_sessionid_Jgccmh3OZDKoMdZj30SeUVWZ9kMTzmYd_name_Fuel_DataScience_BigData)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_VertexAI)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719'
}]->(Google_Cloud_VertexAI)