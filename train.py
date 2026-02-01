# =========================================
# train_model.py
# Offline model training using real data
# =========================================

import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Load real dataset
df = pd.read_csv("data.csv")

# Convert date columns
df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"])
df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"])

# Create Lead Time feature
df["LeadTime"] = (df["AppointmentDay"] - df["ScheduledDay"]).dt.days

# Convert target to numeric
df["NoShow"] = df["No-show"].map({"Yes": 1, "No": 0})

# Select features (simple & explainable)
X = df[["LeadTime", "SMS_received"]]
y = df["NoShow"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")
