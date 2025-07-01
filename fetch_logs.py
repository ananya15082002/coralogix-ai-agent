# fetch_logs.py
import os
import requests
import json
from datetime import datetime, timedelta, timezone
from config import API_KEY, BASE_URL

def get_iso(dt):
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def fetch_logs_dataprime(limit=50):
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=5)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": f"source logs | limit {limit}",
        "metadata": {
            "tier": "TIER_FREQUENT_SEARCH",
            "syntax": "QUERY_SYNTAX_DATAPRIME",
            "startDate": get_iso(start),
            "endDate": get_iso(end),
            "defaultSource": "logs"
        }
    }

    try:
        res = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        res.raise_for_status()
        return res.text.strip().splitlines()
    except Exception as e:
        print(f"[❌] Error fetching logs: {e}")
        return []
