
CREATE (cust_sessionid_JhtRMN0LCXWtxhg6sqb0a_uK97uDvCUa_name_InsureYourTech_Cloud:CUSTOMER_NAME {
    name: 'InsureYourTech.Cloud',
    project_name: 'InsureYourTech.Cloud',
    median_sla_usage_percentage: '913.6988586%',
    median_sla_deviation_risk: '984.809',
    median_traffic_coefficient: '0.2914764079%',
    median_usage_risk: '990.264',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '1532',
    submission_date: '2025-02-06T19:10:35.777Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '670.8072453%',
    median_sla_deviation_risk: '988.448',
    median_traffic_coefficient: '0.3352359209%',
    median_usage_risk: '988.951',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '1762'
})
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
CREATE (cust_sessionid_JhtRMN0LCXWtxhg6sqb0a_uK97uDvCUa_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
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
    median_sla_usage_percentage: '2740.000027%',
    median_sla_deviation_risk: '968.79',
    median_traffic_coefficient: '0.2739726027%',
    median_usage_risk: '990.789',
    median_service_sla: '99.99%',
    median_annual_downtime_minutes: '1440'
})
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
CREATE (cust_sessionid_JhtRMN0LCXWtxhg6sqb0a_uK97uDvCUa_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
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
    median_sla_usage_percentage: '533.3717087%',
    median_sla_deviation_risk: '990.508',
    median_traffic_coefficient: '0.2665525114%',
    median_usage_risk: '991.01',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '1401'
})
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
CREATE (cust_sessionid_JhtRMN0LCXWtxhg6sqb0a_uK97uDvCUa_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '533.3717087%',
    sla_deviation_risk: '990.508',
    traffic_coefficient: '0.2665525114%',
    usage_risk: '991.010'
}]->(Google_Kubernetes_Engine__GKE_)
CREATE (IBM_Cloud:TECHNOLOGY_PROVIDER {
    name: 'IBM Cloud',
    median_sla_usage_percentage: '913.6988586%',
    median_sla_deviation_risk: '984.809',
    median_traffic_coefficient: '0.4566210046%',
    median_usage_risk: '985.313',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '2400'
})
CREATE (IBM_Kubernetes:TECHNOLOGY_SERVICE {
    name: 'IBM Kubernetes',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313',
    annual_downtime_minutes: '2400.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_JhtRMN0LCXWtxhg6sqb0a_uK97uDvCUa_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(IBM_Kubernetes)

CREATE (IBM_Cloud)-[:CONNECTED_RISK {
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313'
}]->(IBM_Kubernetes)
CREATE (MongoDB:TECHNOLOGY_PROVIDER {
    name: 'MongoDB',
    median_sla_usage_percentage: '5829.819649%',
    median_sla_deviation_risk: '937.798',
    median_traffic_coefficient: '0.2914764079%',
    median_usage_risk: '990.264',
    median_service_sla: '99.995%',
    median_annual_downtime_minutes: '1532'
})
CREATE (MongoDB_Atlas:TECHNOLOGY_SERVICE {
    name: 'MongoDB Atlas',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '5829.819649%',
    sla_deviation_risk: '937.798',
    traffic_coefficient: '0.2914764079%',
    usage_risk: '990.264',
    annual_downtime_minutes: '1532.00',
    service_sla_tier1: '99.99500%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_JhtRMN0LCXWtxhg6sqb0a_uK97uDvCUa_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(MongoDB_Atlas)

CREATE (MongoDB)-[:CONNECTED_RISK {
    sla_usage: '5829.819649%',
    sla_deviation_risk: '937.798',
    traffic_coefficient: '0.2914764079%',
    usage_risk: '990.264'
}]->(MongoDB_Atlas)