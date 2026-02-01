# =========================================
# AI Predictor for Patient No-Show Appointments
# Single-file Hackathon Prototype
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Patient No-Show Predictor", layout="centered")
st.title("🏥 AI Predictor for Patient No-Show Appointments")

st.markdown("""
This system predicts whether a patient is likely to **miss (No-Show)** or **attend (Show)**  
a scheduled appointment to help hospitals plan reminders, staffing, and overbooking.
""")

# -----------------------------
# Generate Simulated Historical Data
# -----------------------------
def generate_sample_data():
    np.random.seed(42)
    data = {
        "lead_time": np.random.randint(1, 30, 500),          # days between booking & appointment
        "past_no_shows": np.random.randint(0, 5, 500),
        "reminder_sent": np.random.randint(0, 2, 500),
        "time_of_day": np.random.randint(0, 2, 500),         # 0=Morning, 1=Evening
        "day_type": np.random.randint(0, 2, 500),            # 0=Weekday, 1=Weekend
        "distance_far": np.random.randint(0, 2, 500),        # 0=Near, 1=Far
    }

    df = pd.DataFrame(data)

    # Rule-based outcome generation (for training simulation)
    df["no_show"] = (
        (df["lead_time"] > 14).astype(int) +
        (df["past_no_shows"] > 1).astype(int) +
        (df["reminder_sent"] == 0).astype(int) +
        (df["distance_far"] == 1).astype(int)
    )

    df["no_show"] = (df["no_show"] >= 2).astype(int)
    return df

df = generate_sample_data()

# -----------------------------
# Train AI Model
# -----------------------------
X = df.drop("no_show", axis=1)
y = df["no_show"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -----------------------------
# User Input (Appointment Details)
# -----------------------------
st.header("📅 Enter Appointment Details")

lead_time = st.slider("Appointment Lead Time (days)", 1, 30, 10)
past_no_shows = st.slider("Past No-Shows", 0, 5, 0)
reminder = st.selectbox("Reminder Sent?", ["Yes", "No"])
time_of_day = st.selectbox("Time of Appointment", ["Morning", "Evening"])
day_type = st.selectbox("Day Type", ["Weekday", "Weekend"])
distance = st.selectbox("Patient Distance", ["Near", "Far"])

# Convert inputs to model format
input_data = pd.DataFrame([{
    "lead_time": lead_time,
    "past_no_shows": past_no_shows,
    "reminder_sent": 1 if reminder == "Yes" else 0,
    "time_of_day": 0 if time_of_day == "Morning" else 1,
    "day_type": 0 if day_type == "Weekday" else 1,
    "distance_far": 1 if distance == "Far" else 0,
}])

# -----------------------------
# Prediction
# -----------------------------
if st.button("🔍 Predict No-Show Risk"):
    risk_prob = model.predict_proba(input_data)[0][1]
    risk_percent = int(risk_prob * 100)

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

    reasons = []
    if lead_time > 14:
        reasons.append("Long appointment lead time")
    if past_no_shows > 1:
        reasons.append("History of missed appointments")
    if reminder == "No":
        reasons.append("No reminder sent")
    if distance == "Far":
        reasons.append("Patient lives far from clinic")

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

