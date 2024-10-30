#syntax = docker/dockerfile:1.4

FROM ollama/ollama:latest AS ollama

COPY ./run-ollama.sh /tmp/run-ollama.sh

WORKDIR /tmp

RUN chmod +x run-ollama.sh \
    && ./run-ollama.sh

EXPOSE 11434


