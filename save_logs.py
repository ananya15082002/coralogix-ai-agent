import json
import os

def save_to_file(df, filename="logs.json"):
    if df.empty:
        return
    path = os.path.join(os.getcwd(), filename)
    df.to_json(path, orient="records", indent=4)
