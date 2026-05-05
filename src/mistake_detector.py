import pandas as pd

from src.advanced_analysis import advanced_corner_analysis


def classify_mistakes(row: pd.Series) -> tuple[list[str], int]:
    """
    Convert advanced corner comparison metrics into mistake labels.
    Returns:
    - list of mistakes
    - severity score
    """
    mistakes = []
    severity = 0

    brake_start_delta = row.get("brake_start_delta")
    brake_release_delta = row.get("brake_release_delta")
    throttle_pickup_delta = row.get("throttle_pickup_delta")

    if pd.notna(brake_start_delta):
        if brake_start_delta > 10:
            mistakes.append("Late braking")
            severity += 2
        elif brake_start_delta < -18:
            mistakes.append("Early braking")
            severity += 1

    if pd.notna(brake_release_delta):
        if brake_release_delta > 14:
            mistakes.append("Late brake release")
            severity += 2

    if row.get("min_speed_loss", 0) > 8:
        mistakes.append("Over-slowing")
        severity += 2

    if row.get("apex_speed_loss", 0) > 8:
        mistakes.append("Low apex speed")
        severity += 2

    if row.get("exit_speed_loss", 0) > 7:
        mistakes.append("Poor corner exit")
        severity += 2

    if pd.notna(throttle_pickup_delta):
        if throttle_pickup_delta > 15:
            mistakes.append("Late throttle pickup")
            severity += 2

    if row.get("steering_instability_delta", 0) > 6:
        mistakes.append("Unstable steering")
        severity += 1

    if row.get("coasting_delta", 0) > 10:
        mistakes.append("Too much coasting")
        severity += 1

    if row.get("overlap_delta", 0) > 8:
        mistakes.append("Brake and throttle overlap")
        severity += 1

    if not mistakes:
        mistakes.append("Clean corner")
        severity = 0

    return mistakes, severity


def primary_mistake_from_row(row: pd.Series) -> str:
    """
    Decide the main mistake based on the largest loss phase and metrics.
    """
    phase = row.get("main_loss_phase", "Unknown")

    if phase == "Entry":
        if row.get("brake_start_delta", 0) > 10:
            return "Late braking"
        if row.get("brake_start_delta", 0) < -18:
            return "Early braking"
        return "Entry speed loss"

    if phase == "Apex":
        if row.get("min_speed_loss", 0) > 8:
            return "Over-slowing"
        return "Low apex speed"

    if phase == "Exit":
        if row.get("throttle_pickup_delta", 0) > 15:
            return "Late throttle pickup"
        if row.get("exit_speed_loss", 0) > 7:
            return "Poor corner exit"
        return "Exit speed loss"

    return "General inconsistency"


def detect_corner_mistakes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stage 2 mistake detector.

    Uses best lap reference comparison and phase-based corner metrics.
    Keeps the old output columns so existing pages still work.
    """
    analysis = advanced_corner_analysis(df)

    if analysis.empty:
        return pd.DataFrame()

    rows = []

    for _, row in analysis.iterrows():
        if bool(row["is_best_lap"]):
            continue

        mistakes, severity = classify_mistakes(row)
        primary_mistake = primary_mistake_from_row(row)

        rows.append(
            {
                "lap": int(row["lap"]),
                "corner": row["corner"],
                "mistakes": ", ".join(mistakes),
                "primary_mistake": primary_mistake,
                "severity": int(severity),
                "main_loss_phase": row.get("main_loss_phase", "Unknown"),
                "estimated_time_loss": round(float(row.get("estimated_time_loss", 0)), 3),
                "entry_loss": round(float(row.get("entry_loss_estimate", 0)), 3),
                "apex_loss": round(float(row.get("apex_loss_estimate", 0)), 3),
                "exit_loss": round(float(row.get("exit_loss_estimate", 0)), 3),
                "entry_speed_loss": round(float(row.get("entry_speed_loss", 0)), 2),
                "apex_speed_loss": round(float(row.get("apex_speed_loss", 0)), 2),
                "min_speed_loss": round(float(row.get("min_speed_loss", 0)), 2),
                "exit_speed_loss": round(float(row.get("exit_speed_loss", 0)), 2),
                "brake_start_delta": round(float(row.get("brake_start_delta", 0)), 2)
                if pd.notna(row.get("brake_start_delta"))
                else None,
                "brake_release_delta": round(float(row.get("brake_release_delta", 0)), 2)
                if pd.notna(row.get("brake_release_delta"))
                else None,
                "throttle_pickup_delta": round(float(row.get("throttle_pickup_delta", 0)), 2)
                if pd.notna(row.get("throttle_pickup_delta"))
                else None,
                "steering_instability": round(float(row.get("steering_stability", 0)), 2),
            }
        )

    return pd.DataFrame(rows)


def mistake_summary(mistakes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise mistake frequency, severity and estimated time loss.
    """
    if mistakes_df.empty:
        return pd.DataFrame()

    rows = []

    for _, row in mistakes_df.iterrows():
        mistake_list = [m.strip() for m in row["mistakes"].split(",")]

        for mistake in mistake_list:
            if mistake == "Clean corner":
                continue

            rows.append(
                {
                    "mistake": mistake,
                    "severity": row["severity"],
                    "estimated_time_loss": row["estimated_time_loss"],
                    "main_loss_phase": row.get("main_loss_phase", "Unknown"),
                }
            )

    if not rows:
        return pd.DataFrame()

    out = pd.DataFrame(rows)

    summary = (
        out.groupby("mistake", as_index=False)
        .agg(
            count=("mistake", "count"),
            avg_severity=("severity", "mean"),
            total_time_loss=("estimated_time_loss", "sum"),
        )
        .sort_values("total_time_loss", ascending=False)
    )

    return summary


def priority_improvements(mistakes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank the top improvement priorities.
    """
    summary = mistake_summary(mistakes_df)

    if summary.empty:
        return pd.DataFrame()

    summary = summary.copy()

    summary["priority_score"] = (
        summary["total_time_loss"] * 2
        + summary["count"] * 0.5
        + summary["avg_severity"] * 0.75
    )

    summary = summary.sort_values("priority_score", ascending=False)

    summary["priority"] = range(1, len(summary) + 1)

    return summary[
        [
            "priority",
            "mistake",
            "count",
            "avg_severity",
            "total_time_loss",
            "priority_score",
        ]
    ]