import requests
import pandas as pd
import json
from config import HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def format_prompt(user_question, df: pd.DataFrame) -> str:
    preview = df.head(5).to_json(orient="records", indent=2)
    prompt = (
        f"You are an AI assistant for log analysis. Analyze the following logs:\n\n"
        f"{preview}\n\n"
        f"User's Question: {user_question}\n\n"
        f"Give a short analysis with insights or issues identified in the logs."
    )
    return prompt

def query_llm(user_input, df: pd.DataFrame) -> str:
    try:
        prompt = format_prompt(user_input, df)
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 300}
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
