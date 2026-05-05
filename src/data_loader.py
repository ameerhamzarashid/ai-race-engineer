from pathlib import Path

import pandas as pd

from src.config import REQUIRED_COLUMNS, SAMPLE_TELEMETRY_PATH
from src.generate_sample_data import generate_sample_telemetry


def ensure_sample_data() -> Path:
    """
    Make sure the sample telemetry file exists.
    """
    if not SAMPLE_TELEMETRY_PATH.exists():
        generate_sample_telemetry(SAMPLE_TELEMETRY_PATH)

    return SAMPLE_TELEMETRY_PATH


def load_sample_telemetry() -> pd.DataFrame:
    """
    Load built-in sample telemetry.
    """
    path = ensure_sample_data()
    return pd.read_csv(path)


def load_uploaded_telemetry(file) -> pd.DataFrame:
    """
    Load user uploaded CSV file.
    """
    return pd.read_csv(file)


def validate_telemetry_columns(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate required telemetry columns.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return len(missing) == 0, missing


def get_lap_numbers(df: pd.DataFrame) -> list[int]:
    """
    Get available lap numbers.
    """
    if df.empty or "lap" not in df.columns:
        return []

    return sorted(df["lap"].dropna().astype(int).unique().tolist())


def get_best_lap_number(df: pd.DataFrame) -> int | None:
    """
    Return lap number with lowest lap_time.
    """
    if df.empty or "lap_time" not in df.columns or "lap" not in df.columns:
        return None

    lap_summary = (
        df.groupby("lap", as_index=False)
        .agg(lap_time=("lap_time", "first"))
        .sort_values("lap_time")
    )

    if lap_summary.empty:
        return None

    return int(lap_summary.iloc[0]["lap"])


def get_lap_data(df: pd.DataFrame, lap_number: int) -> pd.DataFrame:
    """
    Return data for one lap.
    """
    if df.empty or "lap" not in df.columns:
        return pd.DataFrame()

    return df[df["lap"].astype(int) == int(lap_number)].copy()


def get_best_lap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return telemetry for the best lap.
    """
    best_lap = get_best_lap_number(df)

    if best_lap is None:
        return pd.DataFrame()

    return get_lap_data(df, best_lap)