import pandas as pd


def clean_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardise telemetry data.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    cleaned = df.copy()

    numeric_columns = [
        "timestamp",
        "lap",
        "distance",
        "speed",
        "throttle",
        "brake",
        "steering",
        "gear",
        "rpm",
        "x",
        "y",
        "sector",
        "lap_time",
    ]

    for col in numeric_columns:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned = cleaned.dropna(subset=["timestamp", "lap", "distance", "speed"])

    if "throttle" in cleaned.columns:
        cleaned["throttle"] = cleaned["throttle"].clip(0, 100)

    if "brake" in cleaned.columns:
        cleaned["brake"] = cleaned["brake"].clip(0, 100)

    if "gear" in cleaned.columns:
        cleaned["gear"] = cleaned["gear"].fillna(1).astype(int)

    cleaned = cleaned.sort_values(["lap", "distance"]).reset_index(drop=True)

    return cleaned