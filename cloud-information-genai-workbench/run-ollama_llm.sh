#!/bin/bash
#
echo "Starting Ollama server..."
ollama serve &
echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done
#
ollama list
#
DEFAULT_LLM=Llama-3.2-3B-Instruct
LLM=${LLM:=DEFAULT_LLM}
#
ollama pull $LLM
#
ollama list
#