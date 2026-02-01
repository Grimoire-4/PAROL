# =========================================
# AI Predictor for Patient No-Show Appointments
# Hackathon Prototype | Single File
# =========================================

import streamlit as st
import pandas as pd

# -----------------------------
# Page Config (DO THIS FIRST)
# -----------------------------
st.set_page_config(
    page_title="Patient No-Show Predictor | GFBQ-Team-Grimoire",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# FORCE LIGHT THEME + RESET
# -----------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #f4f9ff !important;
}

* {
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 🔥 HERO SECTION (TOP OF PAGE – ALWAYS VISIBLE)
# =====================================================
st.markdown("""
<div style="
    width:100%;
    background: linear-gradient(90deg, #1e3c72, #2a7be4);
    padding:40px 20px;
    border-radius:20px;
    margin-bottom:40px;
    text-align:center;
    color:white;
">

<h1 style="font-size:48px; margin-bottom:10px;">
🏥 AI Predictor for Patient No-Show Appointments
</h1>

<h2 style="font-size:22px; font-weight:400; margin-top:0;">
Operational Risk Classification • Hackathon Prototype
</h2>

<hr style="border:1px solid rgba(255,255,255,0.4); width:60%; margin:25px auto;">

<h2 style="font-size:26px; margin-bottom:5px;">
👥 Team: <b>GFBQ-Team-Grimoire</b>
</h2>

<p style="font-size:18px; margin-top:5px;">
Alhamda Iqbal Sadiq • Ashmira Mirza • Shifa Akbani • Khudaija Harmain
</p>

<p style="font-size:15px; margin-top:20px; opacity:0.95;">
🧠 Decision-support system for hospital operations<br>
⚠️ Not a medical diagnosis or clinical decision tool
</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏥 Clinic Assistant")
st.sidebar.markdown("""
**What does this tool do?**

Predicts **appointment no-show risk**  
so clinics can:
- Send reminders
- Plan staffing
- Reduce wasted slots

✔ Explainable  
✔ Non-medical  
✔ Operational intelligence
""")
st.sidebar.caption("Hackathon Prototype")

# -----------------------------
# Main Content
# -----------------------------
st.header("📅 Enter Appointment Details")

# -----------------------------
# Risk Logic
# -----------------------------
def predict_no_show_risk(lead_time, past_no_shows, reminder, distance, time_of_day, day_type):
    risk = 10
    reasons = []

    if lead_time > 14:
        risk += 30
        reasons.append("📆 Appointment booked far in advance")

    if past_no_shows >= 1:
        risk += 25
        reasons.append("❌ History of missed appointments")

    if reminder == "No":
        risk += 25
        reasons.append("📩 No reminder sent")

    if distance == "Far":
        risk += 15
        reasons.append("📍 Patient lives far away")

    if time_of_day == "Evening":
        risk += 10
        reasons.append("🌙 Evening appointment")

    if day_type == "Weekend":
        risk += 10
        reasons.append("🗓 Weekend scheduling")

    if lead_time > 14 and reminder == "No":
        risk += 10
        reasons.append("⚠️ Long lead time without reminder")

    return min(risk, 100), reasons

# -----------------------------
# Inputs
# -----------------------------
c1, c2 = st.columns(2)

with c1:
    lead_time = st.slider("📆 Days before appointment was booked", 1, 30, 10)
    past_no_shows = st.slider("❌ Number of past missed appointments", 0, 5, 0)
    reminder = st.selectbox("📩 Was a reminder sent?", ["Yes", "No"])

with c2:
    time_of_day = st.selectbox("⏰ Appointment time", ["Morning", "Evening"])
    day_type = st.selectbox("🗓 Day of appointment", ["Weekday", "Weekend"])
    distance = st.selectbox("📍 Patient distance from clinic", ["Near", "Far"])

st.markdown("---")

# -----------------------------
# Prediction
# -----------------------------
if st.button("🔍 Predict No-Show Risk", use_container_width=True):

    risk_percent, reasons = predict_no_show_risk(
        lead_time, past_no_shows, reminder, distance, time_of_day, day_type
    )

    st.subheader("📊 Risk Assessment")

    if risk_percent >= 70:
        emoji, level = "🔴", "HIGH"
    elif risk_percent >= 40:
        emoji, level = "🟡", "MEDIUM"
    else:
        emoji, level = "🟢", "LOW"

    st.markdown(f"## {emoji} {level} RISK — {risk_percent}% chance of no-show")
    st.progress(risk_percent / 100)

    st.subheader("🧠 Why this risk?")
    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("• No major risk factors detected")

    st.markdown("---")

    st.subheader("🛠 Recommended Action")
    if risk_percent >= 70:
        st.error("📞 Call patient + send reminder. Consider safe overbooking.")
    elif risk_percent >= 40:
        st.warning("📩 Send reminder or confirmation message.")
    else:
        st.success("✅ No action needed — appointment likely to be attended.")

    st.caption(
        "Explainable operational intelligence prototype. "
        "ML models can replace this logic in production."
    )
