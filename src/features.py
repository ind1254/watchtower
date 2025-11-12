import numpy as np
import pandas as pd


def basic_features(df: pd.DataFrame):
    """
    Build numeric features for the credit card fraud dataset.
    Returns transformed DataFrame and list of feature columns.
    """

    df = df.copy()
    df["hour"] = (df["Time"] % 86400) // 3600
    df["log_amount"] = np.log1p(df["Amount"])
    feature_cols = [c for c in df.columns if c.startswith("V")] + ["hour", "log_amount", "Amount"]
    return df, feature_cols

