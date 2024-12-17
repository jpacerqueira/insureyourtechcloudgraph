FROM langchain/langchain

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY neo4j_customer_submission /app/neo4j_customer_submission

RUN pip install --upgrade -r requirements.txt

COPY CustomerPortal_app.py .

# Copy certs
# Copy certs and set permissions
COPY certs ./certs
RUN chmod 600 /app/certs/server8183.key /app/certs/server8183.cert
RUN chmod 600 /app/certs/server8185.key /app/certs/server8185.cert

EXPOSE 8185

HEALTHCHECK CMD curl --fail http://localhost:8185/_stcore/health

ENTRYPOINT ["streamlit", "run", "CustomerPortal_app.py", "--server.port=8185", "--server.address=0.0.0.0"]