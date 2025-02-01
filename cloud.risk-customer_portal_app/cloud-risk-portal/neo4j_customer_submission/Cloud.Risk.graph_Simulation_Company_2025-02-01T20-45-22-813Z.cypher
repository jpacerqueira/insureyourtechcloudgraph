
CREATE (cust_sessionid_JZQlKm8tACrXulsRtHizMm_eGdZuNa9A_name_Simulation_Company:CUSTOMER_NAME {
    name: 'Simulation Company',
    project_name: 'Simulation Company',
    median_sla_usage_percentage: '170.5571203%',
    median_sla_deviation_risk: '995.9445000000001',
    median_traffic_coefficient: '0.08523592085500001%',
    median_usage_risk: '996.4449999999999',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '448',
    submission_date: '2025-02-01T20:45:22.813Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '170.5571203%',
    median_sla_deviation_risk: '995.9445000000001',
    median_traffic_coefficient: '0.08523592085500001%',
    median_usage_risk: '996.4449999999999',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '448'
})
CREATE (Amazon_s3:TECHNOLOGY_SERVICE {
    name: 'Amazon s3',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '183.1204796%',
    sla_deviation_risk: '995.756',
    traffic_coefficient: '0.09151445967%',
    usage_risk: '996.257',
    annual_downtime_minutes: '481.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_JZQlKm8tACrXulsRtHizMm_eGdZuNa9A_name_Simulation_Company)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_s3)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '183.1204796%',
    sla_deviation_risk: '995.756',
    traffic_coefficient: '0.09151445967%',
    usage_risk: '996.257'
}]->(Amazon_s3)
CREATE (Amazon_AWS_Lambda:TECHNOLOGY_SERVICE {
    name: 'Amazon AWS Lambda',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '157.993761%',
    sla_deviation_risk: '996.133',
    traffic_coefficient: '0.07895738204%',
    usage_risk: '996.633',
    annual_downtime_minutes: '415.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_JZQlKm8tACrXulsRtHizMm_eGdZuNa9A_name_Simulation_Company)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_AWS_Lambda)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '157.993761%',
    sla_deviation_risk: '996.133',
    traffic_coefficient: '0.07895738204%',
    usage_risk: '996.633'
}]->(Amazon_AWS_Lambda)