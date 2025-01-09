
CREATE (cust_sessionid_I4n_C2jP855Umk8MGPV7OmCqysxir8xY_name_Joao:CUSTOMER_NAME {
    name: 'Joao',
    project_name: 'Joao',
    median_sla_usage_percentage: '157.993761%',
    median_sla_deviation_risk: '984.809',
    median_traffic_coefficient: '0.07895738204%',
    median_usage_risk: '985.313',
    median_service_sla: '99.95%',
    median_annual_downtime_minutes: '415',
    submission_date: '2025-01-09T13:21:39.218Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    median_sla_usage_percentage: '78.9968805%',
    median_sla_deviation_risk: '498.0665',
    median_traffic_coefficient: '0.03947869102%',
    median_usage_risk: '498.3165',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '207.5'
})
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
CREATE (cust_sessionid_I4n_C2jP855Umk8MGPV7OmCqysxir8xY_name_Joao)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_AWS_Lambda)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '157.993761%',
    sla_deviation_risk: '996.133',
    traffic_coefficient: '0.07895738204%',
    usage_risk: '996.633'
}]->(Amazon_AWS_Lambda)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    median_sla_usage_percentage: '456.8494293%',
    median_sla_deviation_risk: '492.4045',
    median_traffic_coefficient: '0.2283105023%',
    median_usage_risk: '492.6565',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '1200'
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
CREATE (cust_sessionid_I4n_C2jP855Umk8MGPV7OmCqysxir8xY_name_Joao)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313'
}]->(Google_Kubernetes_Engine__GKE_)