FROM langchain/langchain:0.1.0

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY pdf_bot_v2.py .
COPY utils.py .
COPY chains.py .
COPY pdf_bot_usebatch.py .

# make batch mode work faster build without copying the entire folder of *.pdf files
COPY pdf_bot_usebatch/   ./pdf_bot_usebatch

# Run the script when the container starts - via streamlit entrypoint
# CMD ["python", "pdf_bot_usebatch.py"]

EXPOSE 8504

HEALTHCHECK CMD curl --fail http://localhost:8504/_stcore/health

ENTRYPOINT ["streamlit", "run", "pdf_bot_usebatch.py", "--server.port=8504", "--server.address=0.0.0.0"]
