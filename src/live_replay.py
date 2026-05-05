import pandas as pd


def get_replay_frame(df: pd.DataFrame, frame_index: int) -> pd.Series | None:
    """
    Get one telemetry row for live replay.
    """
    if df.empty:
        return None

    safe_index = frame_index % len(df)

    return df.iloc[safe_index]


def get_replay_window(
    df: pd.DataFrame,
    frame_index: int,
    window_size: int = 120,
) -> pd.DataFrame:
    """
    Get recent telemetry window for live chart.
    """
    if df.empty:
        return pd.DataFrame()

    safe_index = frame_index % len(df)
    start = max(0, safe_index - window_size)

    return df.iloc[start:safe_index + 1].copy()


def current_status(row: pd.Series) -> str:
    """
    Determine current driver status.
    """
    if row is None:
        return "No data"

    if row["brake"] > 60:
        return "Heavy braking"

    if row["throttle"] > 85 and row["brake"] < 5:
        return "Full throttle"

    if row["throttle"] < 10 and row["brake"] < 10:
        return "Coasting"

    if abs(row["steering"]) > 20:
        return "Cornering"

    return "Balanced"