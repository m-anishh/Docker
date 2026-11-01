#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:8010"

echo "Waiting for FastAPI and Redis..."

ready=0

for i in {1..30}; do
  if curl -fsS --max-time 2 "$BASE_URL/healthz" >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done

if [ "$ready" -ne 1 ]; then
  echo "FAIL: Application did not become healthy"
  exit 1
fi

echo "PASS: API health check"

curl -fsS "$BASE_URL/" | python3 -c '
import json, sys
data = json.load(sys.stdin)
assert "message" in data
'
echo "PASS: Home endpoint"

before=$(docker compose exec -T redis redis-cli --raw GET visits)

if [[ ! "$before" =~ ^[0-9]+$ ]]; then
  before=0
fi

response=$(curl -fsS "$BASE_URL/visits")

actual=$(echo "$response" | python3 -c '
import json, sys
print(json.load(sys.stdin)["total_visits"])
')

expected=$((before + 1))

if [ "$actual" -ne "$expected" ]; then
  echo "FAIL: Expected $expected, got $actual"
  exit 1
fi

echo "PASS: Redis visitor counter ($actual)"
echo "All integration tests passed!"
