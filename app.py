import streamlit as st
import requests
import os
import json
import re

# ---------- UI ----------
st.set_page_config(page_title="TXT Football Data Validator", layout="centered")
st.title("TXT Football Data Validator (AI)")
st.write("Upload a TXT file. AI will extract only valid Name / Football Team / Phone records.")

# ---------- API KEY ----------
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY is not set. Please add it in Streamlit → Manage app → Secrets.")
    st.stop()

# ---------- File Upload ----------
uploaded = st.file_uploader("Upload TXT file", type=["txt"])

# ---------- Helpers ----------
def extract_json(text: str):
    """
    Safely extract the first JSON object from a text response.
    Works even if AI adds extra text or markdown.
    """
    match = re.search(r'\{[\s\S]*\}', text)
    return match.group(0) if match else None

# ---------- Main Logic ----------
if uploaded:
    text = uploaded.read().decode("utf-8", errors="ignore")

    if st.button("Analyze"):
        with st.spinner("Analyzing with AI..."):
            prompt = f"""
Return ONLY valid JSON. No explanation. No markdown.

Schema:
{{
  "records": [
    {{"name": "", "football_team": "", "phone": ""}}
  ]
}}

Rules:
- A record must include name, football_team, and phone.
- If any field is missing or invalid, discard that line.
- Normalize phone to digits only (keep country code if exists).

TEXT:
{text}
"""

            try:
                res = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                    params={"key": API_KEY},
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                    timeout=60,
                )
            except Exception as e:
                st.error(f"Network error: {e}")
                st.stop()

            if res.status_code != 200:
                st.error(f"Gemini API error ({res.status_code})")
                st.text(res.text)
                st.stop()

            try:
                raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                st.error("Unexpected Gemini response format")
                st.text(res.text)
                st.stop()

            json_text = extract_json(raw_text)
            if not json_text:
                st.error("AI did not return valid JSON")
                st.text(raw_text)
                st.stop()

            try:
                data = json.loads(json_text)
                records = data.get("records", [])
            except Exception as e:
                st.error("JSON parse failed")
                st.text(json_text)
                st.stop()

            if not records:
                st.warning("No valid records found.")
            else:
                st.success(f"Found {len(records)} valid records")
                st.table(records)
