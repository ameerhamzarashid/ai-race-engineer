import pandas as pd

from src.advanced_analysis import lap_loss_summary
from src.mistake_detector import detect_corner_mistakes


def calculate_driver_score(df: pd.DataFrame) -> dict:
    """
    Stage 2 driver performance score out of 100.

    Components:
    - Pace score
    - Consistency score
    - Control score
    - Race craft score
    - Mistake penalty
    """
    if df.empty:
        return {
            "overall_score": 0,
            "pace_score": 0,
            "consistency_score": 0,
            "control_score": 0,
            "racecraft_score": 0,
            "mistake_penalty": 0,
        }

    lap_times = df.groupby("lap")["lap_time"].first().dropna()

    if lap_times.empty:
        return {
            "overall_score": 0,
            "pace_score": 0,
            "consistency_score": 0,
            "control_score": 0,
            "racecraft_score": 0,
            "mistake_penalty": 0,
        }

    best = lap_times.min()
    avg = lap_times.mean()
    std = lap_times.std() if len(lap_times) > 1 else 0

    pace_loss = avg - best
    pace_score = max(0, 100 - pace_loss * 12)

    consistency_score = max(0, 100 - std * 22)

    steering_std = df["steering"].std()
    brake_smoothness = df["brake"].diff().abs().mean()
    throttle_smoothness = df["throttle"].diff().abs().mean()

    control_penalty = (
        steering_std * 0.28
        + brake_smoothness * 0.22
        + throttle_smoothness * 0.18
    )

    control_score = max(0, 100 - control_penalty)

    loss_df = lap_loss_summary(df)

    if loss_df.empty:
        avg_estimated_loss = 0
    else:
        avg_estimated_loss = loss_df["estimated_total_loss"].mean()

    racecraft_score = max(0, 100 - avg_estimated_loss * 10)

    mistakes_df = detect_corner_mistakes(df)

    if mistakes_df.empty:
        mistake_penalty = 0
    else:
        severe_events = mistakes_df[mistakes_df["severity"] >= 3]
        mistake_penalty = min(
            40,
            mistakes_df["severity"].sum() * 0.35
            + len(severe_events) * 0.75,
        )

    overall = (
        pace_score * 0.30
        + consistency_score * 0.25
        + control_score * 0.25
        + racecraft_score * 0.20
        - mistake_penalty
    )

    return {
        "overall_score": round(max(0, min(100, overall)), 1),
        "pace_score": round(max(0, min(100, pace_score)), 1),
        "consistency_score": round(max(0, min(100, consistency_score)), 1),
        "control_score": round(max(0, min(100, control_score)), 1),
        "racecraft_score": round(max(0, min(100, racecraft_score)), 1),
        "mistake_penalty": round(mistake_penalty, 1),
    }


def score_explanation(scores: dict) -> str:
    """
    Explain the score in simple language.
    """
    overall = scores.get("overall_score", 0)

    if overall >= 85:
        level = "excellent"
    elif overall >= 70:
        level = "strong"
    elif overall >= 55:
        level = "developing"
    else:
        level = "needs improvement"

    return (
        f"Overall performance is {level}. "
        f"Pace score is {scores.get('pace_score', 0)}/100, "
        f"consistency score is {scores.get('consistency_score', 0)}/100, "
        f"control score is {scores.get('control_score', 0)}/100, "
        f"and racecraft score is {scores.get('racecraft_score', 0)}/100."
    )