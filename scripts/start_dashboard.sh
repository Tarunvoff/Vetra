#!/usr/bin/env bash
# Start Next.js monitoring dashboard
set -e

cd "$(dirname "$0")/../dashboard"
echo "Starting Vetra Next.js Dashboard..."
npm run dev
