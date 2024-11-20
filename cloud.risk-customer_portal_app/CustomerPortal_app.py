import os
import requests
from dotenv import load_dotenv
import json
import re
import time

import streamlit as st
from neo4j import GraphDatabase
from flask import Flask
from flask_cors import CORS


# Initialize the Neo4j connection
def init_neo4j_connection(uri, user, password, max_retries=3):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver
    # TODO: remove this when connection works    
    #retry_count = 0
    #while retry_count < max_retries:
    #    try:
    #        driver = GraphDatabase.driver(uri, auth=(user, password))
    #        # Verify connection
    #        with driver.session() as session:
    #            session.run("MATCH (n) RETURN count(n) LIMIT 1")
    #        return driver
    #    except Exception as e:
    #        retry_count += 1
    #        st.warning(f"Attempt {retry_count}: Unable to connect to Neo4j. Retrying... ({str(e)})")
    #        time.sleep(2)  # Wait 2 seconds before retrying
    #st.error(f"Failed to connect to Neo4j after {max_retries} attempts. Please check your connection settings.")
    #return None


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

# Add sanitize function for Cypher node IDs
def sanitize_cypher_identifier(text):
    # Remove special characters and spaces, keep alphanumeric and underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', text)
    # Ensure it doesn't start with a number
    if sanitized[0].isdigit():
        sanitized = 'n' + sanitized
    return sanitized

# Streamlit app starts here
st.title("Cloud.Risk Graph - Customer Portal")
st.header("Customer Submission App")

