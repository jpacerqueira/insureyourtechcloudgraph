import os
import requests
from dotenv import load_dotenv

import streamlit as st
from neo4j import GraphDatabase


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

# Streamlit app starts here
st.title("Cloud Risk ")
st.header("Customer Submission App")
st.subheader("Calculate - cloud risk via inserting services manually")

#Obtain Environment Variables
load_dotenv(".env")

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j connection
uri = st.text_input("Neo4j URI", "bolt://cloudriskgraph.insureyourtech.cloud:17687" ) # "neo4j://cloudriskgraph.insureyourtech.cloud:17687")
user = st.text_input("Username", "neo4j")
password = st.text_input("Password", type="password")
driver = init_neo4j_connection(uri, user, password)

# Insert record form
st.header("New Cloud Risk - Insurance Risk Meajurement")
st.subheader("Insert detailed information")
st.subheader(" for - TECHNOLOGY_PROVIDER ")
st.subheader(" the - TECHNOLOGY_SOLUTION ")
node_type = st.text_input("Node Type", "TECHNOLOGY_SOLUTION")
properties = {}

# Dynamic properties input
num_properties = st.number_input(" By TECHNOLOGY_PROVIDER n TECHNOLOGY_SOLUTION's ", min_value=0, max_value=100, value=1)
for i in range(num_properties):
    key = st.text_input(f"TECHNOLOGY_PROVIDER {i+1} Key")
    value = st.text_input(f"TECHNOLOGY_SOLUTION {i+1} Name")
    properties[key] = value

# Insert button
if st.button("Insert Record"):
    record = insert_record(driver, node_type, properties)
    st.success(f"Record inserted: {record}")


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
