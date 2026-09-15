#!/usr/bin/env bash
# Start Vetra Control Plane daemon
set -e

MODE=${1:-"simulation"}
PORT=${2:-8080}
VLLM_URL=${3:-"http://localhost:8000"}

echo "Starting Vetra Control Plane in ${MODE} mode on port ${PORT}..."
python -m vetra.cli.main start --mode "${MODE}" --port "${PORT}" --vllm-url "${VLLM_URL}"
