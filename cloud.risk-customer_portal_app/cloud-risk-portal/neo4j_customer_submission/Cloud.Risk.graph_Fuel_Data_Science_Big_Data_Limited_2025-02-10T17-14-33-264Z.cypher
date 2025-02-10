
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited:CUSTOMER_NAME {
    name: 'Fuel Data Science Big Data Limited',
    project_name: 'Fuel Data Science Big Data Limited',
    median_sla_usage_percentage: '602.089477%',
    median_sla_deviation_risk: '989.4780000000001',
    median_traffic_coefficient: '0.23316210045000002%',
    median_usage_risk: '992.011',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '1225.5',
    submission_date: '2025-02-10T17:14:33.264Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '426.96386244999997%',
    median_sla_deviation_risk: '992.102',
    median_traffic_coefficient: '0.213375190285%',
    median_usage_risk: '992.604',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '1121.5'
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
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_s3)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '183.1204796%',
    sla_deviation_risk: '995.756',
    traffic_coefficient: '0.09151445967%',
    usage_risk: '996.257'
}]->(Amazon_s3)
CREATE (Amazon_Elastic_Kubernetes_Service__EKS_:TECHNOLOGY_SERVICE {
    name: 'Amazon Elastic Kubernetes Service (EKS)',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '670.8072453%',
    sla_deviation_risk: '988.448',
    traffic_coefficient: '0.3352359209%',
    usage_risk: '988.951',
    annual_downtime_minutes: '1762.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Kubernetes_Service__EKS_)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '670.8072453%',
    sla_deviation_risk: '988.448',
    traffic_coefficient: '0.3352359209%',
    usage_risk: '988.951'
}]->(Amazon_Elastic_Kubernetes_Service__EKS_)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '2035.9722425%',
    median_sla_deviation_risk: '976.5264999999999',
    median_traffic_coefficient: '0.2035768645%',
    median_usage_risk: '992.8985',
    median_service_sla: '99.99%',
    median_annual_downtime_minutes: '1070'
})
CREATE (Azure_Storage_Accounts:TECHNOLOGY_SERVICE {
    name: 'Azure Storage Accounts',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '1331.944458%',
    sla_deviation_risk: '984.263',
    traffic_coefficient: '0.1331811263%',
    usage_risk: '995.008',
    annual_downtime_minutes: '700.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Storage_Accounts)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '1331.944458%',
    sla_deviation_risk: '984.263',
    traffic_coefficient: '0.1331811263%',
    usage_risk: '995.008'
}]->(Azure_Storage_Accounts)
CREATE (Azure_Kubernetes_Service__AKS_:TECHNOLOGY_SERVICE {
    name: 'Azure Kubernetes Service (AKS)',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '2740.000027%',
    sla_deviation_risk: '968.790',
    traffic_coefficient: '0.2739726027%',
    usage_risk: '990.789',
    annual_downtime_minutes: '1440.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Kubernetes_Service__AKS_)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '2740.000027%',
    sla_deviation_risk: '968.790',
    traffic_coefficient: '0.2739726027%',
    usage_risk: '990.789'
}]->(Azure_Kubernetes_Service__AKS_)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '466.55747965%',
    median_sla_deviation_risk: '991.509',
    median_traffic_coefficient: '0.23316210045000002%',
    median_usage_risk: '992.011',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '1225.5'
})
CREATE (Google_Cloud_Storage:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Storage',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '399.7432506%',
    sla_deviation_risk: '992.510',
    traffic_coefficient: '0.1997716895%',
    usage_risk: '993.012',
    annual_downtime_minutes: '1050.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Storage)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '399.7432506%',
    sla_deviation_risk: '992.510',
    traffic_coefficient: '0.1997716895%',
    usage_risk: '993.012'
}]->(Google_Cloud_Storage)
CREATE (Google_Kubernetes_Engine__GKE_:TECHNOLOGY_SERVICE {
    name: 'Google Kubernetes Engine (GKE)',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '533.3717087%',
    sla_deviation_risk: '990.508',
    traffic_coefficient: '0.2665525114%',
    usage_risk: '991.010',
    annual_downtime_minutes: '1401.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_yBzdkr_K9tqAgj59933XwTwF0_wLmzbq_name_Fuel_Data_Science_Big_Data_Limited)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '533.3717087%',
    sla_deviation_risk: '990.508',
    traffic_coefficient: '0.2665525114%',
    usage_risk: '991.010'
}]->(Google_Kubernetes_Engine__GKE_)