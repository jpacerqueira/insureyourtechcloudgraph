
CREATE (cust_sessionid_U1wxfNrga_e1_jyaESztrCBkRPFuMvTO_name_InsureYourTech_Cloud:CUSTOMER_NAME {
    name: 'InsureYourTech.Cloud',
    project_name: 'InsureYourTech.Cloud',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '0',
    median_traffic_coefficient: '0%',
    median_usage_risk: '0',
    median_service_sla: '0%',
    median_annual_downtime_minutes: '0',
    submission_date: '2025-01-14T21:26:26.149Z'
})
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '0',
    median_traffic_coefficient: '0%',
    median_usage_risk: '0',
    median_service_sla: '0%',
    median_annual_downtime_minutes: '0'
})
CREATE (Google_Cloud_Pub_Sub:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Pub/Sub',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '60.91325724%',
    sla_deviation_risk: '997.588',
    traffic_coefficient: '0.0304414003%',
    usage_risk: '998.088',
    annual_downtime_minutes: '160.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_U1wxfNrga_e1_jyaESztrCBkRPFuMvTO_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Pub_Sub)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '60.91325724%',
    sla_deviation_risk: '997.588',
    traffic_coefficient: '0.0304414003%',
    usage_risk: '998.088'
}]->(Google_Cloud_Pub_Sub)
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
CREATE (cust_sessionid_U1wxfNrga_e1_jyaESztrCBkRPFuMvTO_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313'
}]->(Google_Kubernetes_Engine__GKE_)
CREATE (Google_Cloud_reCAPTCHA_Enterprise:TECHNOLOGY_SERVICE {
    name: 'Google Cloud reCAPTCHA Enterprise',
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
CREATE (cust_sessionid_U1wxfNrga_e1_jyaESztrCBkRPFuMvTO_name_InsureYourTech_Cloud)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_reCAPTCHA_Enterprise)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '121.8265145%',
    sla_deviation_risk: '996.675',
    traffic_coefficient: '0.06088280061%',
    usage_risk: '997.175'
}]->(Google_Cloud_reCAPTCHA_Enterprise)