import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from joblib import dump
from features import basic_features
from rules import rule_score

sys.stdout.reconfigure(encoding="utf-8")

# 1. Load data
df = pd.read_csv("data/samples/transactions.csv")

# 2. Create engineered features
df, feature_cols = basic_features(df)

# 3. Define labels
y = df["Class"]
X = df[feature_cols]

# 4. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 5. Train model
model = RandomForestClassifier(
    n_estimators=200,
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train)

# 6. Evaluate
proba = model.predict_proba(X_test)[:, 1]
print("ROC-AUC:", roc_auc_score(y_test, proba))
print(classification_report(y_test, (proba >= 0.5).astype(int)))

# --- Hybrid Scoring Section ---
# Apply model probabilities and rule scores on the test set
df_test = X_test.copy()
df_test["ml_score"] = proba
df_test["rule_score"] = rule_score(df.loc[X_test.index])
# Weighted hybrid score (tweak weights later if needed)
df_test["hybrid_score"] = 0.6 * df_test["ml_score"] + 0.4 * df_test["rule_score"]
# Mark transactions as suspicious if hybrid score > 0.8
df_test["suspicious"] = (df_test["hybrid_score"] > 0.8).astype(int)
# Save the hybrid results for inspection
df_test.to_csv("data/hybrid_results.csv", index=False)
print("✅ Hybrid results saved to data/hybrid_results.csv")
print("High-risk samples:", df_test["suspicious"].sum(), "of", len(df_test))

# 7. Save model
dump({"model": model, "features": feature_cols}, "models/rf_model.joblib")
print("Model saved to models/rf_model.joblib")

