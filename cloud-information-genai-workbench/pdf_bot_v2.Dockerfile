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

COPY pdf_bot_usebatch/   ./pdf_bot_usebatch

EXPOSE 8505

HEALTHCHECK CMD curl --fail http://localhost:8505/_stcore/health

ENTRYPOINT ["streamlit", "run", "pdf_bot_v2.py", "--server.port=8505", "--server.address=0.0.0.0"]
