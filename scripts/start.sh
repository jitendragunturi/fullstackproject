#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker-compose up --build -d
echo "Services started (docker-compose up -d)"
