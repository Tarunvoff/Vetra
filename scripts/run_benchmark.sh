#!/usr/bin/env bash
# Execute KVGuard benchmark suite
set -e

WORKLOAD=${1:-"mixed"}
REQUESTS=${2:-50}

echo "Running KVGuard Benchmark comparison (Workload: ${WORKLOAD}, Requests: ${REQUESTS})..."
python benchmarks/report.py table
