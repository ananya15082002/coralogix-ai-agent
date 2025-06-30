import streamlit as st
import pandas as pd
import json
import os
from utils.log_parser import parse_log_lines
from utils.llm_agent import query_llm
from fetch_logs import fetch_logs_dataprime
from save_logs import save_to_file

st.set_page_config(page_title="Coralogix AI Agent", layout="wide")

st.sidebar.header("⚙️ Settings")
refresh_time = st.sidebar.slider("⏱️ Refresh every (seconds)", 30, 600, 180)
max_logs = st.sidebar.number_input("🔢 Max log entries", min_value=10, max_value=1000, value=50)
ai_chat_enabled = st.sidebar.checkbox("✅ Enable AI Chat", value=True)

st.title("Agent for Coralogix Logs")

st.subheader("📥 Latest Logs")
raw_logs = fetch_logs_dataprime(limit=max_logs)
if raw_logs:
    try:
        ndjson_data = [json.loads(line) for line in raw_logs if line.strip()]
        logs = []
        for obj in ndjson_data:
            if 'result' in obj:
                logs = obj['result']['results']
                break
        parsed_df = parse_log_lines(logs)
        if not parsed_df.empty:
            st.dataframe(parsed_df)
            save_to_file(parsed_df)
        else:
            st.warning("⚠️ No logs parsed or available.")
    except Exception as e:
        st.error(f"❌ Failed to parse logs: {e}")
else:
    st.warning("⚠️ Log file not found or empty.")

if ai_chat_enabled:
    st.subheader("💬 Ask AI (Log Assistant)")
    user_input = st.text_input("Ask something about logs:")
    if user_input and 'parsed_df' in locals() and not parsed_df.empty:
        ai_response = query_llm(user_input, parsed_df)
        st.success(ai_response)
