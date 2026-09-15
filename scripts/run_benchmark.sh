#!/usr/bin/env bash
# Execute Vetra benchmark suite
set -e

WORKLOAD=${1:-"mixed"}
REQUESTS=${2:-50}

echo "Running Vetra Benchmark comparison (Workload: ${WORKLOAD}, Requests: ${REQUESTS})..."
python benchmarks/report.py table
