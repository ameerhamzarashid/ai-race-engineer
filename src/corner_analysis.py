import pandas as pd


def corner_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate performance metrics for each corner.
    """
    if df.empty or "corner" not in df.columns:
        return pd.DataFrame()

    rows = []

    for lap, lap_df in df.groupby("lap"):
        for corner, corner_df in lap_df.groupby("corner"):
            if corner_df.empty:
                continue

            brake_points = corner_df[corner_df["brake"] > 10]
            throttle_points = corner_df[corner_df["throttle"] > 50]

            brake_start = (
                float(brake_points["distance"].min())
                if not brake_points.empty
                else None
            )

            throttle_pickup = (
                float(throttle_points["distance"].min())
                if not throttle_points.empty
                else None
            )

            rows.append(
                {
                    "lap": int(lap),
                    "corner": corner,
                    "entry_speed": float(corner_df.head(10)["speed"].mean()),
                    "min_speed": float(corner_df["speed"].min()),
                    "exit_speed": float(corner_df.tail(10)["speed"].mean()),
                    "avg_speed": float(corner_df["speed"].mean()),
                    "max_brake": float(corner_df["brake"].max()),
                    "avg_throttle": float(corner_df["throttle"].mean()),
                    "steering_stability": float(corner_df["steering"].std()),
                    "brake_start": brake_start,
                    "throttle_pickup": throttle_pickup,
                }
            )

    return pd.DataFrame(rows)


def compare_corners_to_best(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare every lap corner with the best lap corner reference.
    """
    metrics = corner_metrics(df)

    if metrics.empty:
        return pd.DataFrame()

    best_lap = int(
        df.groupby("lap")["lap_time"]
        .first()
        .sort_values()
        .index[0]
    )

    best_metrics = metrics[metrics["lap"] == best_lap].copy()
    other_metrics = metrics.copy()

    merged = other_metrics.merge(
        best_metrics,
        on="corner",
        suffixes=("", "_best"),
        how="left",
    )

    merged["min_speed_loss"] = merged["min_speed_best"] - merged["min_speed"]
    merged["exit_speed_loss"] = merged["exit_speed_best"] - merged["exit_speed"]
    merged["entry_speed_diff"] = merged["entry_speed"] - merged["entry_speed_best"]

    merged["estimated_corner_loss"] = (
        merged["min_speed_loss"].clip(lower=0) * 0.012
        + merged["exit_speed_loss"].clip(lower=0) * 0.018
        + merged["steering_stability"].clip(lower=0) * 0.003
    )

    return merged.sort_values(["lap", "estimated_corner_loss"], ascending=[True, False])