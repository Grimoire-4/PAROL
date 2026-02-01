
import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Patient No-Show Predictor",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# Force Light Theme (Simple & Safe)
# -----------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #f4f9ff;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏥 Clinic Assistant")
st.sidebar.markdown("""
This tool helps clinics **reduce missed appointments**
by predicting **No-Show risk** before the appointment day.

**Designed for:**
- Front desk staff
- Clinic managers
- Hospital operations teams

⚠️ *Not a medical diagnosis tool*
""")

# -----------------------------
# App Title
# -----------------------------
st.title("📅 Patient Appointment No-Show Predictor")

st.markdown("""
This system estimates the **likelihood of a patient missing an appointment**
and suggests **simple operational actions** to prevent it.
""")

st.markdown("---")

# -----------------------------
# Risk Logic (Explainable & Balanced)
# -----------------------------
def predict_no_show_risk(lead_time, past_no_shows, reminder, distance, time_of_day, day_type):
    risk = 10  # base risk
    reasons = []

    if lead_time > 14:
        risk += 30
        reasons.append("Appointment booked far in advance")

    if past_no_shows >= 1:
        risk += 25
        reasons.append("History of missed appointments")

    if reminder == "No":
        risk += 25
        reasons.append("No reminder sent")

    if distance == "Far":
        risk += 15
        reasons.append("Patient lives far from clinic")

    if time_of_day == "Evening":
        risk += 10
        reasons.append("Evening appointment slot")

    if day_type == "Weekend":
        risk += 10
        reasons.append("Weekend scheduling")

    if lead_time > 14 and reminder == "No":
        risk += 10
        reasons.append("Long lead time without reminder")

    return min(risk, 100), reasons

# -----------------------------
# Input Section
# -----------------------------
st.header("📝 Enter Appointment Details")

c1, c2 = st.columns(2)

with c1:
    lead_time = st.slider("Days before appointment was booked", 1, 30, 10)
    past_no_shows = st.slider("Number of past missed appointments", 0, 5, 0)
    reminder = st.selectbox("Was a reminder sent?", ["Yes", "No"])

with c2:
    time_of_day = st.selectbox("Appointment time", ["Morning", "Evening"])
    day_type = st.selectbox("Day of appointment", ["Weekday", "Weekend"])
    distance = st.selectbox("Patient distance from clinic", ["Near", "Far"])

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
        st.error(f"🔴 HIGH RISK — {risk_percent}% chance of no-show")
    elif risk_percent >= 40:
        st.warning(f"🟡 MEDIUM RISK — {risk_percent}% chance of no-show")
    else:
        st.success(f"🟢 LOW RISK — {risk_percent}% chance of no-show")

    st.progress(risk_percent / 100)

    # -----------------------------
    # Explainability
    # -----------------------------
    st.subheader("🧠 Why this risk?")
    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("• No major risk factors detected")

    # -----------------------------
    # Visual Insight
    # -----------------------------
    st.subheader("📈 Risk Contribution Overview")

    chart_data = pd.DataFrame({
        "Factor": ["Lead Time", "Past No-Shows", "Reminder", "Distance", "Time", "Day"],
        "Impact Score": [
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
    # Recommendation
    # -----------------------------
    st.subheader("🛠 What should the clinic do?")

    if risk_percent >= 70:
        st.info("📞 Call patient + send reminder. Consider safe overbooking.")
    elif risk_percent >= 40:
        st.info("📩 Send reminder or confirmation message.")
    else:
        st.info("✅ No action needed — appointment likely to be attended.")

# =====================================================
# ✅ FOOTER — TEAM DETAILS (ALWAYS VISIBLE)
# =====================================================
st.markdown("---")

st.markdown("## 🏆 Hackathon Details")

st.markdown("""
**Problem Statement:**  
AI Predictor for Patient No-Show Appointments  
*(Operational Risk Classification)*

**Team Name:**  
GFBQ-Team-Grimoire

**Team Members:**  
- Alhamda Iqbal Sadiq  
- Ashmira Mirza  
- Shifa Akbani  
- Khudaija Harmain  

**Note:**  
This is an **explainable, non-medical decision-support system** designed to assist hospital operations.
""")

st.caption("Hackathon Prototype • Explainable AI • Operational Intelligence")
