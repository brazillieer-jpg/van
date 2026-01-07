import streamlit as st
import google.generativeai as genai
import json
import re

# ---------- Page ----------
st.set_page_config(page_title="TXT Football Data Validator", layout="centered")
st.title("TXT Football Data Validator (AI)")
st.write("① Paste Gemini API Key → ② Upload TXT → ③ Analyze")

# ---------- API KEY INPUT (UI မှာထည့်) ----------
api_key = st.text_input(
    "Gemini API Key",
    type="password",
    placeholder="AIzaSyxxxxxxxxxxxxxxxxxxxx"
)

if not api_key:
    st.info("Please enter your Gemini API key to continue.")
    st.stop()

# ---------- Configure Gemini ----------
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
except Exception as e:
    st.error("Failed to initialize Gemini model")
    st.stop()

# ---------- File Upload ----------
uploaded = st.file_uploader("Upload TXT file", type=["txt"])

# ---------- Helper ----------
def extract_json(text: str):
    match = re.search(r'\{[\s\S]*\}', text)
    return match.group(0) if match else None

# ---------- Main ----------
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
- phone = digits only (keep country code if exists)

TEXT:
{text}
"""

            try:
                response = model.generate_content(prompt)
                raw_text = response.text
            except Exception as e:
                st.error("Gemini API call failed")
                st.text(str(e))
                st.stop()

            json_text = extract_json(raw_text)

            if not json_text:
                st.error("AI did not return valid JSON")
                st.text(raw_text)
                st.stop()

            try:
                records = json.loads(json_text).get("records", [])
            except Exception:
                st.error("JSON parse failed")
                st.text(json_text)
                st.stop()

            if not records:
                st.warning("No valid records found")
            else:
                st.success(f"Found {len(records)} valid records")
                st.table(records)
