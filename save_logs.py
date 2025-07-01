import json
import os
import ndjson
import pandas as pd

def save_to_file(df, filename="logs.json"):
    if df.empty:
        return
    path = os.path.join(os.getcwd(), filename)
    df.to_json(path, orient="records", indent=4)

def save_json(data, filename="logs.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def save_ndjson(lines, filename="logs.ndjson"):
    with open(filename, "w") as f:
        writer = ndjson.writer(f, ensure_ascii=False)
        for line in lines:
            try:
                writer.writerow(json.loads(line))
            except:
                continue
