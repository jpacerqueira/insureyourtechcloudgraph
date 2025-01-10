
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud:CUSTOMER_NAME {
    name: 'InsureYourTechCloud',
    project_name: 'Test',
    median_sla_usage_percentage: '913.6988586%',
    median_sla_deviation_risk: '984.809',
    median_traffic_coefficient: '0.4337899543%',
    median_usage_risk: '985.999',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '2280',
    submission_date: '2025-01-10T17:56:02.027Z'
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
CREATE (Google_Kubernetes_Engine__GKE_:TECHNOLOGY_SERVICE {
    name: 'Google Kubernetes Engine (GKE)',
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
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313'
}]->(Google_Kubernetes_Engine__GKE_)
CREATE (Google_Cloud_Storage:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Storage',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '121.8265145%',
    sla_deviation_risk: '996.675',
    traffic_coefficient: '0.06088280061%',
    usage_risk: '997.175',
    annual_downtime_minutes: '320.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Storage)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '121.8265145%',
    sla_deviation_risk: '996.675',
    traffic_coefficient: '0.06088280061%',
    usage_risk: '997.175'
}]->(Google_Cloud_Storage)
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
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Compute_Engine)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '175.5063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08770928463%',
    usage_risk: '996.371'
}]->(Google_Cloud_Compute_Engine)
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '227.6632989%',
    median_sla_deviation_risk: '995.089',
    median_traffic_coefficient: '0.1137747336%',
    median_usage_risk: '995.59',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '598'
})
CREATE (Amazon_s3:TECHNOLOGY_SERVICE {
    name: 'Amazon s3',
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
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_s3)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '137.0548288%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849315068%',
    usage_risk: '996.947'
}]->(Amazon_s3)
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
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Compute_Cloud)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '227.6632989%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.1137747336%',
    usage_risk: '995.590'
}]->(Amazon_Elastic_Compute_Cloud)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '4338.333377%',
    median_sla_deviation_risk: '951.226',
    median_traffic_coefficient: '0.4337899543%',
    median_usage_risk: '985.999',
    median_service_sla: '99.99%',
    median_annual_downtime_minutes: '2280'
})
CREATE (Azure_Kubernetes_Service__AKS_:TECHNOLOGY_SERVICE {
    name: 'Azure Kubernetes Service (AKS)',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '8220.000082%',
    sla_deviation_risk: '908.571',
    traffic_coefficient: '0.8219178082%',
    usage_risk: '974.366',
    annual_downtime_minutes: '4320.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Kubernetes_Service__AKS_)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '8220.000082%',
    sla_deviation_risk: '908.571',
    traffic_coefficient: '0.8219178082%',
    usage_risk: '974.366'
}]->(Azure_Kubernetes_Service__AKS_)
CREATE (Azure_Storage_Accounts:TECHNOLOGY_SERVICE {
    name: 'Azure Storage Accounts',
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
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Storage_Accounts)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_Storage_Accounts)
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
CREATE (cust_sessionid_WQ1kGp_Ox9WlUmcydQBTYHIULrBP6W_7_name_InsureYourTechCloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Functions)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '4338.333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.4337899543%',
    usage_risk: '985.999'
}]->(Azure_Functions)