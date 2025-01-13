
CREATE (cust_sessionid_pqC78Mo7zzTqnTH578ctzN1foLoyAlp__name_Sole_Trader_Joao_Af__Cerqueira:CUSTOMER_NAME {
    name: 'Sole Trader Joao Af. Cerqueira',
    project_name: 'Sole Trader Joao Af. Cerqueira',
    median_sla_usage_percentage: '0%',
    median_sla_deviation_risk: '0',
    median_traffic_coefficient: '0%',
    median_usage_risk: '0',
    median_service_sla: '0%',
    median_annual_downtime_minutes: '0',
    submission_date: '2025-01-13T11:39:51.547Z'
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
CREATE (cust_sessionid_pqC78Mo7zzTqnTH578ctzN1foLoyAlp__name_Sole_Trader_Joao_Af__Cerqueira)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313'
}]->(Google_Kubernetes_Engine__GKE_)