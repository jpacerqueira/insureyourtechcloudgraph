
CREATE (cust_sessionid_bVCKvmLdWi_HSCpzTJQVJ3H5KNTbMjkU_name_Fuel:CUSTOMER_NAME {
    name: 'Fuel',
    project_name: 'Fuel',
    median_sla_usage_percentage: '137.0548288%',
    median_sla_deviation_risk: '0',
    median_traffic_coefficient: '0%',
    median_usage_risk: '967.917',
    median_service_sla: '99.95%',
    median_annual_downtime: '360',
    submission_date: '2024-12-13T12:44:58.060Z'
})
CREATE (Microsoft_Azure:TECHNOLOGY_PROVIDER {
    name: 'Microsoft Azure',
    vendor_median_sla_usage_percentage: '6914.694515%',
    vendor_median_sla_deviation_risk: '-6415.2375',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '483.9585',
    vendor_median_service_sla: '49.995%',
    vendor_median_annual_downtime: '3634'
})
CREATE (Azure_PowerBI:TECHNOLOGY_SERVICE {
    name: 'Azure PowerBI',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '13829.38903%',
    sla_deviation_risk: '-12830.475',
    traffic_coefficient: '0.34570%%',
    usage_risk: '967.917',
    annual_downtime_minutes: '7268.00',
    service_sla_tier1: '99.99000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_bVCKvmLdWi_HSCpzTJQVJ3H5KNTbMjkU_name_Fuel)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Azure_PowerBI)

CREATE (Microsoft_Azure)-[:CONNECTED_RISK {
    sla_usage: '13829.38903%',
    sla_deviation_risk: '-12830.475',
    traffic_coefficient: '0.34570%%',
    usage_risk: '967.917'
}]->(Azure_PowerBI)
CREATE (Amazon_AWS:TECHNOLOGY_PROVIDER {
    name: 'Amazon AWS',
    vendor_median_sla_usage_percentage: '68.5274144%',
    vendor_median_sla_deviation_risk: '430.449',
    vendor_median_traffic_coefficient: '0%',
    vendor_median_usage_risk: '498.4735',
    vendor_median_service_sla: '49.975%',
    vendor_median_annual_downtime: '180'
})
CREATE (Amazon_s3:TECHNOLOGY_SERVICE {
    name: 'Amazon s3',
    region: 'global',
    monthly_cost: 1000,
    sla_usage: '137.0548288%',
    sla_deviation_risk: '860.898',
    traffic_coefficient: '0.06849%%',
    usage_risk: '996.947',
    annual_downtime_minutes: '360.00',
    service_sla_tier1: '99.95000%',
    service_credit_back_tier1: '10.000%'
})
CREATE (cust_sessionid_bVCKvmLdWi_HSCpzTJQVJ3H5KNTbMjkU_name_Fuel)-[:CUSTOMER_USES_SERVICE {
    monthly_cost: 1000,
    region: 'global'
}]->(Amazon_s3)

CREATE (Amazon_AWS)-[:CONNECTED_RISK {
    sla_usage: '137.0548288%',
    sla_deviation_risk: '860.898',
    traffic_coefficient: '0.06849%%',
    usage_risk: '996.947'
}]->(Amazon_s3)