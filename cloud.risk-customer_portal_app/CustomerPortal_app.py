import os
import requests
from dotenv import load_dotenv
import json
import re
import time
import pandas as pd

import streamlit as st
from neo4j import GraphDatabase
from flask import Flask
from flask_cors import CORS


# Initialize the Neo4j connection
def init_neo4j_connection(uri, user, password, max_retries=3):
    # TODO: remove this when connection works    
    retry_count = 0
    while retry_count < max_retries:
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            # Verify connection
            with driver.session() as session:
                session.run("MATCH (n) RETURN count(n) LIMIT 1")
            return driver
        except Exception as e:
            retry_count += 1
            st.warning(f"Attempt {retry_count}: Unable to connect to Neo4j. Retrying... ({str(e)})")
            time.sleep(2)  # Wait 2 seconds before retrying
    st.error(f"Failed to connect to Neo4j after {max_retries} attempts. Please check your connection settings.")
    return None


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

# New function to fetch outage data for a specific service
def fetch_outage_data(service):
    try:
        api_url = f"http://node-api:8000/cloud-services-risk-ratings/risk-ratings-freemium/freemium/outages/service/{service}"
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching outage data for {service}: {str(e)}")
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
    "Amazon AWS": ["Amazon API Gateway","Amazon Bedrock","Amazon CloudFront","Amazon Route 53","Amazon CloudWatch Application Insights","Amazon CodeGuru Profiler","Amazon DataZone",
        "Amazon DocumentDB","Amazon DynamoDB","Amazon AWS RDS","Amazon AWS Aurora Serverles","Amazon EC2 Instance Connect","Amazon Elastic Compute Cloud","Amazon Elastic Container Service",
        "Amazon Elastic File System","Amazon Elastic Block Store","Amazon Elastic Load Balancing","Amazon Elastic MapReduce","Amazon ElastiCache",
        "Amazon EMR Serverless","Amazon FinSpace","Amazon QuickSight","Amazon AWS Lambda","Amazon AWS CloudFront",
        "Amazon AWS Step Functions","Amazon Redshift","Amazon AWS Glue","Amazon s3","Amazon Elastic Kubernetes Service"],
    "Google Cloud GCP": ["Google Cloud VertexAI","Google Cloud Machine Learning","Google Cloud Apigee API","Google Cloud Run","Google Cloud BigQuery","AlloyDB for PostgreSQL","Google Cloud SQL",
        "Google Cloud Bigtable","Google Cloud Compute Engine","Google Cloud Dataproc","Google Cloud Dataflow","Google Cloud Storage","Google Cloud DataStudio","Google Cloud Datalab","Google Cloud Composer","Google Cloud Looker Studio Pro","Google Cloud reCAPTCHA Enterprise",
        "Google Cloud Load Balancing","Google Cloud And Media CDN","Google Cloud DNS","Google Kubernetes Engine (GKE)"],
    "Microsoft Azure": ["Azure Active Directory AAD","Microsoft Entra ID","Azure Active Directory B2C",
                        "Azure Machine Learning","Azure AI","Azure AI Search","Azure OpenAI Service","Azure API Management","Azure Databricks",
                        "Azure SQL Managed Instance","Azure SQL Database","Azure Cosmos DB","Azure Database for PostgreSQL","Azure Database for MySQL",
                        "Azure Batch","Azure App Service","Azure Functions","Azure PowerBI","Azure CDN","Azure Storage Accounts","Azure Kubernetes Service (AKS)"],
    "IBM Cloud": ["IBM Watson Platform","IBM Dedicated Storage Instance","IBM Data Engine (previously SQL Query)","IBM Data Product Hub",
        "IBM Databases","IBM Databases for DataStax","IBM Databases for EDB",
        "IBM Databases for Elasticsearch","IBM Databases for etcd","IBM Databases for MongoDB",
        "IBM Databases for MySQL","IBM Databases for PostgreSQL","IBM Databases for Redis",
        "IBM DataStage","IBM Db2","IBM Db2 Warehouse","IBM watsonx BI Assistant",
        "IBM Dedicated Storage Instance","IBM Functions","IBM Cloud Object Storage","IBM Cloud Console","IBM Kubernetes",
        "Red Hat OpenShift on IBM Cloud"],
    "Oracle Cloud OCI": ["Oracle AutonomousDB 21c","Object Storage OCI","Oracle_Big_Data_Service","Oracle Kubernetes Service (OKE)"],
    "Snowflake": ["Snowflake on AWS","Snowflake on Azure","Snowflake on GCP"],
    "Databricks": ["Databricks SaaS","Databricks Workspace", "Databricks Mlflow", "Databricks Notebooks"],
    "Salesforce": ["Salesforce SaaS","Salesforce Sales Cloud", "Salesforce Service Cloud", "Salesforce Marketing Cloud","Salesforce Mulesoft Anypoint Platform"],
    "MongoDB": [ "MongoDB Atlas","MongoDB Atlas AWS","MongoDB Atlas Azure","MongoDB Atlas GCP","MongoDB Atlas Search","MongoDB Atlas Vector Search","MongoDB Atlas Stream Processing","MongoDB Atlas BI Connector","MongoDB Atlas SQL"],
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
max_vendor_selections = 10
selected_vendors = st.multiselect("Select Cloud Vendors (up to 10)", cloud_vendors, max_selections=max_vendor_selections) 

