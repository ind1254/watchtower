import sys
from pathlib import Path

# --- fix for ModuleNotFoundError: 'src' ---
# Add the project root (one level above /app) to Python path
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.append(str(root))

import streamlit as st
import pandas as pd
from joblib import load
from src.features import basic_features
from src.rules import rule_score

st.set_page_config(page_title="Watchtower AML Prototype", layout="wide")
st.title("🕵️‍♂️ Watchtower — Fraud & AML Risk Scoring")

uploaded = st.file_uploader("Upload a transactions CSV", type=["csv"])

if uploaded:
    # Load data
    df = pd.read_csv(uploaded)
    st.subheader("📄 Input Preview")
    st.dataframe(df.head())

    # Apply feature engineering
    df, feats = basic_features(df)

    # Load trained model
    model_blob = load(Path(__file__).resolve().parents[1] / "models" / "rf_model.joblib")
    model = model_blob["model"]

    # Run model + rules
    df["ml_score"] = model.predict_proba(df[feats])[:, 1]
    df["rule_score"] = rule_score(df)
    df["hybrid_score"] = 0.6 * df["ml_score"] + 0.4 * df["rule_score"]
    df["suspicious"] = (df["hybrid_score"] > 0.8).astype(int)

    # Display results
    st.subheader("📊 Results Summary")
    st.write(f"Total suspicious: {df['suspicious'].sum()} of {len(df)} transactions")
    st.metric("Mean hybrid score", round(df['hybrid_score'].mean(), 3))

    st.subheader("🚨 Suspicious Transactions")
    flagged = df[df["suspicious"] == 1]
    if not flagged.empty:
        st.dataframe(flagged.sort_values("hybrid_score", ascending=False))
        st.download_button(
            "Download flagged results CSV",
            flagged.to_csv(index=False),
            file_name="flagged.csv"
        )
    else:
        st.success("No transactions exceeded the risk threshold.")

else:
    st.info("⬆️ Upload a CSV file to begin scoring.")
