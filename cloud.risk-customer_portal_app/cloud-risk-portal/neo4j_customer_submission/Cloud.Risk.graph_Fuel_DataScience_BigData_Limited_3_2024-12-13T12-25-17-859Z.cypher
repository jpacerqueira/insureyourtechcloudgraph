
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3:CUSTOMER_NAME {
    name: 'Fuel DataScience BigData Limited 3',
    project_name: 'Project to insure it now 3',
    median_sla_usage_percentage: '2.0158481065%',
    median_sla_deviation_risk: '995.48',
    median_traffic_coefficient: '0%',
    median_usage_risk: '995.9805',
    median_service_sla: '99.95%',
    median_annual_downtime: '529.5',
    submission_date: '2024-12-13T12:25:17.859Z'
})
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    vendor_median_sla_usage_percentage: '1.8235906384999998%',
    vendor_median_sla_deviation_risk: '995.768',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '996.2685',
    vendor_median_service_sla: '99.95%',
    vendor_median_annual_downtime: '479'
})
CREATE (Amazon_Elastic_Compute_Cloud:TECHNOLOGY_SERVICE {
    name: 'Amazon Elastic Compute Cloud',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '2.276632989%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.11377%%',
    usage_risk: '995.590',
    annual_downtime_minutes: '598.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_Elastic_Compute_Cloud)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '2.276632989%',
    sla_deviation_risk: '995.089',
    traffic_coefficient: '0.11377%%',
    usage_risk: '995.590'
}]->(Amazon_Elastic_Compute_Cloud)
CREATE (Amazon_s3:TECHNOLOGY_SERVICE {
    name: 'Amazon s3',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '1.370548288%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849%%',
    usage_risk: '996.947',
    annual_downtime_minutes: '360.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_s3)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '1.370548288%',
    sla_deviation_risk: '996.447',
    traffic_coefficient: '0.06849%%',
    usage_risk: '996.947'
}]->(Amazon_s3)
CREATE (Google_Cloud_GCP:TECHNOLOGY_PROVIDER {
    name: 'Google Cloud GCP',
    vendor_median_sla_usage_percentage: '1.4866641845%',
    vendor_median_sla_deviation_risk: '996.2729999999999',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '996.7729999999999',
    vendor_median_service_sla: '99.95%',
    vendor_median_annual_downtime: '390.5'
})
CREATE (Google_Cloud_Compute_Engine:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Compute Engine',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '1.755063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371',
    annual_downtime_minutes: '461.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Compute_Engine)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '1.755063224%',
    sla_deviation_risk: '995.871',
    traffic_coefficient: '0.08771%%',
    usage_risk: '996.371'
}]->(Google_Cloud_Compute_Engine)
CREATE (Google_Cloud_Storage:TECHNOLOGY_SERVICE {
    name: 'Google Cloud Storage',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '1.218265145%',
    sla_deviation_risk: '996.675',
    traffic_coefficient: '0.06088%%',
    usage_risk: '997.175',
    annual_downtime_minutes: '320.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Google_Cloud_Storage)

CREATE (Google_Cloud_GCP)-[:CONNECTED_RISK {
    sla_usage: '1.218265145%',
    sla_deviation_risk: '996.675',
    traffic_coefficient: '0.06088%%',
    usage_risk: '997.175'
}]->(Google_Cloud_Storage)
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    vendor_median_sla_usage_percentage: '43.38333377%',
    vendor_median_sla_deviation_risk: '951.226',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '985.999',
    vendor_median_service_sla: '99.99%',
    vendor_median_annual_downtime: '2280'
})
CREATE (Azure_Storage_Accounts:TECHNOLOGY_SERVICE {
    name: 'Azure Storage Accounts',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '43.38333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.43379%%',
    usage_risk: '985.999',
    annual_downtime_minutes: '2280.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Storage_Accounts)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '43.38333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.43379%%',
    usage_risk: '985.999'
}]->(Azure_Storage_Accounts)
CREATE (Azure_Batch:TECHNOLOGY_SERVICE {
    name: 'Azure Batch',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '43.38333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.43379%%',
    usage_risk: '985.999',
    annual_downtime_minutes: '2280.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_KfcxqnCoj3ob6K2U8Hz_Z81ZoxzVxIPV_name_Fuel_DataScience_BigData_Limited_3)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_Batch)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '43.38333377%',
    sla_deviation_risk: '951.226',
    traffic_coefficient: '0.43379%%',
    usage_risk: '985.999'
}]->(Azure_Batch)