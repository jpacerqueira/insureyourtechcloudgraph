
CREATE (cust_sessionid_ZrHcoZjivwDiclRyxqVnqsCynRqg03Ss_name_Fuel_DataScience_BigData:CUSTOMER_NAME {
    name: 'Fuel DataScience BigData',
    project_name: 'Project Simulation Part1',
    median_sla_usage_percentage: '41.11644864%',
    median_sla_deviation_risk: '997.245',
    median_traffic_coefficient: '0.02054794521%',
    median_usage_risk: '997.745',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '108',
    submission_date: '2024-12-15T22:28:31.258Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '20.55822432%',
    median_sla_deviation_risk: '498.942',
    median_traffic_coefficient: '0.010273972605%',
    median_usage_risk: '499.192',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '54'
})
CREATE (Amazon_QuickSight:TECHNOLOGY_SERVICE {
    name: 'Amazon QuickSight',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '41.11644864%',
    sla_deviation_risk: '997.884',
    traffic_coefficient: '0.02054794521%',
    usage_risk: '998.384',
    annual_downtime_minutes: '108.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_ZrHcoZjivwDiclRyxqVnqsCynRqg03Ss_name_Fuel_DataScience_BigData)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_QuickSight)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '41.11644864%',
    sla_deviation_risk: '997.884',
    traffic_coefficient: '0.02054794521%',
    usage_risk: '998.384'
}]->(Amazon_QuickSight)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '41.87786435%',
    median_sla_deviation_risk: '498.6225',
    median_traffic_coefficient: '0.02092846271%',
    median_usage_risk: '498.8725',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '110'
})
CREATE (Google_Cloud_DataStudio:TECHNOLOGY_SERVICE {
    name: 'Google Cloud DataStudio',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '83.7557287%',
    sla_deviation_risk: '997.245',
    traffic_coefficient: '0.04185692542%',
    usage_risk: '997.745',
    annual_downtime_minutes: '220.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_ZrHcoZjivwDiclRyxqVnqsCynRqg03Ss_name_Fuel_DataScience_BigData)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_DataStudio)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '83.7557287%',
    sla_deviation_risk: '997.245',
    traffic_coefficient: '0.04185692542%',
    usage_risk: '997.745'
}]->(Google_Cloud_DataStudio)