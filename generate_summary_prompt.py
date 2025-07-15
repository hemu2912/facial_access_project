import pandas as pd
from datetime import datetime

# Load access log CSV
df = pd.read_csv("access_log.csv", names=["Timestamp", "Name", "Access", "Similarity"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
today = datetime.now().date()
df_today = df[df["Timestamp"].dt.date == today]

# Convert to readable text
log_text = "\n".join([
    f"{row['Timestamp']} - {row['Name']} - {row['Access']} - {row['Similarity']}"
    for _, row in df_today.iterrows()
])

# Save as text for GPT4All
with open("summary_prompt.txt", "w", encoding="utf-8") as f:
    f.write("Summarize the following access logs:\n\n")
    f.write(log_text)
    f.write("\n\nGive a short report mentioning number of entries, users granted/denied, and anything unusual.")
