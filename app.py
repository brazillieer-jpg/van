import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ဘောလုံးစလစ် စစ် AI",
    page_icon="⚽",
    layout="centered"
)

# ---------------- STYLE (Mobile Friendly) ----------------
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
.match-card {
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
    background: #111;
    border: 1px solid #2a2a2a;
}
.win {border-left: 6px solid #16a34a;}
.loss {border-left: 6px solid #dc2626;}
.title {font-size: 18px; font-weight: 700;}
.small {font-size: 14px; opacity: 0.85;}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("⚽ ဘောလုံးလောင်းစလစ် စစ် AI")
st.caption("စလစ်ပုံတင်ပါ → Match တစ်ပွဲချင်း ဘာကြောင့်နိုင် / ဘာကြောင့်ရှုံး ကို မြန်မာလိုရှင်းပြပါမယ်")

# ---------------- GEMINI ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- UPLOAD ----------------
uploaded = st.file_uploader(
    "📸 ဘောလုံးလောင်းစလစ် ပုံတင်ပါ",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    image = Image.open(uploaded)
    st.image(image, use_container_width=True)

    if st.button("🔍 စစ်မယ်", use_container_width=True):
        with st.spinner("AI စစ်နေပါတယ်..."):
            prompt = """
ဒီပုံက ဘောလုံး betting slip ဖြစ်ပါတယ်။

အောက်ပါအတိုင်း မြန်မာလိုပဲ ထုတ်ပါ။
Match တစ်ပွဲချင်း ခွဲပြီး JSON မဟုတ်ပဲ Human readable format နဲ့ရေးပါ။

လိုအပ်တာ:
1. Match တစ်ပွဲချင်း
   - Teams
   - Bet Type
   - Odds
   - Result (နိုင် / ရှုံး / Void)
2. Match တစ်ပွဲချင်းအတွက်
   - ❌ ရှုံးရတဲ့အကြောင်း (ရှိရင်)
   - ✅ နိုင်ရတဲ့အကြောင်း (ရှိရင်)

Format (ဥပမာ):
MATCH 1:
Teams:
Bet Type:
Odds:
Result:

Reason:
- ...

MATCH 2:
...

မခန့်မှန်းပါနဲ့
ပုံထဲမှာ မပါတဲ့ Result ကို မထည့်ပါနဲ့
"""

            res = model.generate_content([prompt, image])

        st.subheader("🧠 Match တစ်ပွဲချင်း အဖြေ")
        st.markdown(res.text)

else:
    st.info("👆 စလစ်ပုံတင်ပြီး စစ်နိုင်ပါတယ်")

st.markdown("---")
st.caption("📱 ဖုန်းနဲ့အသုံးပြုရအဆင်ပြေအောင် ဒီဇိုင်းလုပ်ထားပါတယ်")
