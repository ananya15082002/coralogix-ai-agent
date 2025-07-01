# utils/log_parser.py
import pandas as pd
import json

def extract_from_user_data(user_data_str):
    try:
        return json.loads(user_data_str)
    except (json.JSONDecodeError, TypeError):
        return {}

def parse_log_lines(logs: list):
    parsed_data = []

    for log in logs:
        source = log.get("_source", log)
        metadata = source.get("metadata", [])
        labels = source.get("labels", [])
        user_data_raw = source.get("userData", "")

        row = {}

        # Extract metadata
        for item in metadata:
            row[item.get("key")] = item.get("value")

        # Extract labels
        for label in labels:
            row[label.get("key")] = label.get("value")

        # Parse userData
        user_data = extract_from_user_data(user_data_raw)
        for k, v in user_data.items():
            if isinstance(v, dict):
                for subk, subv in v.items():
                    row[f"{k}_{subk}"] = subv
            else:
                row[k] = v

        parsed_data.append(row)

    df = pd.DataFrame(parsed_data)
    return df
