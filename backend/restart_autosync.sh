#!/bin/bash
# Restart Google Sheets Auto-Sync with credentials

curl -X POST http://localhost:8000/api/google-sheets/auto-sync/start \
  -H "Content-Type: application/json" \
  -d "{
    \"sheet_url\": \"https://docs.google.com/spreadsheets/d/1c9OgQ_fr-Ia33wnXh3tC1JTh8hyaSoOIwME0RrAG7Uo/edit?gid=412096204#gid=412096204\",
    \"credentials_json\": $(cat /Users/jirehb.custodio/Downloads/mynagaapp-sheets-api-c06bb9d76039.json | jq -R -s .),
    \"interval_seconds\": 10
  }"
