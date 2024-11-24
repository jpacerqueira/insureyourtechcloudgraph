import os

import streamlit as st
from pdf_bot_v2 import process_pdf_query, process_folder

def process_single_test_pdf(input_folder="./pdf_bot_usebatch/test.pdf",
                        query="resume the outage in text, how long was the incident in hours minutes and seconds, when was the outage, and what services got impacted, what cloud provider regions and availability zones where impatected, and how long was the outage in summary ?",
                        cloud_vendor="Amazon AWS and/or Google GCP and/or Microsoft Azure and/or  Oracle OCI and/or  IBM Cloud and/or Snowflake and/or Databricksa and/or MongoDB and/or Akamai and/or Cloudflare",
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
        query="resume the outage in text, how long was the incident in hours minutes and seconds, when was the outage, and what services got impacted, what cloud provider regions and availability zones where impatected, and how long was the outage in summary ?",
        cloud_vendor="Amazon AWS and/or Google GCP and/or Microsoft Azure and/or  Oracle OCI and/ro  IBM Cloud and/or Snowflake and/or Databricksa and/or MongoDB and/or Akamai and/or Cloudflare",
        output_folder=input_folder  
    )

if __name__ == "__main__":
    main()