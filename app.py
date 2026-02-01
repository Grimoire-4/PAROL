# =========================================
# AI Predictor for Patient No-Show Appointments
# Zero-dependency Hackathon Prototype
# =========================================

import streamlit as st

st.set_page_config(page_title="Patient No-Show Predictor", layout="centered")
st.title("🏥 AI Predictor for Patient No-Show Appointments")

st.markdown("""
This system estimates the **risk of a patient missing an appointment**
to help hospitals plan reminders, staffing, and overbooking.
""")

# -----------------------------
# Risk Scoring Logic (AI-like)
# -----------------------------
def predict_no_show_risk(lead_time, past_no_shows, reminder, distance, time_of_day, day_type):
    risk = 0
    reasons = []

    if lead_time > 14:
        risk += 25
        reasons.append("Long appointment lead time")

    if past_no_shows > 1:
        risk += 25
        reasons.append("History of missed appointments")

    if reminder == "No":
        risk += 20
        reasons.append("No reminder sent")

    if distance == "Far":
        risk += 15
        reasons.append("Patient lives far from clinic")

    if time_of_day == "Evening":
        risk += 10
        reasons.append("Evening appointments have higher no-show rate")

    if day_type == "Weekend":
        risk += 5
        reasons.append("Weekend scheduling variability")

    return min(risk, 100), reasons

# -----------------------------
# User Input
# -----------------------------
st.header("📅 Appointment Details")

lead_time = st.slider("Appointment Lead Time (days)", 1, 30, 10)
past_no_shows = st.slider("Past No-Shows", 0, 5, 0)
reminder = st.selectbox("Reminder Sent?", ["Yes", "No"])
time_of_day = st.selectbox("Time of Appointment", ["Morning", "Evening"])
day_type = st.selectbox("Day Type", ["Weekday", "Weekend"])
distance = st.selectbox("Patient Distance", ["Near", "Far"])

# -----------------------------
# Prediction
# -----------------------------
if st.button("🔍 Predict No-Show Risk"):
    risk_percent, reasons = predict_no_show_risk(
        lead_time, past_no_shows, reminder, distance, time_of_day, day_type
    )

    st.subheader("📊 Prediction Result")

    if risk_percent >= 70:
        st.error(f"🔴 High No-Show Risk: {risk_percent}%")
    elif risk_percent >= 40:
        st.warning(f"🟡 Medium No-Show Risk: {risk_percent}%")
    else:
        st.success(f"🟢 Low No-Show Risk: {risk_percent}%")

    # -----------------------------
    # Explainability
    # -----------------------------
    st.subheader("🧠 Contributing Factors")
    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("• No major risk factors detected")

    # -----------------------------
    # Recommendation
    # -----------------------------
    st.subheader("🛠 Operational Recommendation")
    if risk_percent >= 70:
        st.info("Send reminder + consider safe overbooking")
    elif risk_percent >= 40:
        st.info("Send reminder or follow-up call")
    else:
        st.info("No action needed")
