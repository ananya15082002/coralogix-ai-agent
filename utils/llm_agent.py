import requests
import pandas as pd
import json
from config import HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def extract_summary_stats(df: pd.DataFrame) -> str:
    summary = []

    if 'severity' in df.columns:
        severity_counts = df['severity'].value_counts().to_dict()
        summary.append(f"- Severity distribution: {severity_counts}")

    if 'applicationname' in df.columns:
        app_counts = df['applicationname'].value_counts().to_dict()
        summary.append(f"- Log volume by application: {app_counts}")

    if 'message' in df.columns:
        critical_logs = df[df['severity'].astype(str) == '5']
        if not critical_logs.empty:
            summary.append(f"- {len(critical_logs)} critical severity logs detected.")
            keywords = critical_logs['message'].str.extract(r"(exception|error|failed|OSError|timeout|CRIT)", expand=False).dropna().unique().tolist()
            if keywords:
                summary.append(f"- Frequent error keywords: {keywords}")

    if 'trace_id' in df.columns:
        unique_traces = df['trace_id'].nunique()
        summary.append(f"- Unique trace IDs: {unique_traces}")

    return "\n".join(summary)

def format_prompt(user_question, df: pd.DataFrame) -> str:
    stats_summary = extract_summary_stats(df)
    prompt = (
        f"You are an expert AI assistant helping developers to debug logs.\n"
        f"Here’s a  summary of the current logs with all stats:\n"
        f"{stats_summary}\n\n"
        f"The user asked: '{user_question}'\n\n"
        f"Based on the overall log patterns and metadata, provide a professional log analysis and suggest any root causes or action items without repeating raw log data."
    )
    return prompt

def query_llm(user_input, df: pd.DataFrame) -> str:
    try:
        prompt = format_prompt(user_input, df)
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 350}
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"]
            else:
                return "⚠️ Unexpected response format from LLM."
        else:
            return f"LLM Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception during LLM call: {str(e)}"
