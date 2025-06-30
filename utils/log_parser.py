import pandas as pd
import hashlib
import json

def extract_from_user_data(user_data_str):
    """Safely parse userData if it's a stringified JSON."""
    try:
        return json.loads(user_data_str)
    except (json.JSONDecodeError, TypeError):
        return {}

def parse_log_lines(logs: list):
    parsed_data = []

    for log in logs:
        source = log.get("_source", log)
        user_data = source.get("userData", {})

        # Parse if userData is string
        if isinstance(user_data, str):
            user_data = extract_from_user_data(user_data)

        # Combine all possible nested paths to extract values
        trace_id = source.get("traceId") or user_data.get("traceId") or source.get("trace_id") or "N/A"
        span_id = source.get("spanId") or user_data.get("spanId") or source.get("span_id") or "N/A"
        timestamp = (
            source.get("timestamp") or source.get("time") or
            user_data.get("timestamp") or user_data.get("time") or
            "N/A"
        )
        severity = source.get("severity") or user_data.get("severity") or "N/A"
        application = source.get("application") or user_data.get("app_name") or "N/A"
        namespace = source.get("namespace") or user_data.get("namespace") or "N/A"
        pod_name = (
            source.get("pod_name") or
            user_data.get("kubernetes", {}).get("pod_name") or
            source.get("kubernetes", {}).get("pod_name") or
            "N/A"
        )
        container_name = (
            source.get("container_name") or
            user_data.get("kubernetes", {}).get("container_name") or
            source.get("kubernetes", {}).get("container_name") or
            "N/A"
        )
        host = (
            source.get("host") or
            user_data.get("kubernetes", {}).get("host") or
            source.get("kubernetes", {}).get("host") or
            "N/A"
        )

        # Improved message logic
        message = (
            source.get("message") or
            source.get("log") or
            user_data.get("message") or
            user_data.get("log") or
            str(source.get("error")) or "N/A"
        )

        # Build a stronger deduplication key
        dedup_key = f"{trace_id}_{span_id}_{timestamp}_{message}"
        log_hash = hashlib.md5(dedup_key.encode()).hexdigest()

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
            "message": message.strip(),
            "hash": log_hash
        })

    # Create DataFrame
    df = pd.DataFrame(parsed_data)

    # Remove exact duplicates
    df.drop_duplicates(subset="hash", inplace=True)
    df.drop(columns=["hash"], inplace=True)

    # Convert timestamp to datetime
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df
