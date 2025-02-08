
CREATE (cust_sessionid_VLLKptkxJfmgYsuE5HWNtxI_w_P0_QDn_name_Fuel_Data_Science_Big_Data_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science Big Data Limited',
    project_name: 'Fuel Data Science Big Data Limited',
    median_sla_usage_percentage: '677.1975353%',
    median_sla_deviation_risk: '987.0185',
    median_traffic_coefficient: '0.44682267880000004%',
    median_usage_risk: '985.6055',
    median_service_sla: '99.92500000000001%',
    median_annual_downtime_minutes: '2348.5',
    submission_date: '2025-02-06T17:32:11.657Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '920.1708921%',
    median_sla_deviation_risk: '984.712',
    median_traffic_coefficient: '0.4598554033%',
    median_usage_risk: '985.216',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '2417'
})
CREATE (Amazon_API_Gateway:TECHNOLOGY_SERVICE {
    name: 'Amazon API Gateway',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '920.1708921%',
    sla_deviation_risk: '984.712',
    traffic_coefficient: '0.4598554033%',
    usage_risk: '985.216',
    annual_downtime_minutes: '2417.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_VLLKptkxJfmgYsuE5HWNtxI_w_P0_QDn_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_API_Gateway)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '920.1708921%',
    sla_deviation_risk: '984.712',
    traffic_coefficient: '0.4598554033%',
    usage_risk: '985.216'
}]->(Amazon_API_Gateway)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '434.2241785%',
    median_sla_deviation_risk: '989.325',
    median_traffic_coefficient: '0.4337899543%',
    median_usage_risk: '985.995',
    median_service_sla: '99.9%',
    median_annual_downtime_minutes: '2280'
})
CREATE (Azure_Databricks:TECHNOLOGY_SERVICE {
    name: 'Azure Databricks',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '434.2241785%',
    sla_deviation_risk: '989.325',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.995',
    annual_downtime_minutes: '2280.00',
    service_sla_tier1: '99.90000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_VLLKptkxJfmgYsuE5HWNtxI_w_P0_QDn_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Databricks)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '434.2241785%',
    sla_deviation_risk: '989.325',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.995'
}]->(Azure_Databricks)