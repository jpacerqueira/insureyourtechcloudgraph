# Cloud Insurance Risk Ratings API

## Overview

This API provides risk ratings for cloud providers based on various factors such as outages, security incidents, and compliance issues. It uses a combination of machine learning models and expert systems to generate risk ratings.

## Deployment

The API is deployed using Docker and Docker Compose. The `docker-compose.yml` file in the root directory will build and run the API container.

## Usage

To run the API, navigate to the root directory and run `docker compose up`. This will build and run the API container.

## API Endpoints

The API has the following endpoints:

- `GET /cloud-insurance-risk-ratings/risk-ratings`: Get the risk ratings for all cloud providers.
- `GET /cloud-insurance-risk-ratings/risk-ratings/{provider}`: Get the risk ratings for a specific cloud provider.
- `GET /cloud-insurance-risk-ratings/risk-ratings/{provider}/{metric}`: Get the risk ratings for a specific cloud provider and metric.


## Example Usage

To get the risk ratings for all cloud providers, you can make a GET request to the `/risk-ratings` endpoint.

```bash
curl http://localhost:3000/cloud-insurance-risk-ratings/risk-ratings
    ``` 

To get the risk ratings for a specific cloud provider, you can make a GET request to the `/cloud-insurance-risk-ratings/risk-ratings/{provider}` endpoint.

```bash
curl http://localhost:8000/cloud-insurance-risk-ratings/risk-ratings/aws
```


To get the risk ratings for a specific cloud provider and metric, you can make a GET request to the `/risk-ratings/{provider}/{metric}` endpoint.

```bash
curl http://localhost:3000/cloud-insurance-risk-ratings/risk-ratings/aws/outages
```

An Example of the CSV data can be found in the `csv-loader` directory.

```bash
 head -n 29 ../information/datamodel/cloud-risk-datamodel-services-sla-outage.csv > data/cloud_service_risk_ratings.csv
 docker compose up --build
```

To rebuild the API without running it, use the following command, option 3:

```bash
 bash -x build-api-cluster 3
```

Example of the CSV data can be found in the `csv-loader` directory.

```bash
 head -n 29 ../information/datamodel/cloud-risk-datamodel-services-sla-outage.csv > data/cloud_service_risk_ratings.csv
```

Example Output

```bash
curl http://localhost:3000/cloud-insurance-risk-ratings/fetch/id/10000000000001
```

```bash
curl -X GET http://localhost:3000/api/risk-ratings/fetch/id/10000000000000 
{"database_key_id_10000000000001":"10000000000000","service_name":"autonomousdb_21c","service_provider":"oci","region_or_global":"global","service_load_at_customer_low_medium_high_very_high_1_2_3_4":"3","customer_service_type_b2c_or_b2b_1_yes_0_no":"0","customer_service_up_hours_8h_day_12h_day_24h_day":"24","customer_service_anual_days_daily_or_weekly_or_weekends_365_261":"365","service_sla_0_99_9999_for_60min_times_24h_365days":"99.99","webscraper_annual_period_service_down_per_year_in_minutes":"360","annual_service_minutes_up_365_24_60_equals_525600":"525600.000","expected_by_sla_annual_service_minutes_up_365_times_24_60_equal":"525547.440","expected_annual_service_minutes_down":"52.560","service_debit_credit_anual_sla_minutes_in_positive_credit_or_ne":"-307.440","expected_percentage_mins_down_on_agreed_sla":"0.01%","actual_percentage_total_mins_down_from_webscraping":"0.07%","actual_percentage_mins_down_on_agreed_sla":"0.07%","gap_time_percent_between_sla_down_actual_down":"-0.06%","riskcoef_per_service_from_gap_expected_actual_time_down":"0.06%","service_sla_usage_percentage":"684.93%","service_traffic_coef_by_percent_down":"0.05%","sla_deviation_connected_risk_0_999":"991.373","usage_connected_risk_0_999":"997.118","notes":""}
```