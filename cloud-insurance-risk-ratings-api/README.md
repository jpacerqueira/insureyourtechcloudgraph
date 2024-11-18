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
curl http://localhost:8000/cloud-insurance-risk-ratings/risk-ratings
    ``` 

To get the risk ratings for a specific cloud provider, you can make a GET request to the `/cloud-insurance-risk-ratings/risk-ratings/{provider}` endpoint.

```bash
curl http://localhost:8000/cloud-insurance-risk-ratings/risk-ratings/aws
```


To get the risk ratings for a specific cloud provider and metric, you can make a GET request to the `/risk-ratings/{provider}/{metric}` endpoint.

```bash
curl http://localhost:8000/cloud-insurance-risk-ratings/risk-ratings/aws/outages
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