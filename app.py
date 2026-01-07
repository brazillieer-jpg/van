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
    "ဘာစီ": "Barcelona", "ဘာစီလိုနာ": "Barcelona", "barcelona": "Barcelona",
    "မန်ယူ": "Manchester United", "man united": "Manchester United",
    "မန်စီးတီး": "Manchester City", "man city": "Manchester City",
    "liverpool": "Liverpool", "လီဗာပူး": "Liverpool",
    "arsenal": "Arsenal", "အာဆင်နယ်": "Arsenal",
    "tottenham": "Tottenham Hotspur", "စပါး": "Tottenham Hotspur",
    "aston villa": "Aston Villa", "ဗီလာ": "Aston Villa",
    "brighton": "Brighton", "ဘရိုက်တန်": "Brighton",
    "sevilla": "Sevilla",
    "newcastle": "Newcastle United",
    "real madrid": "Real Madrid",
    "villarreal": "Villarreal", "ဗီလာရီရဲလ်": "Villarreal"
}

def normalize_team(word):
    w = word.lower().strip()
    for k, v in TEAM_MAP.items():
        if k in w:
            return v
    return None

def extract_phone(text):
    m = re.findall(r'(?:\+?959|09)\d{7,9}', text)
    if not m:
        return None
    return re.sub(r'\D', '', m[0])

# ---------------- Main ----------------
if uploaded:
    raw = uploaded.read().decode("utf-8", errors="ignore")
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    valid_records = []
    no_phone_records = []
    rejected_records = []

    current_name = None
    current_teams = []
    current_phone = None

    for line in lines:
        phone = extract_phone(line)
        teams_found = []

        for word in re.split(r"[,\|\-/ ]+", line):
            t = normalize_team(word)
            if t:
                teams_found.append(t)

        if phone:
            current_phone = phone
        if teams_found:
            current_teams.extend(teams_found)

        # Name heuristic
        if not phone and not teams_found and len(line) < 40:
            current_name = line

        # Decide record
        if current_phone and len(set(current_teams)) >= 5:
            valid_records.append({
                "Name": current_name or "Unknown",
                "Phone": current_phone,
                "Teams": ", ".join(sorted(set(current_teams)))
            })
            current_name = None
            current_teams = []
            current_phone = None

        elif not current_phone and teams_found:
            no_phone_records.append({
                "Name": current_name or "Unknown",
                "Teams": ", ".join(sorted(set(teams_found))),
                "Raw Line": line
            })

        elif current_phone and len(set(current_teams)) < 5:
            rejected_records.append({
                "Name": current_name or "Unknown",
                "Phone": current_phone,
                "Teams Found": len(set(current_teams)),
                "Reason": "Less than 5 teams"
            })

    # ---------------- Display ----------------
    if valid_records:
        df_valid = pd.DataFrame(valid_records)
        st.success(f"✅ Valid records: {len(df_valid)} (Duplicates allowed)")
        st.dataframe(df_valid, use_container_width=True)

        st.download_button(
            "⬇ Download VALID CSV",
            df_valid.to_csv(index=False).encode("utf-8-sig"),
            "valid_records.csv",
            "text/csv"
        )

    if no_phone_records:
        df_nophone = pd.DataFrame(no_phone_records)
        st.warning(f"📵 No-phone records: {len(df_nophone)}")
        st.dataframe(df_nophone, use_container_width=True)

        st.download_button(
            "⬇ Download NO-PHONE CSV",
            df_nophone.to_csv(index=False).encode("utf-8-sig"),
            "no_phone_records.csv",
            "text/csv"
        )

    if rejected_records:
        df_reject = pd.DataFrame(rejected_records)
        st.error(f"❌ Rejected records: {len(df_reject)}")
        st.dataframe(df_reject, use_container_width=True)

        st.download_button(
            "⬇ Download REJECTED CSV",
            df_reject.to_csv(index=False).encode("utf-8-sig"),
            "rejected_records.csv",
            "text/csv"
        )
