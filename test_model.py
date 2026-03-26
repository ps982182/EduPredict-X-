import joblib
import pandas as pd

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# Input values
attendance = 55
assignment = 60
quiz = 45
midsem = 50

# Calculate engagement
engagement = (attendance + assignment + quiz) / 3

# Create DataFrame (IMPORTANT)
data = pd.DataFrame([{
    "attendance": attendance,
    "assignment": assignment,
    "quiz": quiz,
    "midsem": midsem,
    "engagement": engagement
}])

# Scale
data_scaled = scaler.transform(data)

# Predict
prediction = model.predict(data_scaled)

# Output
if prediction[0] == 1:
    print("HIGH RISK ⚠️")
else:
    print("SAFE ✅")