import shap
import joblib
import pandas as pd

# Load model + scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# Sample input
data = pd.DataFrame([{
    "attendance": 55,
    "assignment": 60,
    "quiz": 45,
    "midsem": 50,
    "engagement": (55 + 60 + 45) / 3
}])

# Scale
data_scaled = scaler.transform(data)

# SHAP explainer
explainer = shap.TreeExplainer(model)

# Get SHAP values
shap_values = explainer.shap_values(data_scaled)

# Print explanation
features = data.columns

print("\n📊 Feature Contributions:\n")

for i, val in enumerate(shap_values[0]):
    print(f"{features[i]} → {val:.4f}")