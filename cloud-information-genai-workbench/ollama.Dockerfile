#syntax = docker/dockerfile:1.4

FROM ollama/ollama:latest AS ollama

COPY ./run-ollama_llm.sh /root/run-ollama_llm.sh

WORKDIR /root

RUN chmod +x run-ollama_llm.sh

EXPOSE 11434

HEALTHCHECK --interval=1m --timeout=3s --retries=3 CMD curl -f http://localhost:11434 || exit 2 # exit 1 is the response code for the healthcheck 0 - success 1 - unhealthy 2 - reserved

RUN chmod +x run-ollama_llm.sh \
    && ./run-ollama_llm.sh \
    && sleep 5
