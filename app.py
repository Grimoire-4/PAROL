# =========================================
# AI Predictor for Patient No-Show Appointments
# Human-friendly | Visual | Zero-dependency
# =========================================

import streamlit as st
import pandas as pd

# -----------------------------
# Force Light Theme (CSS)
# -----------------------------
st.set_page_config(
    page_title="Patient No-Show Predictor",
    page_icon="🏥",
    layout="centered"
)

st.markdown("""
<style>

/* Force light background */
html, body, [class*="css"] {
    background-color: #f4f9ff !important;
}

/* Main container */
.block-container {
    padding: 2rem 3rem;
}

/* Headers */
h1, h2, h3 {
    color: #0b3c5d;
    font-family: 'Segoe UI', sans-serif;
}

/* Card-style sections */
div[data-testid="stVerticalBlock"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Buttons */
button[kind="primary"] {
    background-color: #2a7be4 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    background-image: linear-gradient(90deg, #2ecc71, #f1c40f, #e74c3c);
}

/* Sidebar */
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
Predict appointment **No-Show risk**  
for better hospital operations.

✔ Non-medical  
✔ Explainable  
✔ Staff-friendly
""")

st.sidebar.caption("Hackathon Prototype")

# -----------------------------
# Main Header
# -----------------------------
st.title("📅 Patient Appointment No-Show Predictor")

st.markdown("""
This tool helps clinics **reduce missed appointments**
by identifying **high-risk bookings in advance**.
""")

st.markdown("---")

# -----------------------------
# Risk Logic
# -----------------------------
def predict_no_show_risk(lead_time, past_no_shows, reminder, distance, time_of_day, day_type):
    risk = 10  # base risk (no appointment is ever zero-risk)
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

    # Compound risk boost (real-world behavior)
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
# Prediction
# -----------------------------
if st.button("🔍 Predict No-Show Risk", use_container_width=True):

    risk_percent, reasons = predict_no_show_risk(
        lead_time, past_no_shows, reminder, distance, time_of_day, day_type
    )

    st.subheader("📊 Risk Overview")

    # 🌡️ Visual Risk Gauge
    if risk_percent >= 70:
        emoji = "😟"
        level = "HIGH"
    elif risk_percent >= 40:
        emoji = "😐"
        level = "MEDIUM"
    else:
        emoji = "🙂"
        level = "LOW"

    st.markdown(
        f"""
        ### {emoji} No-Show Risk Level: **{level}**
        **Estimated Probability:** {risk_percent}%
        """
    )

    st.progress(risk_percent / 100)

    # 🚦 Traffic Light Indicators
    c1, c2, c3 = st.columns(3)
    c1.metric("🟢 Low Risk", "0–39%")
    c2.metric("🟡 Medium Risk", "40–69%")
    c3.metric("🔴 High Risk", "70–100%")

    st.markdown("---")

    # -----------------------------
    # Risk Contribution Visual
    # -----------------------------
    st.subheader("📈 What factors increased the risk?")

    chart_data = pd.DataFrame({
        "Factor": [
            "Lead Time",
            "Past No-Shows",
            "Reminder",
            "Distance",
            "Time of Day",
            "Day Type"
        ],
        "Impact Score": [
            25 if lead_time > 14 else 5,
            25 if past_no_shows > 1 else 5,
            20 if reminder == "No" else 5,
            15 if distance == "Far" else 5,
            10 if time_of_day == "Evening" else 5,
            5 if day_type == "Weekend" else 2
        ]
    }).set_index("Factor")

    st.bar_chart(chart_data)

    # -----------------------------
    # Explainability (Human Language)
    # -----------------------------
    st.subheader("🧠 Simple Explanation (Human-Readable)")

    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("• Appointment looks stable with no major risk signals")

    st.markdown("---")

    # -----------------------------
    # What-If Visual Insight
    # -----------------------------
    st.subheader("🔮 What if we send a reminder?")

    improved_risk = max(risk_percent - 20, 0)

    colA, colB = st.columns(2)
    colA.metric("Current Risk", f"{risk_percent}%")
    colB.metric("Risk After Reminder", f"{improved_risk}%", delta=f"-{risk_percent - improved_risk}%")

    st.markdown("---")

    # -----------------------------
    # Recommendation
    # -----------------------------
    st.subheader("🛠 Recommended Action for Staff")

    if risk_percent >= 70:
        st.info("📞 Call patient + send reminder. Consider safe overbooking.")
    elif risk_percent >= 40:
        st.info("📩 Send reminder or confirmation message.")
    else:
        st.success("✅ No action needed. Appointment likely to be attended.")

    st.caption(
        "🔍 This is an **explainable operational intelligence prototype**. "
        "In production, the same logic can be replaced with a trained ML model."
    )
)

    # -----------------------------
    # Risk Overview
    # -----------------------------
    st.subheader("📊 Risk Overview")

    st.progress(risk_percent / 100)

    if risk_percent >= 70:
        st.error(f"🔴 High Risk — {risk_percent}% chance of No-Show")
    elif risk_percent >= 40:
        st.warning(f"🟡 Medium Risk — {risk_percent}% chance of No-Show")
    else:
        st.success(f"🟢 Low Risk — {risk_percent}% chance of No-Show")

    # -----------------------------
    # Analytical Visual (SAFE)
    # -----------------------------
    st.subheader("📈 Risk Contribution Analysis")

    chart_data = pd.DataFrame({
        "Factor": [
            "Lead Time",
            "Past No-Shows",
            "Reminder",
            "Distance",
            "Time of Day",
            "Day Type"
        ],
        "Impact Score": [
            25 if lead_time > 14 else 5,
            25 if past_no_shows > 1 else 5,
            20 if reminder == "No" else 5,
            15 if distance == "Far" else 5,
            10 if time_of_day == "Evening" else 5,
            5 if day_type == "Weekend" else 2
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

    # -----------------------------
    # Recommendation
    # -----------------------------
    st.subheader("🛠 Recommended Action")

    if risk_percent >= 70:
        st.info("📞 Send reminder immediately + consider safe overbooking")
    elif risk_percent >= 40:
        st.info("📩 Send reminder or confirmation message")
    else:
        st.info("✅ No action needed")

    st.caption(
        "🔍 Explainable operational intelligence prototype. "
        "In production, these features feed a trained ML classifier."
    )
