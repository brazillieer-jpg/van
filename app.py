import streamlit as st
import pandas as pd
import re

# ---------------- Page ----------------
st.set_page_config(page_title="TXT Football Data Validator", layout="wide")
st.title("TXT Football Data Validator (NO AI)")
st.caption("Rule-based • Stable • No API")

# ---------------- Upload ----------------
uploaded = st.file_uploader("Upload TXT file", type=["txt"])

# ---------------- Helpers ----------------
TEAM_MAP = {
    "ဘာစီ": "Barcelona",
    "ဘာစီလိုနာ": "Barcelona",
    "barcelona": "Barcelona",
    "မန်ယူ": "Manchester United",
    "man united": "Manchester United",
    "manchester united": "Manchester United",
    "မန်စီးတီး": "Manchester City",
    "man city": "Manchester City",
    "liverpool": "Liverpool",
    "လီဗာပူး": "Liverpool",
    "arsenal": "Arsenal",
    "အာဆင်နယ်": "Arsenal",
    "tottenham": "Tottenham Hotspur",
    "စပါး": "Tottenham Hotspur",
    "aston villa": "Aston Villa",
    "ဗီလာ": "Aston Villa",
    "brighton": "Brighton",
    "ဘရိုက်တန်": "Brighton",
    "sevilla": "Sevilla",
    "newcastle": "Newcastle United",
    "real madrid": "Real Madrid",
    "ဗီလာရီရဲလ်": "Villarreal",
}

def normalize_team(word):
    w = word.lower().strip()
    for k, v in TEAM_MAP.items():
        if k in w:
            return v
    return None

def extract_phone(text):
    nums = re.findall(r'(?:\+?959|09)\d{7,9}', text)
    if not nums:
        return None
    return re.sub(r'\D', '', nums[0])

# ---------------- Main ----------------
if uploaded:
    raw = uploaded.read().decode("utf-8", errors="ignore")
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    records = []
    current_name = None
    current_teams = []
    current_phone = None

    for line in lines:
        phone = extract_phone(line)
        if phone:
            current_phone = phone

        teams_found = []
        for word in re.split(r"[,\|\-/ ]+", line):
            t = normalize_team(word)
            if t:
                teams_found.append(t)

        if teams_found:
            current_teams.extend(teams_found)

        # name heuristic
        if not phone and not teams_found and len(line) < 40:
            current_name = line

        # finalize record
        if current_phone and len(set(current_teams)) >= 5:
            records.append({
                "Name": current_name or "Unknown",
                "Phone": current_phone,
                "Teams": ", ".join(sorted(set(current_teams)))
            })
            current_name = None
            current_teams = []
            current_phone = None

    if not records:
        st.error("No valid records found")
        st.stop()

    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["Phone"])

    st.success(f"Valid records: {len(df)}")
    st.dataframe(df, use_container_width=True)

    # ---------------- Download ----------------
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Download CSV",
        csv,
        "football_validated.csv",
        "text/csv"
    )