# Add custom CSS to modify multiselect colors and page width
st.markdown("""
    <style>
    /* Set page width */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
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
uri = os.getenv("NEO4J_CLIENT_URI", "bolt://host.docker.internal:17687") # TODO: changed from "bolt://customer.risk.graph.neo4j:17687"
user = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

# Initialize Neo4j connection using environment variables
driver = init_neo4j_connection(uri, user, password)
#if not driver:
#    st.error("Unable to establish connection to Neo4j. Please check your configuration.")#
#    st.stop()

# Replace the existing form section with new cloud risk assessment form
st.subheader("New Cloud Risk Assessment")
st.subheader("Cloud.Risk.Graph - Analysis")

# Define services dictionary before using it
services = {
    "Amazon AWS": ["Amazon API Gateway","Amazon Bedrock","Amazon CloudFront","Amazon CloudWatch Application Insights","Amazon CodeGuru Profiler","Amazon DataZone",
        "Amazon DocumentDB","Amazon DynamoDB","Amazon EC2 Instance Connect","Amazon Elastic Compute Cloud","Amazon Elastic Container Service",
        "Amazon Elastic File System","Amazon Elastic Load Balancing","Amazon Elastic MapReduce","Amazon ElastiCache",
        "Amazon EMR Serverless","Amazon FinSpace","Amazon QuickSight","Amazon AWS Lambda","Amazon AWS CloudFront",
        "Amazon AWS Step Functions","Amazon s3","Amazon Elastic Kubernetes Service"],
    "Google Cloud GCP": ["Google Cloud VertexAI","Google Cloud Apigee API","Google Cloud Run","Google Cloud BigQuery","AlloyDB for PostgreSQL",
        "Google Cloud SQL","Google Cloud Compute Engine","Google Cloud Dataproc","Google Cloud Dataflow","Google Cloud Storage","Google Cloud And Media CDN",
        "Google Kubernetes Engine (GKE)"],
    "Microsoft Azure": ["Azure Batch","Azure functions","Azure PowerBi App","Azure CDN","Azure Storage Accounts","Azure Kubernetes Service (AKS)"],
    "IBM Cloud": ["IBM Dedicated Storage Instance","IBM Data Engine (previously SQL Query)","IBM Data Product Hub",
        "IBM Databases","IBM Databases for DataStax","IBM Databases for EDB",
        "IBM Databases for Elasticsearch","IBM Databases for etcd","IBM Databases for MongoDB",
        "IBM Databases for MySQL","IBM Databases for PostgreSQL","IBM Databases for Redis",
        "IBM DataStage","IBM Db2","IBM Db2 Warehouse","IBM watsonx BI Assistant",
        "IBM Dedicated Storage Instance","IBM Functions","IBM Cloud Object Storage","IBM Kubernetes",
        "Red Hat OpenShift on IBM Cloud"],
    "Oracle Cloud OCI": ["Oracle AutonomousDB 21c","autonomousdb_21c","Object Storage OIC","Oracle_Big_Data_Service","Oracle Kubernetes Service (OKE)"],
    "Snowflake": ["Snowflake on AWS","Snowflake on Azure","Snowflake on GCP"],
    "Databricks": ["Databricks","Databricks Workspace", "Databricks MLflow", "Databricks Notebooks"],
    "Salesforce": ["Salesforce SaaS","Salesforce Sales Cloud", "Salesforce Service Cloud", "Salesforce Marketing Cloud"],
    "MongoDB": [ "MongoDB Atlas", "MongoDB Atlas Search"],
    "Cloudflare": ["AnyCast CloudFlare","CDN CloudFlare", "Cloudflare DNS", "Cloudflare DDoS Protection"],
    "Akamai": ["CDN Akamai", "Edge Computing Akamai", "Security Akamai"],
    "Macrometa": ["CDN Macrometa", "Edge Computing Macrometa"]
}

# Company details
company_name = st.text_input("Company Name (required)")
project_name = st.text_input("Project Name (optional)", value="Project by "+company_name)

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
        
        # Initialize lists to store values for median calculation
        sla_usage_values = []
        sla_deviation_values = []
        traffic_coef_values = []
        usage_risk_values = []
        
        # Clean company name
        company_name = company_name.replace('\'', '.')
        # Clean project name
        project_name = project_name.replace('\'', '.')
        # Generate Cypher query with sanitized identifiers
        company_id = sanitize_cypher_identifier(company_name)
        cypher_query = f"""CREATE (cust_{company_id}:CUSTOMER_NAME {{
            name: '{company_name}',
            project_name: '{project_name}',
            median_sla_usage: 0,
            median_sla_deviation: 0,
            median_traffic_coefficient: 0,
            median_usage_risk: 0
        }})
"""
        
        # Create vendor nodes with sanitized IDs
        for vendor in selected_vendors:
            vendor_id = sanitize_cypher_identifier(vendor)
            cypher_query += f"CREATE ({vendor_id}:TECHNOLOGY_PROVIDER {{name: '{vendor}'}})\n"
        
        # Create service nodes and relationships with sanitized IDs
        for service in selected_services:
            service_id = sanitize_cypher_identifier(service)
            risk_data = fetch_cloud_risk_data(service, region_type)
            
            if risk_data:
                # Convert to float and remove % and ,
                sla_usage = float(risk_data.get('service_sla_usage_percentage', 0.0).rstrip('%').replace(',', '.'))
                sla_deviation = float(risk_data.get('sla_deviation_connected_risk_0_999', 0.0).rstrip('%').replace(',', '.'))
                traffic_coef = float(risk_data.get('service_traffic_coef_by_percent_down', 0.0).rstrip('%').replace(',', '.'))
                usage_risk = float(risk_data.get('usage_connected_risk_0_999', 0.0).rstrip('%').replace(',', '.'))
                
                # Append values to lists
                sla_usage_values.append(sla_usage)
                sla_deviation_values.append(sla_deviation)
                traffic_coef_values.append(traffic_coef)
                usage_risk_values.append(usage_risk)
                
                # Create service node
                cypher_query += f"""
CREATE ({service_id}:TECHNOLOGY_SERVICE {{
    name: '{service}',
    sla_usage: '{risk_data.get('service_sla_usage_percentage', 0.0)}',
    sla_deviation_risk: '{risk_data.get('sla_deviation_connected_risk_0_999', 0.0)}',
    traffic_coefficient: '{risk_data.get('service_traffic_coef_by_percent_down', 0.0)}',
    usage_risk: '{risk_data.get('usage_connected_risk_0_999', 0.0)}'
}})
"""
                # Find vendor for this service
                for vendor, vendor_services in services.items():
                    if service in vendor_services:
                        vendor_id = sanitize_cypher_identifier(vendor)
                        # Create relationships with sanitized IDs
                        cypher_query += f"""
CREATE (cust_{company_id})-[:CUSTOMER_USES_SERVICE]->({service_id})
CREATE ({vendor_id})-[:CONNECTED_RISK {{
    sla_usage: '{risk_data.get('service_sla_usage_percentage', 0.0)}',
    sla_deviation_risk: '{risk_data.get('sla_deviation_connected_risk_0_999', 0.0)}',
    traffic_coefficient: '{risk_data.get('service_traffic_coef_by_percent_down', 0.0)}',
    usage_risk: '{risk_data.get('usage_connected_risk_0_999', 0.0)}'
}}]->({service_id})
"""
        
        # Replace the mean calculation section with median calculation
        if valid_services_count > 0:
            # Calculate medians
            median_sla_usage = sorted(sla_usage_values)[len(sla_usage_values)//2]
            median_sla_deviation = sorted(sla_deviation_values)[len(sla_deviation_values)//2]
            median_traffic_coef = sorted(traffic_coef_values)[len(traffic_coef_values)//2]
            median_usage_risk = sorted(usage_risk_values)[len(usage_risk_values)//2]
            
            st.subheader("Overall Risk Analysis Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Median SLA Usage %", f"{median_sla_usage:.2f}")
                st.metric("Median SLA Deviation Risk", f"{median_sla_deviation:.2f}")
            with col2:
                st.metric("Median Traffic Coefficient %", f"{median_traffic_coef:.2f}")
                st.metric("Median Usage Risk Rating", f"{median_usage_risk:.2f}")
            
            # Update the customer node with median values
            cypher_query = cypher_query.replace(
                f"CREATE (cust_{company_id}:CUSTOMER_NAME {{",
                f"""CREATE (cust_{company_id}:CUSTOMER_NAME {{
                    median_sla_usage: {median_sla_usage:.2f},
                    median_sla_deviation: {median_sla_deviation:.2f},
                    median_traffic_coefficient: {median_traffic_coef:.2f},
                    median_usage_risk: {median_usage_risk:.2f},"""
            )

        # Save Cypher query to file
        output_path = "neo4j_customer_submission/New_-_Cloud.Risk.Graph_-_Submission.graph"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(cypher_query)
            
        st.success(f"Generated Cypher query saved to {output_path}")
        
        # Continue with existing risk analysis display
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
st.header("View your Cloud Risk Graphs")

# Get list of files from neo4j_customer_submission folder
submission_folder = "neo4j_customer_submission"
list_options = []
if os.path.exists(submission_folder):
    list_options = [f for f in os.listdir(submission_folder) if f.endswith('.graph')]

cloud_risk_list = st.query_params.get("cloud risk - assesments list", None)

if cloud_risk_list:
    f"## {cloud_risk_list} is a great choice! "
    st.image(f"https://placehold.co/200x100?text={cloud_risk_list}", caption=f"{cloud_risk_list}!")

else:
    selection = st.selectbox("Select:", list_options, index=None)
    if selection:
        # Read the Cypher query from the selected file
        file_path = os.path.join(submission_folder, selection)
        try:
            with open(file_path, 'r') as f:
                cypher_query = f.read()
                
            # Execute the Cypher query using the Neo4j driver
            with driver.session() as session:
                try:
                    result = session.run(cypher_query)
                    st.success(f"Successfully uploaded graph data for {selection}")
                except Exception as e:
                    st.error(f"Error executing Cypher query: {str(e)}")
                
            st.link_button(
                f"View Your Cloud Risk Graph - {selection}",
                url=f"http://localhost:17474/", # TODO: change to cloudriskgraph.insureyourtech.cloud:17474
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Interactive Explore Graph Risk data
st.subheader("Explore All Cloud Risk Graph - Records")
st.caption("Go to http://localhost:17474/  - Explore your Cloud Services Cloud.Risk.Graph . with Neo4J Browser") # TODO: change to cloudriskgraph.insureyourtech.cloud:17474

# Flask API
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:8504",
            "http://localhost:17474",
            "bolt://localhost:17687",
            "bolt://host.docker.internal:17687",
            "http://host.docker.internal:17474",
            "https://customerportal.cloudriskgraph.insureyourtech.cloud",
            "http://cloudriskgraph.insureyourtech.cloud:17474",
            "https://cloudriskgraph.insureyourtech.cloud:17474"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
        "expose_headers": ["Access-Control-Allow-Origin"],
        "supports_credentials": True
    }
})

# Add these decorators to handle CORS preflight requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
