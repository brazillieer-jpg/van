import streamlit as st
import requests
import os
import json
import re

st.set_page_config(page_title="TXT Football Data Validator", layout="centered")
st.title("TXT Football Data Validator (AI)")

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY is not set in Streamlit Secrets")
    st.stop()

uploaded = st.file_uploader("Upload TXT file", type=["txt"])

def extract_json(text: str):
    match = re.search(r'\{[\s\S]*\}', text)
    return match.group(0) if match else None

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
- name, football_team, phone required
- invalid or missing → discard
- phone = digits only

TEXT:
{text}
"""

            url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

            res = requests.post(
                url,
                params={"key": API_KEY},
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=60,
            )

            if res.status_code != 200:
                st.error(f"Gemini API error ({res.status_code})")
                st.json(res.json())
                st.stop()

            raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            json_text = extract_json(raw_text)

            if not json_text:
                st.error("AI did not return valid JSON")
                st.text(raw_text)
                st.stop()

            records = json.loads(json_text).get("records", [])

            if not records:
                st.warning("No valid records found")
            else:
                st.success(f"Found {len(records)} valid records")
                st.table(records)
