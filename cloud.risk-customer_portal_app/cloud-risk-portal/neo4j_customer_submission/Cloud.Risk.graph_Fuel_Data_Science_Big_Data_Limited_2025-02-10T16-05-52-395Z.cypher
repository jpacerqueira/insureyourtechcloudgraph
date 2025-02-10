
CREATE (cust_sessionid_yzqoSkAfCH94tjpk9kn_wXXvUEsARWoP_name_Fuel_Data_Science_Big_Data_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science Big Data Limited',
    project_name: 'Fuel Data Science Big Data Limited',
    median_sla_usage_percentage: '2245.30826005%',
    median_sla_deviation_risk: '973.7225000000001',
    median_traffic_coefficient: '0.25494672753000003%',
    median_usage_risk: '991.359',
    median_service_sla: '99.97%',
    median_annual_downtime_minutes: '1340',
    submission_date: '2025-02-10T16:05:52.396Z'
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
CREATE (Amazon_Route_53:TECHNOLOGY_SERVICE {
    name: 'Amazon Route 53',
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
CREATE (cust_sessionid_yzqoSkAfCH94tjpk9kn_wXXvUEsARWoP_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Route_53)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '152.2831431%',
    sla_deviation_risk: '996.219',
    traffic_coefficient: '0.07610350076%',
    usage_risk: '996.719'
}]->(Amazon_Route_53)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '4338.333377%',
    median_sla_deviation_risk: '951.226',
    median_traffic_coefficient: '0.4337899543%',
    median_usage_risk: '985.999',
    median_service_sla: '99.99%',
    median_annual_downtime_minutes: '2280'
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
CREATE (cust_sessionid_yzqoSkAfCH94tjpk9kn_wXXvUEsARWoP_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Functions)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_Functions)