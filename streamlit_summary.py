import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Load today's log
df = pd.read_csv("access_log.csv", names=["Timestamp", "Name", "Access", "Similarity"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
today = datetime.now().date()
df_today = df[df["Timestamp"].dt.date == today]

# Display raw data
st.title("📊 Daily Access Dashboard")
st.subheader(f"Log Summary for {today}")
st.dataframe(df_today)

# Prepare log text for summary
log_text = "\n".join([
    f"{row['Timestamp']} - {row['Name']} - {row['Access']} - {row['Similarity']}"
    for _, row in df_today.iterrows()
])

prompt = f"""
You are an assistant summarizing access control logs.

Entries:
{log_text}

Provide a summary with:
- Total entries
- Granted vs. Denied
- Unusual activity
"""

# Call local LLM (Gemma)
if st.button("Generate Summary"):
    with st.spinner("Summarizing..."):
        response = requests.post(
            "http://localhost:11434/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "gemma:2b-instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
        )

        try:
            summary = response.json()['choices'][0]['message']['content']
            st.subheader("📋 Summary")
            st.write(summary)
        except Exception as e:
            st.error("❌ Failed to get summary.")
            st.json(response.json())
