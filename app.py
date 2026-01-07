import streamlit as st
import requests
import os
import json

st.title("TXT Football Data Validator (AI)")

uploaded = st.file_uploader("Upload TXT file", type=["txt"])

if uploaded:
    text = uploaded.read().decode("utf-8")

    if st.button("Analyze"):
        prompt = f"""
Extract ONLY valid records.
Each record must have: name, football_team, phone.
Return JSON only.

TEXT:
{text}
"""

        res = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": os.environ["GEMINI_API_KEY"]},
            json={"contents":[{"parts":[{"text":prompt}]}]}
        )

        try:
            raw = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            records = json.loads(raw)["records"]
            st.table(records)
        except:
            st.error("AI response error")
