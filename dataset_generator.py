import pandas as pd
import numpy as np

# Number of students (increase if you want more)
n = 5000

np.random.seed(42)

# Generate realistic data
attendance = np.random.randint(40, 100, n)
assignment = np.random.randint(30, 100, n)
quiz = np.random.randint(20, 100, n)
midsem = np.random.randint(20, 100, n)

# Engagement = average behavior
engagement = (attendance + assignment + quiz) / 3

# Risk logic (VERY IMPORTANT)
risk = []

for i in range(n):
    if attendance[i] < 60 or assignment[i] < 50 or quiz[i] < 40:
        risk.append(1)   # at risk
    else:
        risk.append(0)   # safe

# Create dataframe
df = pd.DataFrame({
    "attendance": attendance,
    "assignment": assignment,
    "quiz": quiz,
    "midsem": midsem,
    "engagement": engagement,
    "risk": risk
})

# Save file
df.to_csv("student_data.csv", index=False)

print("Dataset created!")
print(df.head())