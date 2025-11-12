import pandas as pd


def rule_score(df: pd.DataFrame):
    """
    Assigns a basic heuristic risk score (0–1) to each transaction.
    Rules target obviously suspicious behavior such as large amounts
    or transactions occurring at unusual hours.
    """
    df = df.copy()
    # High-amount rule
    high_amount = (df["Amount"] > 2000).astype(int)
    # Night-time rule (hours between 0–6 or > 22)
    odd_hour = ((df.get("hour", 0) < 6) | (df.get("hour", 0) > 22)).astype(int)
    # Combine and normalize to 0–1
    score = (high_amount + odd_hour) / 2
    return score

