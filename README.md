# Facial Access Control System

A complete offline facial recognition access control system with daily log summarization using a local LLM (Gemma via Ollama) and a Streamlit dashboard.

## Features

1. **Face Detection & Recognition**  
   - Uses InsightFace (`buffalo_l`) on CPU.  
   - Enhances brightness & draws bounding boxes.  
   - Grants/denies access based on cosine similarity with registered embeddings.  
   - Logs each person **only once per day**.

2. **Access Logging**  
   - Appends each access attempt to `access_log.csv` with:  
     ```
     Timestamp, Name, Access, Similarity
     ```

3. **Daily Summary via Local LLM**  
   - Uses Ollama + `gemma:2b-instruct` model.  
   - Summarizes today’s log entries via `summarize_access_local.py`.

4. **Streamlit Dashboard**  
   - Displays today’s log and AI-generated summary.  
   - Launched via `streamlit_summary.py`.

5. **Unified Launcher**  
   - `main.py` can run the full pipeline (detection → summary → dashboard).

## Prerequisites

- **Python 3.10+**  
- **Ollama** installed & model pulled:
  ```bash
  ollama pull gemma:2b-instruct
