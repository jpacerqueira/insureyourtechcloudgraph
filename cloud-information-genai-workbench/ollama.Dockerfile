FROM ollama/ollama::0.5.3-rc0 AS ollama 
#syntax = docker/dockerfile:1.4

#FROM ollama/ollama:0.4.2 AS ollama
#FROM ollama/ollama:0.4.3 AS ollama
#FROM ollama/ollama:0.5.0 AS ollama #
### rocm is for AMD GPU support NO NVIDIA Drivers

COPY ./run-ollama_llm.sh /root/run-ollama_llm.sh

WORKDIR /root

RUN chmod +x run-ollama_llm.sh

EXPOSE 11434

HEALTHCHECK --interval=60s --timeout=30s --retries=5 CMD ollama list || exit 1 # exit 1 is the response code for the healthcheck 0 - success 1 - unhealthy 2 - reserved

RUN chmod +x run-ollama_llm.sh \
    && ./run-ollama_llm.sh \
    && sleep 5
