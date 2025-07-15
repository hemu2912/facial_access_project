import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Face Access Dashboard", layout="centered")

st.title("🔐 Face Recognition Access Log Dashboard")

LOG_FILE = "access_log.csv"

if not os.path.exists(LOG_FILE):
    st.warning("⚠️ No access log file found yet.")
    st.stop()

# Load the log
df = pd.read_csv(LOG_FILE, names=["Timestamp", "Name", "Access", "Similarity"])

# Sidebar filter
user_filter = st.sidebar.selectbox("Filter by user", ["All"] + sorted(df["Name"].unique().tolist()))
if user_filter != "All":
    df = df[df["Name"] == user_filter]

# Summary stats
granted = (df["Access"] == "Granted").sum()
denied = (df["Access"] == "Denied").sum()

st.subheader("📊 Access Summary")
col1, col2 = st.columns(2)
col1.metric("✅ Access Granted", granted)
col2.metric("❌ Access Denied", denied)

# Show latest 10 entries
st.subheader("🕒 Latest Entries")
st.dataframe(df.sort_values("Timestamp", ascending=False).head(10), use_container_width=True)

# Download log
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Log as CSV", csv, "access_log.csv", "text/csv")
