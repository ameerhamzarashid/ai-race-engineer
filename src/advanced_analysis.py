import pandas as pd


def get_best_lap_number(df: pd.DataFrame) -> int | None:
    """
    Return the best lap number based on lowest lap_time.
    """
    if df.empty or "lap" not in df.columns or "lap_time" not in df.columns:
        return None

    lap_times = (
        df.groupby("lap")["lap_time"]
        .first()
        .dropna()
        .sort_values()
    )

    if lap_times.empty:
        return None

    return int(lap_times.index[0])


def calculate_corner_phase_metrics(corner_df: pd.DataFrame) -> dict:
    """
    Split one corner into entry, apex and exit phases.
    Calculates phase-based driving behaviour.
    """
    if corner_df.empty:
        return {}

    corner_df = corner_df.sort_values("distance").copy()

    total_rows = len(corner_df)

    if total_rows < 6:
        entry_df = corner_df
        apex_df = corner_df
        exit_df = corner_df
    else:
        entry_end = max(1, int(total_rows * 0.33))
        apex_end = max(entry_end + 1, int(total_rows * 0.66))

        entry_df = corner_df.iloc[:entry_end]
        apex_df = corner_df.iloc[entry_end:apex_end]
        exit_df = corner_df.iloc[apex_end:]

    brake_points = corner_df[corner_df["brake"] > 10]
    throttle_points = corner_df[corner_df["throttle"] > 50]

    brake_start = None
    brake_release = None
    throttle_pickup = None

    if not brake_points.empty:
        brake_start = float(brake_points["distance"].min())
        brake_release = float(brake_points["distance"].max())

    if not throttle_points.empty:
        throttle_pickup = float(throttle_points["distance"].min())

    coasting_points = corner_df[
        (corner_df["brake"] < 5)
        & (corner_df["throttle"] < 10)
    ]

    brake_throttle_overlap = corner_df[
        (corner_df["brake"] > 10)
        & (corner_df["throttle"] > 10)
    ]

    metrics = {
        "entry_speed": float(entry_df["speed"].mean()),
        "apex_speed": float(apex_df["speed"].min()),
        "exit_speed": float(exit_df["speed"].mean()),
        "avg_speed": float(corner_df["speed"].mean()),
        "min_speed": float(corner_df["speed"].min()),
        "max_speed": float(corner_df["speed"].max()),
        "avg_throttle": float(corner_df["throttle"].mean()),
        "avg_brake": float(corner_df["brake"].mean()),
        "max_brake": float(corner_df["brake"].max()),
        "steering_stability": float(corner_df["steering"].std()),
        "entry_steering_stability": float(entry_df["steering"].std()),
        "apex_steering_stability": float(apex_df["steering"].std()),
        "exit_steering_stability": float(exit_df["steering"].std()),
        "brake_start": brake_start,
        "brake_release": brake_release,
        "throttle_pickup": throttle_pickup,
        "coasting_points": int(len(coasting_points)),
        "brake_throttle_overlap_points": int(len(brake_throttle_overlap)),
        "samples": int(len(corner_df)),
    }

    return metrics


