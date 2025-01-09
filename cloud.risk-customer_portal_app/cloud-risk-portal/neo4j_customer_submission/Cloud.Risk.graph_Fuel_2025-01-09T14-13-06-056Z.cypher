
CREATE (cust_sessionid_u_1KIiU4tHxw7GJLOZn0JLNBy_U85_fM_name_Fuel:CUSTOMER_NAME {
    name: 'Fuel',
    project_name: 'Fuel',
    median_sla_usage_percentage: '456.8494293%',
    median_sla_deviation_risk: '454.2855',
    median_traffic_coefficient: '0.2283105023%',
    median_usage_risk: '487.183',
    median_service_sla: '49.975%',
    median_annual_downtime_minutes: '1200',
    submission_date: '2025-01-09T14:13:06.056Z'
})
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
    monthly_cost: 668,
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313',
    annual_downtime_minutes: '2400.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_u_1KIiU4tHxw7GJLOZn0JLNBy_U85_fM_name_Fuel)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 668,
    region: 'global'
}]->(Google_Kubernetes_Engine__GKE_)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '913.6988586%',
    sla_deviation_risk: '984.809',
    traffic_coefficient: '0.4566210046%',
    usage_risk: '985.313'
}]->(Google_Kubernetes_Engine__GKE_)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    median_sla_usage_percentage: '4110.000041%',
    median_sla_deviation_risk: '454.2855',
    median_traffic_coefficient: '0.4109589041%',
    median_usage_risk: '487.183',
    median_service_sla: '49.995%',
    median_annual_downtime_minutes: '2160'
})
CREATE (Azure_Kubernetes_Service__AKS_:TECHNOLOGY_SERVICE {
    name: 'Azure Kubernetes Service (AKS)',
    region: 'global',
    monthly_cost: 650,
    sla_usage: '8220.000082%',
    sla_deviation_risk: '908.571',
    traffic_coefficient: '0.8219178082%',
    usage_risk: '974.366',
    annual_downtime_minutes: '4320.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_u_1KIiU4tHxw7GJLOZn0JLNBy_U85_fM_name_Fuel)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 650,
    region: 'global'
}]->(Azure_Kubernetes_Service__AKS_)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '8220.000082%',
    sla_deviation_risk: '908.571',
    traffic_coefficient: '0.8219178082%',
    usage_risk: '974.366'
}]->(Azure_Kubernetes_Service__AKS_)