# Service selection based on vendors - modified to show services for all selected vendors
all_available_services = []
for vendor in selected_vendors:
    all_available_services.extend(services.get(vendor, []))

max_service_selections = 100
selected_services = st.multiselect("Select Services (up to 100)", all_available_services, max_selections=max_service_selections)

# Add monthly cost estimates for each selected service
service_costs = {}
if selected_services:
    st.subheader("Monthly Service Cost Estimates")
    cols = st.columns(3)  # Create 3 columns for better layout
    for idx, service in enumerate(selected_services):
        with cols[idx % 3]:
            service_costs[service] = st.number_input(
                f"Monthly cost estimate for {service} ($)",
                min_value=1.0,
                max_value=100000.0,
                value=1000.0,
                step=50.0,
                key=f"cost_{service}"
            )

# Region type selection
region_type = st.selectbox("Select Region Type", ["global", "regional"])

# Analyze Cloud Risk - modified to handle multiple services
if st.button("Analyze Cloud Risk"):
    if company_name and selected_services and region_type:
        st.header("Risk Analysis Results")
        
        # Initialize lists to store values for median calculation
        customer_sla_usage_values = []
        customer_sla_deviation_values = []
        customer_traffic_coef_values = []
        customer_usage_risk_values = []
        customer_service_sla_values = []
        customer_annual_downtime_values = []
        
        # Clean company name
        company_name = company_name.replace('\'', '.')
        # Clean project name
        project_name = project_name.replace('\'', '.')
        # Generate Cypher query with sanitized identifiers
        company_id = sanitize_cypher_identifier(company_name)
        cypher_query = ""
        # Create customer node
        # moved to end of script to allow for median calculation
            
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
                customer_sla_usage_values.append(sla_usage)
                customer_sla_deviation_values.append(sla_deviation)
                customer_traffic_coef_values.append(traffic_coef)
                customer_usage_risk_values.append(usage_risk)
                
                # Update these lines to use new API fields
                service_sla = float(risk_data.get('service_sla_0_99_9999_for_tier1', 0.0).rstrip('%').replace(',', '.'))
                service_credit_back = float(risk_data.get('percentage_service_credit_back_tier1', 0.0).rstrip('%').replace(',', '.'))
                annual_downtime = float(risk_data.get('webscraper_annual_period_service_down_per_year_in_minutes', 0.0))
                customer_service_sla_values.append(service_sla)
                customer_annual_downtime_values.append(annual_downtime)
                
                # Update service node creation
                cypher_query += f"""
CREATE ({service_id}:TECHNOLOGY_SERVICE {{
    name: '{service}',
    sla_usage: '{risk_data.get('service_sla_usage_percentage', 0.0)}',
    sla_deviation_risk: '{risk_data.get('sla_deviation_connected_risk_0_999', 0.0)}',
    traffic_coefficient: '{risk_data.get('service_traffic_coef_by_percent_down', 0.0)}',
    usage_risk: '{risk_data.get('usage_connected_risk_0_999', 0.0)}',
    annual_downtime_minutes: '{risk_data.get('webscraper_annual_period_service_down_per_year_in_minutes', 0.0)}',
    service_sla_tier1: '{risk_data.get('service_sla_0_99_9999_for_tier1', 0.0)}',
    service_credit_back_tier1: '{risk_data.get('percentage_service_credit_back_tier1', 0.0)}'
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

        # Initialize dictionaries to store values per vendor
        vendor_metrics = {vendor: {
            'sla_usage': [],
            'sla_deviation': [],
            'traffic_coef': [],
            'usage_risk': [],
            'service_sla': [],
            'annual_downtime': []
        } for vendor in selected_vendors}
        
        # Collect metrics per vendor
        for service in selected_services:
            risk_data = fetch_cloud_risk_data(service, region_type)
            if risk_data:
                # Find vendor for this service
                for vendor, vendor_services in services.items():
                    if service in vendor_services and vendor in selected_vendors:
                        # Add annual downtime to vendor metrics
                        annual_downtime = float(risk_data.get('webscraper_annual_period_service_down_per_year_in_minutes', 0.0))
                        vendor_metrics[vendor].setdefault('annual_downtime', []).append(annual_downtime)
                        
                        # Convert to float and remove % and ,
                        sla_usage = float(risk_data.get('service_sla_usage_percentage', 0.0).rstrip('%').replace(',', '.'))
                        sla_deviation = float(risk_data.get('sla_deviation_connected_risk_0_999', 0.0).rstrip('%').replace(',', '.'))
                        traffic_coef = float(risk_data.get('service_traffic_coef_by_percent_down', 0.0).rstrip('%').replace(',', '.'))
                        usage_risk = float(risk_data.get('usage_connected_risk_0_999', 0.0).rstrip('%').replace(',', '.'))
                        # Add service_sla to vendor metrics
                        service_sla = float(risk_data.get('service_sla_0_99_9999_for_tier1', 0.0).rstrip('%').replace(',', '.'))
                        vendor_metrics[vendor].setdefault('service_sla', []).append(service_sla)
                        
                        vendor_metrics[vendor]['sla_usage'].append(sla_usage)
                        vendor_metrics[vendor]['sla_deviation'].append(sla_deviation)
                        vendor_metrics[vendor]['traffic_coef'].append(traffic_coef)
                        vendor_metrics[vendor]['usage_risk'].append(usage_risk)
        
        # Calculate and display vendor medians
        st.divider()
        st.subheader("by Cloud Vendor")
        for vendor in selected_vendors:
            metrics = vendor_metrics[vendor]
            if any(metrics.values()):
                vendor_id = sanitize_cypher_identifier(vendor)
                
                # Calculate medians including annual downtime
                vendor_median_annual_downtime = sorted(metrics['annual_downtime'])[len(metrics['annual_downtime'])//2] if metrics['annual_downtime'] else 0.0
                
                # Calculate medians including service_sla
                vendor_median_sla = sorted(metrics['service_sla'])[len(metrics['service_sla'])//2] if metrics['service_sla'] else 0.0
                vendor_median_sla_usage = sorted(metrics['sla_usage'])[len(metrics['sla_usage'])//2] if metrics['sla_usage'] else 0.0
                vendor_median_sla_deviation = sorted(metrics['sla_deviation'])[len(metrics['sla_deviation'])//2] if metrics['sla_deviation'] else 0.0
                vendor_median_traffic_coef = sorted(metrics['traffic_coef'])[len(metrics['traffic_coef'])//2] if metrics['traffic_coef'] else 0.0
                vendor_median_usage_risk = sorted(metrics['usage_risk'])[len(metrics['usage_risk'])//2] if metrics['usage_risk'] else 0.0
                
                # Display vendor metrics
                st.write(f"### {vendor} Metrics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Median SLA Usage %", f"{vendor_median_sla_usage:.2f}%")
                    st.metric("Rating Median Cloud.Risk SLA Deviation", f"{vendor_median_sla_deviation:.2f}")
                with col2:
                    st.metric("Median Traffic Coefficient %", f"{vendor_median_traffic_coef:.2f}%")
                    st.metric("Rating Median Cloud.Risk Usage Risk", f"{vendor_median_usage_risk:.2f}")
                with col3:
                    st.metric("Median Service SLA %", f"{vendor_median_sla:.2f}%")
                    st.metric("Median Annual Downtime (minutes)", f"{vendor_median_annual_downtime:.2f}")
                st.divider()

                # Update vendor node creation in Cypher query to include annual downtime
                cypher_query = f"""CREATE ({vendor_id}:TECHNOLOGY_PROVIDER {{
                    name: '{vendor}',
                    vendor_median_sla_usage_percentage: '{vendor_median_sla_usage:.2f}%',
                    vendor_median_sla_deviation_risk: '{vendor_median_sla_deviation:.2f}',
                    vendor_median_traffic_coefficient: '{vendor_median_traffic_coef:.2f}%',
                    vendor_median_usage_risk: '{vendor_median_usage_risk:.2f}',
                    vendor_median_service_sla: '{vendor_median_sla:.2f}%',
                    vendor_median_annual_downtime: '{vendor_median_annual_downtime:.2f}'
                }})\n""" + cypher_query

        if customer_sla_usage_values and customer_sla_deviation_values and customer_traffic_coef_values and customer_usage_risk_values:
            # Calculate medians
            customer_median_sla_usage = sorted(customer_sla_usage_values)[len(customer_sla_usage_values)//2]
            customer_median_sla_deviation = sorted(customer_sla_deviation_values)[len(customer_sla_deviation_values)//2]
            customer_median_traffic_coef = sorted(customer_traffic_coef_values)[len(customer_traffic_coef_values)//2]
            customer_median_usage_risk = sorted(customer_usage_risk_values)[len(customer_usage_risk_values)//2]
            customer_median_service_sla = sorted(customer_service_sla_values)[len(customer_service_sla_values)//2]
            customer_median_annual_downtime = sorted(customer_annual_downtime_values)[len(customer_annual_downtime_values)//2]

            st.header("Customer Summary")           
            st.subheader("Overall Cloud Risk Analysis")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Median SLA Usage %", f"{customer_median_sla_usage:.2f}%")
                st.metric("Rating Median Cloud.Risk SLA Deviation", f"{customer_median_sla_deviation:.2f}")
            with col2:
                st.metric("Median Traffic Coefficient %", f"{customer_median_traffic_coef:.2f}%")
                st.metric("Rating Median Cloud.Risk Usage Risk", f"{customer_median_usage_risk:.2f}")
            with col3:
                st.metric("Median Service SLA %", f"{customer_median_service_sla:.2f}%")
                st.metric("Median Annual Downtime (minutes)", f"{customer_median_annual_downtime:.2f}")

            # Update customer node creation with new median values
            cypher_query = f"""
