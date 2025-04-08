import streamlit as st
import psycopg2
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    'dbname': 'cloud_risk_portal',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

def get_database_metadata():
    """Fetch metadata about all tables in the database."""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT table_schema, table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name, ordinal_position;
    """)
    
    metadata = []
    for row in cursor.fetchall():
        schema, table, column, data_type, nullable = row
        metadata.append(f"Table: {schema}.{table}\nColumn: {column}\nType: {data_type}\nNullable: {nullable}\n")
    
    cursor.close()
    conn.close()
    return "\n".join(metadata)

def create_rag_chain():
    """Create a RAG chain for querying the database metadata."""
    # Get database metadata
    metadata_text = get_database_metadata()
    
    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_text(metadata_text)
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create vector store
    vectorstore = FAISS.from_texts(texts, embeddings)
    
    # Create LLM
    llm = Ollama(model="llama2")
    
    # Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    return qa_chain

def main():
    st.title("SQL Database Metadata Query Assistant")
    st.write("Ask questions about the database schema and get answers powered by RAG!")
    
    # Initialize session state for the QA chain
    if 'qa_chain' not in st.session_state:
        with st.spinner("Initializing RAG system..."):
            st.session_state.qa_chain = create_rag_chain()
    
    # User input
    user_question = st.text_input("Ask a question about the database schema:", 
                                 placeholder="e.g., What tables are in the cloud_risk_portal schema?")
    
    if user_question:
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.qa_chain.run(user_question)
                st.write("Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Add a button to refresh the metadata
    if st.button("Refresh Database Metadata"):
        with st.spinner("Refreshing metadata..."):
            st.session_state.qa_chain = create_rag_chain()
        st.success("Metadata refreshed successfully!")

if __name__ == "__main__":
    main() 