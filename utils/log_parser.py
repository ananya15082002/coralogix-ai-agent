import pandas as pd
import hashlib
import json

def extract_from_user_data(user_data_str):
    """Helper to parse userData JSON safely if it’s a string."""
    try:
        return json.loads(user_data_str)
    except (json.JSONDecodeError, TypeError):
        return {}

def parse_log_lines(logs: list):
    parsed_data = []

    for log in logs:
        source = log.get("_source", log)
        user_data = source.get("userData", {})
        
        # Parse userData if it's a JSON string
        if isinstance(user_data, str):
            user_data = extract_from_user_data(user_data)

        # Priority: direct > userData > nested
        trace_id = source.get("traceId") or user_data.get("traceId") or "N/A"
        span_id = source.get("spanId") or user_data.get("spanId") or "N/A"
        timestamp = source.get("timestamp") or user_data.get("timestamp") or source.get("time") or user_data.get("time") or "N/A"
        severity = source.get("severity") or user_data.get("severity") or "N/A"
        application = source.get("application") or user_data.get("app_name") or "N/A"
        namespace = source.get("namespace") or user_data.get("namespace") or "N/A"
        pod_name = source.get("pod_name") or user_data.get("kubernetes", {}).get("pod_name") or "N/A"
        container_name = source.get("container_name") or user_data.get("kubernetes", {}).get("container_name") or "N/A"
        host = source.get("host") or user_data.get("kubernetes", {}).get("Host") or "N/A"
        message = source.get("message") or user_data.get("message") or "N/A"

        # Hash for deduplication
        log_hash = hashlib.md5(f"{timestamp}_{message}".encode()).hexdigest()

        parsed_data.append({
            "trace_id": trace_id,
            "span_id": span_id,
            "timestamp": timestamp,
            "severity": severity,
            "application": application,
            "namespace": namespace,
            "pod_name": pod_name,
            "container_name": container_name,
            "host": host,
            "message": message,
            "hash": log_hash
        })

    df = pd.DataFrame(parsed_data)

    # Drop duplicate entries based on hash
    df.drop_duplicates(subset="hash", inplace=True)
    df.drop(columns=["hash"], inplace=True)

    # Convert timestamp to datetime for visualization
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df