CREATE (cust_{company_id}:CUSTOMER_NAME {{
    name: '{company_name}',
    project_name: '{project_name}',
    median_sla_usage_percentage: '{customer_median_sla_usage:.2f}%',
    median_sla_deviation_risk: '{customer_median_sla_deviation:.2f}',
    median_traffic_coefficient: '{customer_median_traffic_coef:.2f}%',
    median_usage_risk: '{customer_median_usage_risk:.2f}',
    median_service_sla: '{customer_median_service_sla:.2f}%',
    median_annual_downtime: '{customer_median_annual_downtime:.2f}'
    }})
""" + cypher_query
        else:
            # Create vendor nodes with sanitized IDs
            for vendor in selected_vendors:
                vendor_id = sanitize_cypher_identifier(vendor)
                cypher_query = f"""CREATE ({vendor_id}:TECHNOLOGY_PROVIDER {{name: '{vendor}',
                  vendor_median_sla_usage_percentage: '0.0',
                  vendor_median_sla_deviation_risk: '0.0',
                  vendor_median_traffic_coefficient: '0.0',
                  vendor_median_usage_risk: '0.0'
                  }})
                  """ + cypher_query
            # 
            # Create customer node with default median values
            cypher_query =  f"""
CREATE (cust_{company_id}:CUSTOMER_NAME {{
    name: '{company_name}',
    project_name: '{project_name}',
    median_sla_usage_percentage: '0.0',
    median_sla_deviation_risk: '0.0',
    median_traffic_coefficient: '0.0',
    median_usage_risk: '0.0'
    }})
