
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited:CUSTOMER_NAME {
    name: 'Fuel DataScience BigData Limited',
    project_name: 'Project to Insure Part1',
    median_sla_usage_percentage: '218.9070182%',
    median_sla_deviation_risk: '995.089',
    median_traffic_coefficient: '0.1093987823%',
    median_usage_risk: '995.59',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '575',
    submission_date: '2024-12-15T22:24:08.056Z'
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
CREATE (Google_Cloud_SQL:TECHNOLOGY_SERVICE {
    name: 'Google Cloud SQL',
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
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_SQL)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.5063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08770928463%',
    usage_risk: '996.371'
}]->(Google_Cloud_SQL)
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
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Compute_Engine)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.5063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08770928463%',
    usage_risk: '996.371'
}]->(Google_Cloud_Compute_Engine)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '4338.333377%',
    median_sla_deviation_risk: '951.226',
    median_traffic_coefficient: '0.4337899543%',
    median_usage_risk: '985.999',
    median_service_sla: '99.99%',
    median_annual_downtime_minutes: '2280'
})
CREATE (Azure_Database_for_PostgreSQL:TECHNOLOGY_SERVICE {
    name: 'Azure Database for PostgreSQL',
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
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Database_for_PostgreSQL)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_Database_for_PostgreSQL)
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
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Functions)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_Functions)
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '218.9070182%',
    median_sla_deviation_risk: '995.089',
    median_traffic_coefficient: '0.1093987823%',
    median_usage_risk: '995.59',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '575'
})
CREATE (Amazon_AWS_RDS:TECHNOLOGY_SERVICE {
    name: 'Amazon AWS RDS',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '218.9070182%',
    sla_deviation_risk: '995.220',
    traffic_coefficient: '0.1093987823%',
    usage_risk: '995.721',
    annual_downtime_minutes: '575.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_AWS_RDS)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '218.9070182%',
    sla_deviation_risk: '995.220',
    traffic_coefficient: '0.1093987823%',
    usage_risk: '995.721'
}]->(Amazon_AWS_RDS)
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
CREATE (cust_sessionid_YJw_XravlgCAvOF7mU9jhTmv0oUopMou_name_Fuel_DataScience_BigData_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Compute_Cloud)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '227.6632989%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.1137747336%',
    usage_risk: '995.590'
}]->(Amazon_Elastic_Compute_Cloud)