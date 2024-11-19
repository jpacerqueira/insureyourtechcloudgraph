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

EXPOSE 8504

HEALTHCHECK CMD curl --fail http://localhost:8504/_stcore/health

ENTRYPOINT ["streamlit", "run", "CustomerPortal_app.py", "--server.port=8504", "--server.address=0.0.0.0"]