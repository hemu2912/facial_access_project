import requests
import csv
from datetime import datetime

def read_access_logs():
    try:
        with open("access_log.csv", "r") as file:
            reader = csv.reader(file)
            entries = list(reader)[1:]  # Skip header if it exists
            return entries
    except FileNotFoundError:
        return []

def generate_prompt(entries):
    if not entries:
        return "The access log is empty. There are no entries to summarize."

    formatted = "\n".join([", ".join(row) for row in entries])
    prompt = f"""
You are an AI assistant that summarizes access control logs.
Here is today's access log:

{formatted}

Please provide:
- Total number of entries
- Number of granted vs denied entries
- Any unusual activity (like repeated denials, unknown faces, etc.)
Respond clearly.
"""
    return prompt

entries = read_access_logs()
prompt = generate_prompt(entries)

# 🔗 Local Ollama API call
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma:2b-instruct",
        "prompt": prompt,
        "stream": False
    }
)

try:
    summary = response.json()["response"]
    print("\n📋 DAILY ACCESS SUMMARY:\n")
    print(summary)
except Exception as e:
    print("\n❌ Failed to get summary.")
    print("🔍 Full response:")
    print(response.json())
