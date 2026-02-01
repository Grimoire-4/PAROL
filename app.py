# =========================================
# AI Predictor for Patient No-Show Appointments
# Human-friendly | Explainable | Zero-dependency
# =========================================

import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Patient No-Show Predictor",
    page_icon="🏥",
    layout="centered"
)

# -----------------------------
# Sidebar – Friendly Context
# -----------------------------
st.sidebar.title("🏥 Clinic Assistant")
st.sidebar.markdown("""
This tool helps clinics **reduce missed appointments** by
predicting **No-Show risk** *before* the appointment day.

👩‍⚕️ Designed for:
- Front-desk staff
- Clinic managers
- Hospital operations teams

🧠 Uses explainable operational logic  
⚠️ Not a medical diagnosis tool
""")

st.sidebar.markdown("---")
st.sidebar.caption("Hackathon Prototype • Decision Support")

# -----------------------------
# Main Header
# -----------------------------
st.title("📅 Patient Appointment No-Show Predictor")

st.markdown("""
💡 **What does this do?**  
It estimates the likelihood that a patient may **miss their appointment**
and suggests **simple actions** to prevent it.
""")

st.markdown("---")

# -----------------------------
# Risk Logic (Explainable + Operational)
# -----------------------------
def predict_no_show_risk(lead_time, past_no_shows, reminder, distance, time_of_day, day_type):
    risk = 0
    reasons = []

    if lead_time > 14:
        risk += 25
        reasons.append("📆 Appointment booked far in advance")

    if past_no_shows > 1:
        risk += 25
        reasons.append("❌ History of missed appointments")

    if reminder == "No":
        risk += 20
        reasons.append("📩 No reminder sent")

    if distance == "Far":
        risk += 15
        reasons.append("📍 Patient lives far from clinic")

    if time_of_day == "Evening":
        risk += 10
        reasons.append("🌙 Evening appointment slot")

    if day_type == "Weekend":
        risk += 5
        reasons.append("🗓 Weekend scheduling")

    return min(risk, 100), reasons

# -----------------------------
# Input Section (Clean & Friendly)
# -----------------------------
st.header("📝 Enter Appointment Details")

col1, col2 = st.columns(2)

with col1:
    lead_time = st.slider("How many days before the appointment was it booked?", 1, 30, 10)
    past_no_shows = st.slider("How many past appointments were missed?", 0, 5, 0)
    reminder = st.selectbox("Was a reminder sent?", ["Yes", "No"])

with col2:
    time_of_day = st.selectbox("Appointment time", ["Morning", "Evening"])
    day_type = st.selectbox("Day of appointment", ["Weekday", "Weekend"])
    distance = st.selectbox("Patient distance from clinic", ["Near", "Far"])

st.markdown("---")

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("🔍 Check No-Show Risk", use_container_width=True):

    risk_percent, reasons = predict_no_show_risk(
        lead_time, past_no_shows, reminder, distance, time_of_day, day_type
    )

    # -----------------------------
    # Visual Risk Indicator
    # -----------------------------
    st.subheader("📊 No-Show Risk Assessment")
    st.progress(risk_percent / 100)

    if risk_percent >= 70:
        st.error(f"🔴 **High Risk** — {risk_percent}% chance of No-Show")
    elif risk_percent >= 40:
        st.warning(f"🟡 **Medium Risk** — {risk_percent}% chance of No-Show")
    else:
        st.success(f"🟢 **Low Risk** — {risk_percent}% chance of No-Show")

    # -----------------------------
    # Explainability Section
    # -----------------------------
    st.subheader("🧠 Why is this the risk?")

    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("• No significant risk factors detected")

    # -----------------------------
    # Recommendation Section
    # -----------------------------
    st.subheader("🛠 What should the clinic do?")

    if risk_percent >= 70:
        st.info("📞 Send reminder immediately and consider **safe overbooking**")
    elif risk_percent >= 40:
        st.info("📩 Send reminder or confirmation message")
    else:
        st.info("✅ No action needed — appointment likely to be attended")

    st.markdown("---")
    st.caption(
        "🔍 This prototype demonstrates **explainable operational intelligence**. "
        "In real deployment, the same inputs can feed a trained machine learning model."
    )
