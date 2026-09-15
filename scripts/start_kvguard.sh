#!/usr/bin/env bash
# Start KVGuard Control Plane daemon
set -e

MODE=${1:-"simulation"}
PORT=${2:-8080}
VLLM_URL=${3:-"http://localhost:8000"}

echo "Starting KVGuard Control Plane in ${MODE} mode on port ${PORT}..."
python -m kvguard.cli.main start --mode "${MODE}" --port "${PORT}" --vllm-url "${VLLM_URL}"
