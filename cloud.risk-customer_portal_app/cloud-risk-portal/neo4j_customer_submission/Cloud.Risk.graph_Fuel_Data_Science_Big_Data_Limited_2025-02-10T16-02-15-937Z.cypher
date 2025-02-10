
CREATE (cust_sessionid_QatQ2yACCaKngzqrIRug6GNuxAnErAbP_name_Fuel_Data_Science_Big_Data_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science Big Data Limited',
    project_name: 'Fuel Data Science Big Data Limited',
    median_sla_usage_percentage: '137.0548288%',
    median_sla_deviation_risk: '996.447',
    median_traffic_coefficient: '0.06849315068%',
    median_usage_risk: '996.947',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '360',
    submission_date: '2025-02-10T16:02:15.938Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '137.0548288%',
    median_sla_deviation_risk: '996.447',
    median_traffic_coefficient: '0.06849315068%',
    median_usage_risk: '996.947',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '360'
})
CREATE (Amazon_AWS_Glue:TECHNOLOGY_SERVICE {
    name: 'Amazon AWS Glue',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '137.0548288%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849315068%',
    usage_risk: '996.947',
    annual_downtime_minutes: '360.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_QatQ2yACCaKngzqrIRug6GNuxAnErAbP_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_AWS_Glue)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '137.0548288%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849315068%',
    usage_risk: '996.947'
}]->(Amazon_AWS_Glue)