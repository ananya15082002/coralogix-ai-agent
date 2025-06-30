# fetch_logs.py

import requests
from datetime import datetime, timedelta
from config import API_KEY, BASE_URL

def fetch_logs_dataprime(limit=50):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=8)

    payload = {
        "query": f"source logs | limit {limit}",
        "metadata": {
            "tier": "TIER_FREQUENT_SEARCH",
            "syntax": "QUERY_SYNTAX_DATAPRIME",
            "startDate": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDate": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "defaultSource": "logs"
        }
    }

    print(f"[INFO] Fetching logs from {start_time.isoformat()} to {end_time.isoformat()} ...")
    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        lines = response.text.strip().split("\n")
        return [line for line in lines if line.strip()]
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return []
