#!/usr/bin/env bash
# Start vLLM with metrics and prefix caching enabled
set -e

MODEL_NAME=${1:-"meta-llama/Meta-Llama-3-8B-Instruct"}
PORT=${2:-8000}

echo "Starting vLLM inference server on port ${PORT} with model ${MODEL_NAME}..."
python -m vllm.entrypoints.openai.api_server \
  --model "${MODEL_NAME}" \
  --port "${PORT}" \
  --enable-prefix-caching \
  --disable-log-requests
