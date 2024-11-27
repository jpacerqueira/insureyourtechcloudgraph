import os

import streamlit as st
from pdf_bot_v2 import process_pdf_query, process_folder

def process_single_test_pdf(input_folder="./pdf_bot_usebatch/test.pdf",
                            query="Resume the one or more outages indentified in text, how long was the incident, when was the outage, and what services got impacted in what regions and availability zones? Also, what services had outage, what was the root cause of the outage, how long was the outage , when was the outaged started, its duration in days, hours and minutes, duration of outaged explicited for each of the cloud services, what was the services downtime period, and when was it marked as resolved ? Also, remove Cloud Vendors not identified in the text. Also, remove Apostrophes, include all full words, no abreviations in text response.",
                            cloud_vendor="the Cloud Providers identified in the text being one or many of them, Amazon AWS and/or Google GCP and/or Microsoft Azure and/or  Oracle OCI and/or  IBM Cloud and/or Snowflake and/or Databricksa and/or MongoDB and/or Akamai and/or Cloudflare",
                            save_output=True,
                            output_dir="./pdf_bot_usebatch"):
    # Process single PDF
    response = process_pdf_query(pdf_path=input_folder, query=query, cloud_vendor=cloud_vendor, save_output=save_output, output_dir=output_dir)
    return response

def main(input_folder="./pdf_bot_usebatch"):
    st.title("Workbench App_4")
    st.header(f"PDF_BOT_BATCHMODE - 📄Extract Cloud Outage information from your pdf source folder {input_folder} (batch mode)")
    st.warning(f"This is a batch mode, it will process all the pdf files in the folder and save the output in the same folder {input_folder}")

    # Process entire folder
    process_folder(
        input_folder=input_folder,
        query="Resume the one or more outages indentified in text, how long was the incident, when was the outage, and what services got impacted in what regions and availability zones? Also, what services had outage, what was the root cause of the outage, how long was the outage , when was the outaged started, its duration in days, hours and minutes, duration of outaged explicited for each of the cloud services, what was the services downtime period, and when was it marked as resolved ? Also, remove Cloud Vendors not identified in the text. Also, remove Apostrophes, include all full words, no abreviations in text response.",
        cloud_vendor="the Cloud Providers identified in the text being one or many of them, Amazon AWS and/or Google GCP and/or Microsoft Azure and/or  Oracle OCI and/ro  IBM Cloud and/or Snowflake and/or Databricksa and/or MongoDB and/or Akamai and/or Cloudflare",
        output_folder=input_folder,
        mark_processed=True  
    )
    os.system("python pdf_bot_usebatch/merger.py")

if __name__ == "__main__":
    main()