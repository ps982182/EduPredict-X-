from fastapi import FastAPI
import joblib
import pandas as pd
import shap

app = FastAPI()

# Load model & scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

features = ['attendance', 'assignment', 'quiz', 'midsem', 'engagement']

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "EduPredict-X+ API is running 🚀"}

# =========================
# PREDICTION API
# =========================
@app.post("/predict")
def predict(data: dict):

    attendance = data["attendance"]
    assignment = data["assignment"]
    quiz = data["quiz"]
    midsem = data["midsem"]

    engagement = (attendance + assignment + quiz) / 3

    df = pd.DataFrame([{
        "attendance": attendance,
        "assignment": assignment,
        "quiz": quiz,
        "midsem": midsem,
        "engagement": engagement
    }])

    df_scaled = scaler.transform(df)

    pred = model.predict(df_scaled)[0]

    return {
        "risk": int(pred),
        "status": "HIGH RISK ⚠️" if pred == 1 else "SAFE ✅"
    }

# =========================
# EXPLANATION API (SHAP)
# =========================
@app.post("/explain")
def explain(data: dict):

    attendance = data["attendance"]
    assignment = data["assignment"]
    quiz = data["quiz"]
    midsem = data["midsem"]

    engagement = (attendance + assignment + quiz) / 3

    df = pd.DataFrame([{
        "attendance": attendance,
        "assignment": assignment,
        "quiz": quiz,
        "midsem": midsem,
        "engagement": engagement
    }])

    df_scaled = scaler.transform(df)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df_scaled)

    explanation = []

    for i, val in enumerate(shap_values[0]):
        if val < -0.2:
            explanation.append(f"Low {features[i]} is increasing risk")
        elif val > 0.2:
            explanation.append(f"Good {features[i]} is reducing risk")

    return {"explanation": explanation}

# =========================
# SUGGESTION API (COUNTERFACTUAL)
# =========================
@app.post("/suggest")
def suggest(data: dict):

    attendance = data["attendance"]
    assignment = data["assignment"]
    quiz = data["quiz"]

    suggestions = []

    if attendance < 60:
        suggestions.append(f"Increase attendance to 70+")

    if assignment < 50:
        suggestions.append(f"Improve assignment to 60+")

    if quiz < 40:
        suggestions.append(f"Improve quiz to 50+")

    return {"suggestions": suggestions}