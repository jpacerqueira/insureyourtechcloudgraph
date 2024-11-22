import os

import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.chains import RetrievalQA
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit.logger import get_logger
from chains import (
    load_embedding_model,
    load_llm,
)

# load api key lib
from dotenv import load_dotenv

load_dotenv(".env")


url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL")
llm_name = os.getenv("LLM")
# Remapping for Langchain Neo4j integration
os.environ["NEO4J_URL"] = url

logger = get_logger(__name__)


embeddings, dimension = load_embedding_model(
    embedding_model_name, config={"ollama_base_url": ollama_base_url}, logger=logger
)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


llm = load_llm(llm_name, logger=logger, config={"ollama_base_url": ollama_base_url})


def process_pdf_query(pdf_path, query, cloud_vendor="", save_output=False, output_dir=None):
    """Helper function to process PDF and run queries that can be called from other programs"""
    pdf_reader = PdfReader(pdf_path)
    
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text=text)
    
    vectorstore = Neo4jVector.from_texts(
        chunks,
        url=url,
        username=username,
        password=password,
        embedding=embeddings,
        index_name="pdf_bot",
        node_label="PdfBotChunk",
        pre_delete_collection=True,
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )
    
    # Enhance query with cloud vendor if specified
    enhanced_query = f"For {cloud_vendor} apply this query: {query}" if cloud_vendor else f"For all cloud vendors {cloud_vendor} apply this query: {query}"
    logger.info(f"In pdf_path: {pdf_path} - running query: {enhanced_query}")
    response = qa.run(enhanced_query)
    
    if save_output and output_dir:
        output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_path))[0] + ".txt")
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(response)
    
    return response

def process_folder(input_folder, query, cloud_vendor="", output_folder="pdf_bot_usebatch"):
    """Process all PDFs in a folder"""
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            process_pdf_query(pdf_path, query, cloud_vendor, True, output_folder)

def main():
    st.title("Workbench App_3")
    st.header("PDF_BOT - 📄Extract Cloud Outage information from your pdf source files")

    # Add cloud vendor selection
    cloud_vendor = st.selectbox(
        "Select Cloud Vendor",
        ["", "Amazon AWS", "Google GCP", "Microsoft Azure", "Oracle OCI", "IBM Cloud", "Snowflake", "Databricks", "MongoDB", "Akamai", "Cloudflare"]
    )

    # upload a your pdf file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    # Add save output option
    save_output = st.checkbox("Save output to file")
    
    if save_output:
        output_dir = "pdf_bot_usebatch"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    if pdf is not None:
        # Save uploaded file temporarily
        temp_pdf_path = f"temp_{pdf.name}"
        with open(temp_pdf_path, "wb") as f:
            f.write(pdf.getvalue())

        # Accept user questions/query
        query = st.text_input(
            "Request outage information from your upload pdf file\n"
            "- Ask Questions? e.g.\n"
            "- resume the outage in text, how long was the incident, when was the outage, and what services got impacted in what regions and availability zones?\n"
            "- What services had outage, how long was the outage, when was the outage?"
        )

        if query:
            stream_handler = StreamHandler(st.empty())
            response = process_pdf_query(
                temp_pdf_path,
                query,
                cloud_vendor,
                save_output,
                output_dir=output_dir if save_output else "pdf_bot_usebatch"
            )
            
            # Display with stream handler
            stream_handler.text = response
            stream_handler.container.markdown(response)

        # Cleanup temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)


if __name__ == "__main__":
    main()
