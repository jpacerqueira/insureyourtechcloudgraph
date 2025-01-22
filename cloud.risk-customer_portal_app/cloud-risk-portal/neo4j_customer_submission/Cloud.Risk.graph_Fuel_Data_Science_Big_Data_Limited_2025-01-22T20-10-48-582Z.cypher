
CREATE (cust_sessionid_clN2vLBeh207eJFJcux1_ygOFwog_kC2_name_Fuel_Data_Science_Big_Data_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science Big Data Limited',
    project_name: 'Fuel Data Science Big Data Limited',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '0',
    median_traffic_coefficient: '0%',
    median_usage_risk: '0',
    median_service_sla: '0%',
    median_annual_downtime_minutes: '0',
    submission_date: '2025-01-22T20:10:48.582Z'
})
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '0',
    median_traffic_coefficient: '0%',
    median_usage_risk: '0',
    median_service_sla: '0%',
    median_annual_downtime_minutes: '0'
})
CREATE (Azure_Functions:TECHNOLOGY_SERVICE {
    name: 'Azure Functions',
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
CREATE (cust_sessionid_clN2vLBeh207eJFJcux1_ygOFwog_kC2_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Functions)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_Functions)