#!/usr/bin/env bash
# Start Next.js monitoring dashboard
set -e

cd "$(dirname "$0")/../dashboard"
echo "Starting KVGuard Next.js Dashboard..."
npm run dev
