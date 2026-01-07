import streamlit as st
import requests
import json
import re

# ---------- Page ----------
st.set_page_config(page_title="TXT Football Data Validator", layout="centered")
st.title("TXT Football Data Validator (AI)")

st.write("Step 1️⃣ : Paste your Gemini API Key")
st.write("Step 2️⃣ : Upload TXT file and click Analyze")

# ---------- API KEY INPUT (ဒီနေရာပဲ သင်တောင်းထားတာ) ----------
api_key = st.text_input(
    "Gemini API Key",
    type="password",
    placeholder="AIzaSyxxxxxxxxxxxxxxxxxxxx"
)

if not api_key:
    st.info("Please enter your Gemini API key to continue.")
    st.stop()

# ---------- File Upload ----------
uploaded = st.file_uploader("Upload TXT file", type=["txt"])

# ---------- Helper ----------
def extract_json(text: str):
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
- name, football_team, phone are required
- missing or invalid → discard
- phone = digits only

TEXT:
{text}
"""

            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

            try:
                res = requests.post(
                    url,
                    params={"key": api_key},
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [
                            {"parts": [{"text": prompt}]}
                        ]
                    },
                    timeout=60,
                )
            except Exception as e:
                st.error(f"Network error: {e}")
                st.stop()

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

            try:
                records = json.loads(json_text).get("records", [])
            except:
                st.error("JSON parse failed")
                st.text(json_text)
                st.stop()

            if not records:
                st.warning("No valid records found")
            else:
                st.success(f"Found {len(records)} valid records")
                st.table(records)
