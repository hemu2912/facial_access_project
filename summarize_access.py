from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Load your .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load access log
df = pd.read_csv("access_log.csv", names=["Timestamp", "Name", "Access", "Similarity"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
today = datetime.now().date()
df_today = df[df["Timestamp"].dt.date == today]

# Convert logs to text
log_text = "\n".join([
    f"{row['Timestamp']} - {row['Name']} - {row['Access']} - {row['Similarity']}"
    for _, row in df_today.iterrows()
])

# Prompt
prompt = f"""Summarize the following access log entries for today:

{log_text}

Give a short report mentioning number of entries, users granted/denied, and anything unusual."""

# Use GPT-3.5-turbo
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

print("\n📋 DAILY ACCESS SUMMARY:")
print(response.choices[0].message.content)
