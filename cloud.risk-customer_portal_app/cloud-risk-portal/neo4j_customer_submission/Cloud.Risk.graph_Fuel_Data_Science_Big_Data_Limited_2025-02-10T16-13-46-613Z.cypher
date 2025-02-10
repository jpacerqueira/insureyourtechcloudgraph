
CREATE (cust_sessionid_HiYezmlxI_MPhHKY8CKb63qFWnm_w1OR_name_Fuel_Data_Science_Big_Data_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science Big Data Limited',
    project_name: 'Fuel Data Science Big Data Limited',
    median_sla_usage_percentage: '152.2831431%',
    median_sla_deviation_risk: '996.219',
    median_traffic_coefficient: '0.07610350076%',
    median_usage_risk: '996.719',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '400',
    submission_date: '2025-02-10T16:13:46.613Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '152.2831431%',
    median_sla_deviation_risk: '996.219',
    median_traffic_coefficient: '0.07610350076%',
    median_usage_risk: '996.719',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '400'
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
CREATE (cust_sessionid_HiYezmlxI_MPhHKY8CKb63qFWnm_w1OR_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Bedrock)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719'
}]->(Amazon_Bedrock)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '4338.333377%',
    median_sla_deviation_risk: '951.226',
    median_traffic_coefficient: '0.4337899543%',
    median_usage_risk: '985.999',
    median_service_sla: '99.99%',
    median_annual_downtime_minutes: '2280'
})
CREATE (Azure_OpenAI_Service:TECHNOLOGY_SERVICE {
    name: 'Azure OpenAI Service',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999',
    annual_downtime_minutes: '2280.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_HiYezmlxI_MPhHKY8CKb63qFWnm_w1OR_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_OpenAI_Service)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_OpenAI_Service)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '152.2831431%',
    median_sla_deviation_risk: '996.219',
    median_traffic_coefficient: '0.07610350076%',
    median_usage_risk: '996.719',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '400'
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
CREATE (cust_sessionid_HiYezmlxI_MPhHKY8CKb63qFWnm_w1OR_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_VertexAI)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719'
}]->(Google_Cloud_VertexAI)