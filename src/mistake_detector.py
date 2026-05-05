import pandas as pd

from src.corner_analysis import compare_corners_to_best


def detect_corner_mistakes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect mistakes per corner by comparing each lap to best lap reference.
    """
    comparison = compare_corners_to_best(df)

    if comparison.empty:
        return pd.DataFrame()

    rows = []

    for _, row in comparison.iterrows():
        if row["lap"] == row["lap_best"]:
            continue

        mistakes = []

        severity = 0

        if row["min_speed_loss"] > 8:
            mistakes.append("Over-slowing")
            severity += 2

        if row["exit_speed_loss"] > 7:
            mistakes.append("Poor corner exit")
            severity += 2

        if row["steering_stability"] > row["steering_stability_best"] + 6:
            mistakes.append("Unstable steering")
            severity += 1

        if pd.notna(row["brake_start"]) and pd.notna(row["brake_start_best"]):
            if row["brake_start"] > row["brake_start_best"] + 10:
                mistakes.append("Late braking")
                severity += 2

            if row["brake_start"] < row["brake_start_best"] - 18:
                mistakes.append("Early braking")
                severity += 1

        if pd.notna(row["throttle_pickup"]) and pd.notna(row["throttle_pickup_best"]):
            if row["throttle_pickup"] > row["throttle_pickup_best"] + 15:
                mistakes.append("Late throttle pickup")
                severity += 2

        if not mistakes:
            mistakes.append("Clean corner")
            severity = 0

        rows.append(
            {
                "lap": int(row["lap"]),
                "corner": row["corner"],
                "mistakes": ", ".join(mistakes),
                "severity": severity,
                "estimated_time_loss": round(float(row["estimated_corner_loss"]), 3),
                "min_speed_loss": round(float(row["min_speed_loss"]), 2),
                "exit_speed_loss": round(float(row["exit_speed_loss"]), 2),
                "steering_stability": round(float(row["steering_stability"]), 2),
            }
        )

    return pd.DataFrame(rows)


def mistake_summary(mistakes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise mistake frequency.
    """
    if mistakes_df.empty:
        return pd.DataFrame()

    rows = []

    for _, row in mistakes_df.iterrows():
        mistake_list = [m.strip() for m in row["mistakes"].split(",")]

        for mistake in mistake_list:
            if mistake != "Clean corner":
                rows.append(
                    {
                        "mistake": mistake,
                        "severity": row["severity"],
                        "estimated_time_loss": row["estimated_time_loss"],
                    }
                )

    if not rows:
        return pd.DataFrame()

    out = pd.DataFrame(rows)

    return (
        out.groupby("mistake", as_index=False)
        .agg(
            count=("mistake", "count"),
            avg_severity=("severity", "mean"),
            total_time_loss=("estimated_time_loss", "sum"),
        )
        .sort_values("total_time_loss", ascending=False)
    )