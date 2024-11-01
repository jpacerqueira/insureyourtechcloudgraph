#syntax = docker/dockerfile:1.4

FROM ollama/ollama:latest AS ollama

COPY ./run-ollama_llm.sh /root/run-ollama_llm.sh

WORKDIR /root

RUN chmod +x run-ollama_llm.sh \
    && ./run-ollama_llm.sh
    && sleep infinity

EXPOSE 11434

HEALTHCHECK CMD curl --fail http://localhost:11434
