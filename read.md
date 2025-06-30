fetch_agent/
│
├── .env
├── config.py
├── fetch_logs.py
├── save_logs.py
├── run_agent.py
├── streamlit_app.py  ← demo UI
├── requirements.txt
└── utils/
    └── parser.py



[.env Config] 
     ↓
[fetch_logs.py] ─────────┐
     ↓                   │
[parser.py]              │
     ↓                   │
[Smart Agent Core]       │
     ↓                   │
[streamlit_app.py] ◄─────┘
     ↓
[Output: Table | Raw | Export | Future AI Agent]



[Coralogix API (via fetch_logs.py)]
          ↓
[parse_log_lines() in log_parser.py]
          ↓
[DataFrame → structured logs]
          ↓
[Analysis OR LLM interaction (e.g., via llm_agent.py)]
          ↓
[Output → save to logs.json]
