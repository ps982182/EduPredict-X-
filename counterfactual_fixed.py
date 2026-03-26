import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

# Input student
attendance = 50
assignment = 40
quiz = 30
midsem = 45

engagement = (attendance + assignment + quiz) / 3

student = pd.DataFrame([{
    "attendance": attendance,
    "assignment": assignment,
    "quiz": quiz,
    "midsem": midsem,
    "engagement": engagement
}])

# Predict
prediction = model.predict(student)[0]

print("\nPrediction:", "HIGH RISK ⚠️" if prediction == 1 else "SAFE ✅")

# 🔥 MANUAL COUNTERFACTUAL (ALWAYS WORKS)
print("\n🎯 Actionable Improvements:\n")

suggestions = []

if attendance < 60:
    suggestions.append(f"Increase attendance from {attendance} → 70+")

if assignment < 50:
    suggestions.append(f"Improve assignment score from {assignment} → 60+")

if quiz < 40:
    suggestions.append(f"Improve quiz score from {quiz} → 50+")

# Print suggestions
for s in suggestions:
    print("•", s)

# Simulate improved case
new_attendance = max(attendance, 70)
new_assignment = max(assignment, 60)
new_quiz = max(quiz, 50)

new_engagement = (new_attendance + new_assignment + new_quiz) / 3

new_student = pd.DataFrame([{
    "attendance": new_attendance,
    "assignment": new_assignment,
    "quiz": new_quiz,
    "midsem": midsem,
    "engagement": new_engagement
}])

new_pred = model.predict(new_student)[0]

print("\nAfter improvement →", "SAFE ✅" if new_pred == 0 else "Still Risk ⚠️")