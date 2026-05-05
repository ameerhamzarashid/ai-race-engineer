import pandas as pd

from src.mistake_detector import detect_corner_mistakes


def calculate_driver_score(df: pd.DataFrame) -> dict:
    """
    Calculate driver performance score out of 100.
    """
    if df.empty:
        return {
            "overall_score": 0,
            "pace_score": 0,
            "consistency_score": 0,
            "control_score": 0,
            "mistake_penalty": 0,
        }

    lap_times = df.groupby("lap")["lap_time"].first()

    best = lap_times.min()
    avg = lap_times.mean()
    std = lap_times.std()

    pace_loss = avg - best
    pace_score = max(0, 100 - pace_loss * 15)

    consistency_score = max(0, 100 - std * 25) if pd.notna(std) else 70

    steering_std = df["steering"].std()
    brake_smoothness = df["brake"].diff().abs().mean()
    throttle_smoothness = df["throttle"].diff().abs().mean()

    control_penalty = (
        steering_std * 0.35
        + brake_smoothness * 0.25
        + throttle_smoothness * 0.20
    )

    control_score = max(0, 100 - control_penalty)

    mistakes_df = detect_corner_mistakes(df)

    if mistakes_df.empty:
        mistake_penalty = 0
    else:
        mistake_penalty = min(35, mistakes_df["severity"].sum() * 0.45)

    overall = (
        pace_score * 0.35
        + consistency_score * 0.30
        + control_score * 0.35
        - mistake_penalty
    )

    return {
        "overall_score": round(max(0, min(100, overall)), 1),
        "pace_score": round(max(0, min(100, pace_score)), 1),
        "consistency_score": round(max(0, min(100, consistency_score)), 1),
        "control_score": round(max(0, min(100, control_score)), 1),
        "mistake_penalty": round(mistake_penalty, 1),
    }