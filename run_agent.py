from fetch_logs import fetch_logs_dataprime
from save_logs import save_ndjson, save_json
import json

def main():
    ndjson_lines = fetch_logs_dataprime()

    if not ndjson_lines:
        print("❌ No data to save.")
        return

    save_ndjson(ndjson_lines, "logs.ndjson")

    # If you want structured JSON:
    parsed = [json.loads(line) for line in ndjson_lines if line.startswith('{')]
    save_json(parsed, "logs.json")

    # Print example: show severity or subsystem if present
    for item in parsed:
        if "result" in item:
            logs = item["result"]["results"]
            for log in logs:
                print(json.dumps(log, indent=2))

if __name__ == "__main__":
    main()
