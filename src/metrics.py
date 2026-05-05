import pandas as pd


def session_summary(df: pd.DataFrame) -> dict:
    """
    Calculate high-level session summary.
    """
    if df.empty:
        return {
            "laps": 0,
            "best_lap": None,
            "avg_lap": None,
            "max_speed": None,
            "avg_speed": None,
        }

    lap_times = df.groupby("lap")["lap_time"].first()

    return {
        "laps": int(df["lap"].nunique()),
        "best_lap": float(lap_times.min()),
        "avg_lap": float(lap_times.mean()),
        "max_speed": float(df["speed"].max()),
        "avg_speed": float(df["speed"].mean()),
    }


def lap_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise each lap.
    """
    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("lap", as_index=False)
        .agg(
            lap_time=("lap_time", "first"),
            max_speed=("speed", "max"),
            avg_speed=("speed", "mean"),
            avg_throttle=("throttle", "mean"),
            avg_brake=("brake", "mean"),
            steering_smoothness=("steering", "std"),
        )
        .sort_values("lap")
    )

    return summary


def sector_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise lap time proxy by sector.
    """
    if df.empty or "sector" not in df.columns:
        return pd.DataFrame()

    rows = []

    for lap, lap_df in df.groupby("lap"):
        for sector, sector_df in lap_df.groupby("sector"):
            rows.append(
                {
                    "lap": int(lap),
                    "sector": int(sector),
                    "avg_speed": float(sector_df["speed"].mean()),
                    "max_speed": float(sector_df["speed"].max()),
                    "avg_throttle": float(sector_df["throttle"].mean()),
                    "avg_brake": float(sector_df["brake"].mean()),
                }
            )

    return pd.DataFrame(rows)


def compare_lap_to_best(selected_lap: pd.DataFrame, best_lap: pd.DataFrame) -> dict:
    """
    Compare selected lap against best lap.
    """
    if selected_lap.empty or best_lap.empty:
        return {}

    selected_lap_time = selected_lap["lap_time"].iloc[0]
    best_lap_time = best_lap["lap_time"].iloc[0]

    return {
        "selected_lap": int(selected_lap["lap"].iloc[0]),
        "best_lap": int(best_lap["lap"].iloc[0]),
        "selected_lap_time": float(selected_lap_time),
        "best_lap_time": float(best_lap_time),
        "time_loss": float(selected_lap_time - best_lap_time),
        "selected_avg_speed": float(selected_lap["speed"].mean()),
        "best_avg_speed": float(best_lap["speed"].mean()),
        "selected_max_speed": float(selected_lap["speed"].max()),
        "best_max_speed": float(best_lap["speed"].max()),
    }