# =========================================
# AI Predictor for Patient No-Show Appointments
# Explainable Operational Intelligence
# Hackathon-ready | Single-file | Zero-dependency
# =========================================

import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Patient No-Show Predictor",
    page_icon="🏥",
    layout="centered"
)

# -----------------------------
# Force Light Theme + UI Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #f4f9ff !important;
}
.block-container {
    padding: 2rem 3rem;
}
h1, h2, h3 {
    color: #0b3c5d;
    font-family: 'Segoe UI', sans-serif;
}
div[data-testid="stVerticalBlock"] {
    background-color: #ffffff;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}
button[kind="primary"] {
    background-color: #2a7be4 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
div[data-testid="stProgress"] > div > div {
    background-image: linear-gradient(90deg, #2ecc71, #f1c40f, #e74c3c);
}
section[data-testid="stSidebar"] {
    background-color: #eaf3ff;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏥 Clinic Assistant")
st.sidebar.markdown("""
**Purpose:**  
Predict **appointment no-show risk**  
to improve hospital operations.

✔ Non-medical  
✔ Explainable  
✔ Staff-friendly  
""")
st.sidebar.caption("Hackathon Prototype")

# -----------------------------
# HERO HEADER (Always Visible)
# -----------------------------
st.markdown("""
<div style="
    background: linear-gradient(90deg, #2a7be4, #5fa8ff);
    padding: 30px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
">

<h1 style="margin-bottom: 10px; color: white;">
🏥 AI Predictor for Patient No-Show Appointments
</h1>

<h3 style="margin-top: 0; font-weight: 400; color: #eaf3ff;">
Operational Risk Classification • Hackathon Prototype
</h3>

<hr style="border: 1px solid rgba(255,255,255,0.3); margin: 20px 0;">

<p style="font-size: 18px; margin-bottom: 5px;">
<b>Team:</b> GFBQ-Team-Grimoire
</p>

<p style="font-size: 16px; margin-top: 0;">
Alhamda Iqbal Sadiq • Ashmira Mirza • Shifa Akbani • Khudaija Harmain
</p>

<p style="font-size: 14px; opacity: 0.9; margin-top: 15px;">
🧠 Decision-support system for hospital operations  
⚠️ Not a medical diagnosis tool
</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# Main Header
# -----------------------------
st.title("📅 Patient Appointment No-Show Predictor")

st.markdown("""
This tool helps clinics **reduce missed appointments**
by identifying **high-risk bookings in advance** and
suggesting **simple preventive actions**.
""")

st.markdown("---")

# -----------------------------
# Risk Logic (Balanced & Realistic)
# -----------------------------
def predict_no_show_risk(lead_time, past_no_shows, reminder, distance, time_of_day, day_type):
    risk = 10  # base risk
    reasons = []

    if lead_time > 14:
        risk += 30
        reasons.append("📆 Appointment booked far in advance")

    if past_no_shows >= 1:
        risk += 25
        reasons.append("❌ Previous missed appointment(s)")

    if reminder == "No":
        risk += 25
        reasons.append("📩 No reminder sent")

    if distance == "Far":
        risk += 15
        reasons.append("📍 Patient lives far from clinic")

    if time_of_day == "Evening":
        risk += 10
        reasons.append("🌙 Evening appointment slot")

    if day_type == "Weekend":
        risk += 10
        reasons.append("🗓 Weekend scheduling")

    if lead_time > 14 and reminder == "No":
        risk += 10
        reasons.append("⚠️ Long lead time without reminder")

    return min(risk, 100), reasons

# -----------------------------
# Input Section
# -----------------------------
st.header("📝 Appointment Details")

c1, c2 = st.columns(2)

with c1:
    lead_time = st.slider("📆 Days between booking & appointment", 1, 30, 10)
    past_no_shows = st.slider("❌ Number of past no-shows", 0, 5, 0)
    reminder = st.selectbox("📩 Reminder sent?", ["Yes", "No"])

with c2:
    time_of_day = st.selectbox("⏰ Appointment time", ["Morning", "Evening"])
    day_type = st.selectbox("🗓 Appointment day", ["Weekday", "Weekend"])
    distance = st.selectbox("📍 Patient distance", ["Near", "Far"])

st.markdown("---")

# -----------------------------
# Prediction Section
# -----------------------------
if st.button("🔍 Predict No-Show Risk", use_container_width=True):

    risk_percent, reasons = predict_no_show_risk(
        lead_time, past_no_shows, reminder, distance, time_of_day, day_type
    )

    st.subheader("📊 Risk Overview")

    if risk_percent >= 70:
        emoji, level = "😟", "HIGH"
    elif risk_percent >= 40:
        emoji, level = "😐", "MEDIUM"
    else:
        emoji, level = "🙂", "LOW"

    st.markdown(f"### {emoji} Risk Level: **{level}**  \n**Estimated Probability:** {risk_percent}%")
    st.progress(risk_percent / 100)

    cA, cB, cC = st.columns(3)
    cA.metric("🟢 Low", "0–39%")
    cB.metric("🟡 Medium", "40–69%")
    cC.metric("🔴 High", "70–100%")

    st.markdown("---")

    # -----------------------------
    # Visual Risk Contribution
    # -----------------------------
    st.subheader("📈 Risk Contribution Analysis")

    chart_data = pd.DataFrame({
        "Factor": ["Lead Time", "Past No-Shows", "Reminder", "Distance", "Time", "Day"],
        "Impact": [
            30 if lead_time > 14 else 5,
            25 if past_no_shows >= 1 else 5,
            25 if reminder == "No" else 5,
            15 if distance == "Far" else 5,
            10 if time_of_day == "Evening" else 5,
            10 if day_type == "Weekend" else 5
        ]
    }).set_index("Factor")

    st.bar_chart(chart_data)

    # -----------------------------
    # Explainability
    # -----------------------------
    st.subheader("🧠 Why this risk?")

    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("• No major risk factors detected")

    st.markdown("---")

    # -----------------------------
    # What-If Insight
    # -----------------------------
    st.subheader("🔮 What if a reminder is sent?")
    improved = max(risk_percent - 20, 0)

    colX, colY = st.columns(2)
    colX.metric("Current Risk", f"{risk_percent}%")
    colY.metric("After Reminder", f"{improved}%", delta=f"-{risk_percent - improved}%")

    st.markdown("---")

    # -----------------------------
    # Recommendation
    # -----------------------------
    st.subheader("🛠 Recommended Action")

    if risk_percent >= 70:
        st.info("📞 Call patient + send reminder. Consider safe overbooking.")
    elif risk_percent >= 40:
        st.info("📩 Send reminder or confirmation message.")
    else:
        st.success("✅ No action needed — appointment likely to be attended.")

    st.caption(
        "🔍 Explainable operational intelligence prototype. "
        "Production systems can replace this logic with trained ML models."
    )
