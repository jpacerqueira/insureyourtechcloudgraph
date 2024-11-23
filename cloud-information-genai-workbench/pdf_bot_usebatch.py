import os

import streamlit as st
from pdf_bot import process_pdf_query, process_folder


def main(input_folder="./pdf_bot_usebatch"):
    st.title("Workbench App_4")
    st.header(f"PDF_BOT_BATCHMODE - 📄Extract Cloud Outage information from your pdf source folder {input_folder} (batch mode)")
    st.warning(f"This is a batch mode, it will process all the pdf files in the folder and save the output in the same folder {input_folder}")
    # Process single PDF
    #response = process_pdf_query(
    #    "pdf_bot_usebatch/test.pdf",
    #    "resume the outage in text, how long was the incident and what services got impacted, what regions and availability zones where impatected, and how long was the outage ?",
    #    cloud_vendor="Amazon AWS , Google GCP , Microsoft Azure , Oracle OCI , IBM Cloud, Snowflake, Databricks, MongoDB , Akamai, Cloudflare",
    #    save_output=True,
    #    output_dir="pdf_bot_usebatch"
    #)

    # Process entire folder
    process_folder(
        input_folder=input_folder,
        query="resume the outage in text, how long was the incident and what services got impacted, what regions and availability zones where impatected, and how long was the outage ?",
        cloud_vendor="Amazon AWS and Google GCP and Microsoft Azure and  Oracle OCI and  IBM Cloud and Snowflake and Databricksa and MongoDB and Akamai and Cloudflare",
        output_folder=input_folder
    )

if __name__ == "__main__":
    main()