""" + cypher_query
            
        # Save Cypher query to file
        output_path = "neo4j_customer_submission/New     Cloud.Risk    .graph"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(cypher_query)

        st.success(f"Generated Cypher query saved to {output_path}")
        st.divider()

        st.header("Individual Cloud Services Risk Analysis")
        st.subheader("by Cloud Services")

        # Store the toggle state in session state if it doesn't exist
        if 'expand_all' not in st.session_state:
            st.session_state.expand_all = False

        # Add a single toggle button for all services
        show_all = False
        # show_all = st.button("Show/Hide All Services Analysis") # TODO: change to "Show/Hide All Services Analysis" when ready
        # Update the state when button is clicked
        if show_all:
            st.session_state.expand_all = not st.session_state.expand_all

        # Continue with existing risk analysis display
        for service in selected_services:
            # Use the session state to control expansion
            with st.expander(f"Risk Analysis for {service}", expanded=st.session_state.expand_all):
                risk_data = fetch_cloud_risk_data(service, region_type)
                if risk_data:
                    col1, col2, col3, col4 = st.columns(4)

                    # TODO: change to ASK_CUSTOMER_HOW_MUCH=1000 when ready
                    # Formula: when SLA usage is 100% or more, then the credit back is XXX%-100% of the SLA usage , divide by 12 for monthy approach
                    estimated_cloud_services_credit_money_back = 0.0 if float(risk_data.get("service_sla_usage_percentage", 0.0).rstrip('%')) <= 100 else (float(risk_data.get("service_sla_usage_percentage", 0.0).rstrip('%'))-100)/100*float(risk_data.get("percentage_service_credit_back_tier1", 0.0).rstrip('%'))/100*service_costs[service]
                    estimated_cloud_services_credit_money_back = round(estimated_cloud_services_credit_money_back, 2)
                    # Limit the credit back to 1000.00 per month
                    # TODO: change to ASK_CUSTOMER_HOW_MUCH=1000 when ready
                    # Open question: what is the max. credit back per month?
                    # TODO: add 1000 to the formula when ready (ASK_CUSTOMER_HOW_MUCH=1000)
                    # Set Warning if max. credit back was above 1000.00 per month
                    warning_max_credit_back = f"**Warning: Max. credit back was above the {service_costs[service]} of service estimated cost per month**" if estimated_cloud_services_credit_money_back > service_costs[service] else ""
                    estimated_cloud_services_credit_money_back = min(estimated_cloud_services_credit_money_back, service_costs[service])

                    with col1:
                        st.metric("SLA Usage %", risk_data.get("service_sla_usage_percentage", "N/A"))
                        st.metric("Rating Cloud.Risk SLA Deviation", risk_data.get("sla_deviation_connected_risk_0_999", "N/A"))
                    
                    with col2:
                        st.metric("Traffic Coefficient %", risk_data.get("service_traffic_coef_by_percent_down", "N/A"))
                        st.metric("Rating Cloud.Risk Usage", risk_data.get("usage_connected_risk_0_999", "N/A"))
                    
                    with col3:
                        st.metric("Annual Downtime (minutes)", risk_data.get("webscraper_annual_period_service_down_per_year_in_minutes", "N/A"))
                        st.metric("By SLA Expected Annual Downtime (minutes)", risk_data.get("expected_annual_service_minutes_down", "N/A"))
                    
                    with col4:
                        st.metric("Service SLA Tier 1 (99.99999%)", risk_data.get("service_sla_0_99_9999_for_tier1", "N/A") +"%")
                        st.metric("Service Credit Back Tier 1 (%)", str(risk_data.get("percentage_service_credit_back_tier1", "N/A"))+"%")
                        st.metric("Monthly Credit Back max. for Service ", "$"+str(estimated_cloud_services_credit_money_back))
                        st.caption(warning_max_credit_back)
                    
                    st.text_area(f"AI Analysis - {service}", risk_data.get("remarks_outage_genai", "No analysis available"), height=100)
                    st.divider()

        # Add a new section for displaying outage reports as charts
        if selected_services:
            st.subheader("Outage Reports by Selected Services")

            for service in selected_services:
                # Fetch outage data for each selected service
                outage_data = fetch_outage_data(service)  # New function to fetch outage data

                if outage_data:
                    # Create a DataFrame for the outage data
                    df_outages = pd.DataFrame(outage_data)

                    # Display a chart for the outages
                    # Follow chronological order with outage_timestamp
                    st.line_chart(df_outages['outage_timestamp'], use_container_width=True)  # Example chart

                    st.write(f"Outage details for {service}:")
                    st.dataframe(df_outages)  # Display the outage data in a table

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
