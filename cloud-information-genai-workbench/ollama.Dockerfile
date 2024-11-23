#syntax = docker/dockerfile:1.4

FROM ollama/ollama::0.4.2 AS ollama

COPY ./run-ollama_llm.sh /root/run-ollama_llm.sh

WORKDIR /root

RUN chmod +x run-ollama_llm.sh

EXPOSE 11434

HEALTHCHECK --interval=20s --timeout=30s --retries=5 CMD ollama list || exit 1 # exit 1 is the response code for the healthcheck 0 - success 1 - unhealthy 2 - reserved

RUN chmod +x run-ollama_llm.sh \
    && ./run-ollama_llm.sh \
    && sleep 5
