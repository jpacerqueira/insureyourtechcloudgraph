#!/bin/bash

echo "Starting Ollama server..."
ollama serve &


echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

DEFAULT_LLM=llama3.2
LLM=${LLM:=DEFAULT_LLM}

ollama pull $LLM

ollama list

