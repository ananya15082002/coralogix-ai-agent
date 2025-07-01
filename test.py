from fetch_logs import fetch_logs_dataprime

import json
from fetch_logs import fetch_logs_dataprime

if __name__ == "__main__":
    logs = fetch_logs_dataprime(limit=5)

    print("\n🔎 Type of `logs`:", type(logs))

    # If logs is a list, print its length
    if isinstance(logs, list):
        print(f"✅ Total logs fetched: {len(logs)}")
        if not logs:
            print("❌ Log list is empty.")
        else:
            for idx, log in enumerate(logs):
                print(f"\n--- Log {idx + 1} ---")
                try:
                    print(json.dumps(log, indent=2))
                except Exception as e:
                    print(f"❌ JSON print failed for log {idx+1}: {e}")
                    print(log)
    else:
        print("❌ `logs` is not a list. Here's what was returned:")
        print(json.dumps(logs, indent=2) if isinstance(logs, dict) else logs)
