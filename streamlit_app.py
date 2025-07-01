# streamlit_app.py

import streamlit as st
import pandas as pd
import json
from utils.log_parser import parse_log_lines
from utils.llm_agent import query_llm
from fetch_logs import fetch_logs_dataprime
from save_logs import save_to_file
from streamlit_autorefresh import st_autorefresh

# ------------------------------------
# Page Config
# ------------------------------------
st.set_page_config(page_title="Coralogix AI Agent", layout="wide")

# ------------------------------------
# Sidebar - Settings
# ------------------------------------
st.sidebar.title("⚙️ Settings")
refresh_time = st.sidebar.slider("⏱️ Refresh interval (seconds)", min_value=30, max_value=600, value=180)
max_logs = st.sidebar.number_input("🔢 Maximum log entries", min_value=10, max_value=1000, value=50)
ai_chat_enabled = st.sidebar.checkbox("Enable AI Assistant", value=True)

# ------------------------------------
# Auto-refresh logic
# ------------------------------------
st_autorefresh(interval=refresh_time * 1000, key="auto_refresh")

# ------------------------------------
# App Title
# ------------------------------------
st.title(" Coralogix Log Monitoring Agent")

# ------------------------------------
# Fetch Logs
# ------------------------------------
st.subheader("📥 Latest Logs")
raw_logs = fetch_logs_dataprime(limit=max_logs)

if raw_logs:
    try:
        logs = []
        for line in raw_logs:
            obj = json.loads(line)
            if 'result' in obj and 'results' in obj['result']:
                logs.extend(obj['result']['results'])

        parsed_df = parse_log_lines(logs)

        if not parsed_df.empty:
            st.success(f"✅ Parsed {len(parsed_df)} logs")
            st.dataframe(parsed_df, use_container_width=True)
            save_to_file(parsed_df)
        else:
            st.warning("⚠️ No structured logs parsed from the response.")

    except Exception as e:
        st.error(f"❌ Error while parsing logs: {e}")
else:
    st.warning("⚠️ No logs fetched. Please check API keys or Coralogix availability.")

# ------------------------------------
# LLM Assistant Chat
# ------------------------------------
if ai_chat_enabled:
    st.subheader("💬 AI Log Assistant")
    user_input = st.text_area("Ask a question about the logs below:", height=100)

    if st.button("Submit"):
        if user_input and 'parsed_df' in locals() and not parsed_df.empty:
            with st.spinner("Querying LLM..."):
                ai_response = query_llm(user_input, parsed_df)
            st.success("🤖 LLM Response:")
            st.code(ai_response, language="markdown")
        else:
            st.warning("⚠️ Load logs before asking questions.")
