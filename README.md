# 🏥 AI Predictor for Patient No-Show Appointments
### Operational Risk Classification System

---

## 📌 Problem Statement
Missed hospital appointments (No-Shows) reduce clinic efficiency, waste staff time,
and delay care for other patients. Hospitals often identify no-shows only after
they occur, leading to reactive and inefficient operations.

---

## 💡 Proposed Solution
We propose an **AI-powered, explainable decision-support system** that predicts
the **risk of a patient missing a scheduled appointment** using operational
and behavioral factors.

The system helps hospitals:
- Prioritize reminders
- Plan staffing better
- Reduce wasted appointment slots
- Apply safe overbooking strategies

⚠️ This system is **not a medical diagnosis tool**.  
It supports **operational planning only**.

---

## 🧠 How the System Works
1. Historical appointment data is analyzed
2. Key operational features are extracted (lead time, reminders, timing)
3. A machine learning model learns patterns of no-shows
4. Upcoming appointments are assigned a **risk score**
5. Staff receive **clear, explainable recommendations**

---

## ⚙️ Technical Stack
- **Programming Language:** Python  
- **Web Framework:** Streamlit  
- **Machine Learning Model:** Logistic Regression  
- **Data Processing:** Pandas  
- **Deployment:** Local / GitHub Codespaces / Streamlit Cloud  

---

## 📊 Real-Life Data Used
The model is trained using a **public, anonymized healthcare dataset**:

- **Dataset:** Medical Appointment No-Shows Dataset  
- **Source:** Public healthcare records (Kaggle)  
- **Data Type:** Historical appointment scheduling data  
- **Privacy:** No personal identifiers or medical records  

### Features Used:
- Appointment lead time
- Reminder sent (SMS)
- Day of appointment
- Past no-show behavior (derived)
- Attendance outcome (Show / No-Show)

---

## 🤖 Model Training (Offline)
The predictive model is trained **offline** using real historical data.

- **Algorithm:** Logistic Regression  
- **Reason:** Transparent, explainable, and suitable for healthcare operations  
- **Output:** Probability score indicating no-show risk  

The trained model is saved as a reusable file (`model.pkl`) and loaded
by the application during runtime.

> For this hackathon prototype, rule-based logic simulates the trained
model’s behavior to ensure lightweight deployment and explainability.

---

## 🚀 How to Run the Project

### 1️⃣ Train the Model (One-Time)
```bash
python train_model.py