def advanced_corner_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare every lap and corner against the best lap reference.

    This gives:
    - Entry speed difference
    - Apex speed difference
    - Exit speed difference
    - Braking difference
    - Throttle pickup difference
    - Steering instability
    - Estimated time loss
    """
    if df.empty:
        return pd.DataFrame()

    required = [
        "lap",
        "corner",
        "distance",
        "speed",
        "throttle",
        "brake",
        "steering",
        "lap_time",
    ]

    for col in required:
        if col not in df.columns:
            return pd.DataFrame()

    best_lap = get_best_lap_number(df)

    if best_lap is None:
        return pd.DataFrame()

    rows = []

    for lap, lap_df in df.groupby("lap"):
        for corner, corner_df in lap_df.groupby("corner"):
            metrics = calculate_corner_phase_metrics(corner_df)

            if not metrics:
                continue

            row = {
                "lap": int(lap),
                "corner": corner,
                "is_best_lap": int(lap) == int(best_lap),
                **metrics,
            }

            rows.append(row)

    metrics_df = pd.DataFrame(rows)

    if metrics_df.empty:
        return pd.DataFrame()

    best_df = metrics_df[metrics_df["lap"] == best_lap].copy()

    comparison = metrics_df.merge(
        best_df,
        on="corner",
        suffixes=("", "_best"),
        how="left",
    )

    comparison["entry_speed_loss"] = (
        comparison["entry_speed_best"] - comparison["entry_speed"]
    )

    comparison["apex_speed_loss"] = (
        comparison["apex_speed_best"] - comparison["apex_speed"]
    )

    comparison["exit_speed_loss"] = (
        comparison["exit_speed_best"] - comparison["exit_speed"]
    )

    comparison["min_speed_loss"] = (
        comparison["min_speed_best"] - comparison["min_speed"]
    )

    comparison["steering_instability_delta"] = (
        comparison["steering_stability"] - comparison["steering_stability_best"]
    )

    comparison["entry_instability_delta"] = (
        comparison["entry_steering_stability"]
        - comparison["entry_steering_stability_best"]
    )

    comparison["apex_instability_delta"] = (
        comparison["apex_steering_stability"]
        - comparison["apex_steering_stability_best"]
    )

    comparison["exit_instability_delta"] = (
        comparison["exit_steering_stability"]
        - comparison["exit_steering_stability_best"]
    )

    comparison["brake_start_delta"] = (
        comparison["brake_start"] - comparison["brake_start_best"]
    )

    comparison["brake_release_delta"] = (
        comparison["brake_release"] - comparison["brake_release_best"]
    )

    comparison["throttle_pickup_delta"] = (
        comparison["throttle_pickup"] - comparison["throttle_pickup_best"]
    )

    comparison["coasting_delta"] = (
        comparison["coasting_points"] - comparison["coasting_points_best"]
    )

    comparison["overlap_delta"] = (
        comparison["brake_throttle_overlap_points"]
        - comparison["brake_throttle_overlap_points_best"]
    )

    comparison["entry_loss_estimate"] = (
        comparison["entry_speed_loss"].clip(lower=0) * 0.008
        + comparison["brake_start_delta"].clip(lower=0).fillna(0) * 0.004
        + comparison["entry_instability_delta"].clip(lower=0).fillna(0) * 0.006
    )

    comparison["apex_loss_estimate"] = (
        comparison["apex_speed_loss"].clip(lower=0) * 0.016
        + comparison["min_speed_loss"].clip(lower=0) * 0.010
        + comparison["apex_instability_delta"].clip(lower=0).fillna(0) * 0.006
    )

    comparison["exit_loss_estimate"] = (
        comparison["exit_speed_loss"].clip(lower=0) * 0.020
        + comparison["throttle_pickup_delta"].clip(lower=0).fillna(0) * 0.005
        + comparison["exit_instability_delta"].clip(lower=0).fillna(0) * 0.005
    )

    comparison["estimated_time_loss"] = (
        comparison["entry_loss_estimate"]
        + comparison["apex_loss_estimate"]
        + comparison["exit_loss_estimate"]
        + comparison["coasting_delta"].clip(lower=0).fillna(0) * 0.002
        + comparison["overlap_delta"].clip(lower=0).fillna(0) * 0.002
    )

    comparison["main_loss_phase"] = comparison[
        ["entry_loss_estimate", "apex_loss_estimate", "exit_loss_estimate"]
    ].idxmax(axis=1)

    comparison["main_loss_phase"] = comparison["main_loss_phase"].replace(
        {
            "entry_loss_estimate": "Entry",
            "apex_loss_estimate": "Apex",
            "exit_loss_estimate": "Exit",
        }
    )

    return comparison.sort_values(
        ["lap", "estimated_time_loss"],
        ascending=[True, False],
    )


def lap_loss_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise estimated loss by lap.
    """
    analysis = advanced_corner_analysis(df)

    if analysis.empty:
        return pd.DataFrame()

    out = (
        analysis[analysis["is_best_lap"] == False]
        .groupby("lap", as_index=False)
        .agg(
            estimated_total_loss=("estimated_time_loss", "sum"),
            entry_loss=("entry_loss_estimate", "sum"),
            apex_loss=("apex_loss_estimate", "sum"),
            exit_loss=("exit_loss_estimate", "sum"),
        )
        .sort_values("lap")
    )

    return out


def top_loss_corners(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Return worst corners by estimated time loss.
    """
    analysis = advanced_corner_analysis(df)

    if analysis.empty:
        return pd.DataFrame()

    return (
        analysis[analysis["is_best_lap"] == False]
        .sort_values("estimated_time_loss", ascending=False)
        .head(n)
    )