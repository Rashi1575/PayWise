import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os 

# === Step 1: Load the Dataset ===
df = pd.read_csv("creditcard.csv")  # File should be in the same directory

# === Step 2: Rename target column ===
df.rename(columns={"Class": "is_fraud"}, inplace=True)

# === Step 3: Optional — Reduce imbalance (speed up training) ===
# You can comment this out to use the full dataset
# fraud_df = df[df["is_fraud"] == 1]
# non_fraud_df = df[df["is_fraud"] == 0].sample(n=len(fraud_df)*3, random_state=42)
# df = pd.concat([fraud_df, non_fraud_df])

# === Step 4: Split features and labels ===
X = df.drop(columns=["is_fraud", "Time"], errors="ignore")  # Drop Time if exists
y = df["is_fraud"]

# === Step 5: Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === Step 6: Train model ===
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === Step 7: Evaluate model ===
print("\n=== Classification Report ===")
print(classification_report(y_test, model.predict(X_test)))

# === Step 8: Save model and feature list ===
joblib.dump(model, "fraud_model.pkl")
joblib.dump(X.columns.tolist(), "fraud_model_features.pkl")

print("Model and feature list saved.")
