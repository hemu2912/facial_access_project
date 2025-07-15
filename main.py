import os
import pandas as pd
from datetime import datetime
import requests

# Load today's log entries
df = pd.read_csv("access_log.csv", names=["Timestamp", "Name", "Access", "Similarity"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
today = datetime.now().date()
df_today = df[df["Timestamp"].dt.date == today]

# Prepare log as text
log_text = "\n".join([
    f"{row['Timestamp']} - {row['Name']} - {row['Access']} - {row['Similarity']}"
    for _, row in df_today.iterrows()
])

# Prompt to summarize
prompt = f"""Summarize the following access log entries for today:

{log_text}

Provide a short report mentioning:
- Total number of entries
- Number of granted and denied
- Any patterns or unusual entries."""

# Call local LM Studio or Ollama API
response = requests.post(
    "http://localhost:11434/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "gemma:2b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
)

# Handle response
try:
    summary = response.json()["choices"][0]["message"]["content"]
    print("\nDAILY ACCESS SUMMARY:\n")
    print(summary)
    with open("summary_prompt.txt", "w", encoding="utf-8") as f:
        f.write(summary)
except Exception as e:
    print("Failed to get summary.")
    print("Full response:", response.json())
