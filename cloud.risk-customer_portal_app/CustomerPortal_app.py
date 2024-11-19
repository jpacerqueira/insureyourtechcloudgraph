import os
import requests
from dotenv import load_dotenv
import json

import streamlit as st
from neo4j import GraphDatabase
from flask import Flask
from flask_cors import CORS


# Initialize the Neo4j connection
def init_neo4j_connection(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

# Neo4j insert function
def insert_record(driver, node_type, properties):
    with driver.session() as session:
        query = f"CREATE (n:{node_type} $properties) RETURN n"
        result = session.run(query, properties=properties)
        return result.single()

# Fetch distinct node labels for dropdown
def fetch_labels(driver):
    with driver.session() as session:
        result = session.run("CALL db.labels()")
        labels = [record["label"] for record in result]
    return labels

# Fetch nodes by type
def fetch_nodes_by_label(driver, label):
    with driver.session() as session:
        query = f"MATCH (n:{label}) RETURN n"
        result = session.run(query)
        return [record["n"] for record in result]

# Add new API endpoint function
def fetch_cloud_risk_data(service_name, region_type):
    try:
        api_url = f"http://node-api:8000/cloud-services-risk-ratings/risk-ratings-freemium/freemium/fetch/service/service_name/{service_name}/global_or_by_regions/{region_type}"
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching cloud risk data: {str(e)}")
        return None

# Streamlit app starts here
st.title("Cloud.Risk ")
st.header("Customer Portal App")

# Add custom CSS to modify multiselect colors and page width
st.markdown("""
    <style>
    /* Set page width */
    .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Change the color of selected items in multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #808080 !important;
    }
    
    /* Change the color of selected item in selectbox */
    .stSelectbox [data-baseweb="tag"] {
        background-color: #808080 !important;
    }
    </style>
""", unsafe_allow_html=True)

#Obtain Environment Variables
load_dotenv(".env")

# Replace the connection input fields with environment variables
uri = os.getenv("NEO4J_URI", "bolt://localhost:17687")
user = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j connection using environment variables
driver = init_neo4j_connection(uri, user, password)

# Replace the existing form section with new cloud risk assessment form
st.subheader("New Cloud Risk Assessment")
st.subheader("Cloud Service Risk Analysis")

# Define services dictionary before using it
services = {
    "Amazon AWS": ["Amazon API Gateway","Amazon Bedrock","Amazon CloudFront","Amazon CloudWatch Application Insights","Amazon CodeGuru Profiler","Amazon DataZone",
        "Amazon DocumentDB","Amazon DynamoDB","Amazon EC2 Instance Connect","Amazon Elastic Compute Cloud","Amazon Elastic Container Service",
        "Amazon Elastic File System","Amazon Elastic Load Balancing","Amazon Elastic MapReduce","Amazon ElastiCache",
        "Amazon EMR Serverless","Amazon FinSpace","Amazon QuickSight","Amazon AWS Lambda","Amazon AWS CloudFront",
        "Amazon AWS Step Functions","Amazon s3","Amazon Elastic Kubernetes Service"],
    "Google Cloud GCP": ["Google Cloud VertexAI","Google Cloud Apigee","Google Cloud BigQuery","AlloyDB for PostgreSQL",
        "Google Cloud Dataproc","Google Cloud Dataflow","Google Cloud Storage","Google Cloud And Media CDN",
        "Google Kubernetes Engine (GKE)"],
    "Microsoft Azure": ["Azure Batch","Azure functions","PowerBi App","Azure CDN","Azure Storage Accounts","Azure Kubernetes Service (AKS)"],
    "IBM Cloud": ["IBM Dedicated Storage Instance","IBM Data Engine (previously SQL Query)","IBM Data Product Hub",
        "IBM Databases","IBM Databases for DataStax","IBM Databases for EDB",
        "IBM Databases for Elasticsearch","IBM Databases for etcd","IBM Databases for MongoDB",
        "IBM Databases for MySQL","IBM Databases for PostgreSQL","IBM Databases for Redis",
        "IBM DataStage","IBM Db2","IBM Db2 Warehouse","IBM watsonx BI Assistant",
        "IBM Dedicated Storage Instance","IBM Functions","IBM Cloud Object Storage","IBM Kubernetes",
        "Red Hat OpenShift on IBM Cloud"],
    "Oracle Cloud OCI": ["Oracle AutonomousDB 21c","autonomousdb_21c","Object Storage OIC","Oracle_Big_Data_Service","Oracle Kubernetes Service (OKE)"],
    "Snowflake": ["Snowflake on AWS","Snowflake on Azure","Snowflake on GCP"],
    "Databricks": ["Databricks","Workspace", "MLflow", "Delta Lake"],
    "Salesforce": ["Salesforce SaaS","Sales Cloud", "Service Cloud", "Marketing Cloud"],
    "MongoDB": [ "MongoDB Atlas"],
    "Cloudflare": ["AnyCast CloudFlare","CDN CloudFlare", "DNS", "DDoS Protection"],
    "Akamai": ["CDN Akamai", "Edge Computing", "Security"]
}

# Company details
company_name = st.text_input("Company Name (required)")
project_name = st.text_input("Project Name (optional)", value=company_name)

# Cloud service selection - modified to accept multiple vendors
cloud_vendors = ["Amazon AWS", "Google Cloud GCP", "Microsoft Azure", "IBM Cloud", "Oracle Cloud OCI", 
                "Snowflake", "Databricks", "Salesforce", "MongoDB", "Cloudflare", "Akamai"]
selected_vendors = st.multiselect("Select Cloud Vendors (up to 6)", cloud_vendors, max_selections=6)

# Service selection based on vendors - modified to show services for all selected vendors
all_available_services = []
for vendor in selected_vendors:
    all_available_services.extend(services.get(vendor, []))

selected_services = st.multiselect("Select Services (up to 50)", all_available_services, max_selections=50)

# Region type selection
region_type = st.selectbox("Select Region Type", ["global", "regional"])

# Analyze Cloud Risk - modified to handle multiple services
if st.button("Analyze Cloud Risk"):
    if company_name and selected_services and region_type:
        st.subheader("Risk Analysis Results")
        
        for service in selected_services:
            st.write(f"Analysis for {service}")
            risk_data = fetch_cloud_risk_data(service, region_type)
            if risk_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("SLA Usage %", risk_data.get("service_sla_usage_percentage", "N/A"))
                    st.metric("SLA Deviation Risk", risk_data.get("sla_deviation_connected_risk_0_999", "N/A"))
                
                with col2:
                    st.metric("Traffic Coefficient %", risk_data.get("service_traffic_coef_by_percent_down", "N/A"))
                    st.metric("Usage Risk Rating", risk_data.get("usage_connected_risk_0_999", "N/A"))
                
                st.text_area(f"AI Analysis - {service}", risk_data.get("remarks_outage_genai", "No analysis available"), height=100)
                st.divider()
    else:
        st.warning("Please fill in all required fields")

# VIEW Results -  from Application - Customer
# Insert record form
st.header("View your Cloud Risk Graphs")
list_options = ["CURRENT_Cloud_RISK_Meajurement_v3", "Cloud_RISK_Meajurement_2", "Cloud_RISK_Meajurement_1"]

cloud_risk_list = st.query_params.get("cloud risk - assesments list", None)

if cloud_risk_list:
    f"## {cloud_risk_list} is a great choice! "
    st.image(f"https://placehold.co/200x100?text={cloud_risk_list}", caption=f"{cloud_risk_list}!")

else:
    selection = st.selectbox("Select:", list_options, index=None)
    if selection:
        st.link_button(
            f"See Cloud Risk Graph - {selection}",
            url=f"http://cloudriskgraph.insureyourtech.cloud:17474/",
            use_container_width=True
        )

# Interactive Explore Graph Risk data
st.subheader("Explore All Cloud Risk Graph - Records")
st.caption("Go to http://cloudriskgraph.insureyourtech.cloud:17474/  - Explore your cloud services risk graph.")

# Fetch node labels for selection
#labels = fetch_labels(driver)
#selected_label = st.selectbox("Select Node Type", labels)

# Fetch and display nodes of the selected type
#if selected_label:
#    nodes = fetch_nodes_by_label(driver, selected_label)
#    for node in nodes:
#        st.write(node)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8504", "https://CustomerPortal.cloudriskgraph.insureyourtech.cloud"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
