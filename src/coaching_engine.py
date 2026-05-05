import pandas as pd

from src.mistake_detector import detect_corner_mistakes, mistake_summary


def coaching_message_for_mistake(mistake: str) -> str:
    """
    Convert mistake labels into race engineer advice.
    """
    messages = {
        "Late braking": "Brake slightly earlier and focus on stabilising the car before turn-in.",
        "Early braking": "You are braking too early. Try moving the braking point a few metres later while staying smooth.",
        "Over-slowing": "You are carrying too little minimum speed. Release the brake more progressively and keep momentum.",
        "Poor corner exit": "Prioritise exit speed. Open the steering earlier before applying full throttle.",
        "Late throttle pickup": "Start feeding in throttle earlier after the apex to improve exit speed.",
        "Unstable steering": "Smooth your steering input. Too much correction scrubs speed and unsettles the car.",
        "Clean corner": "Good corner. Keep repeating this rhythm.",
    }

    return messages.get(mistake, "Focus on smoother inputs and more consistent corner execution.")


def generate_corner_feedback(mistakes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate feedback for every detected mistake.
    """
    if mistakes_df.empty:
        return pd.DataFrame()

    rows = []

    for _, row in mistakes_df.iterrows():
        mistake_list = [m.strip() for m in row["mistakes"].split(",")]

        feedback_items = [
            coaching_message_for_mistake(mistake)
            for mistake in mistake_list
        ]

        rows.append(
            {
                "lap": row["lap"],
                "corner": row["corner"],
                "mistakes": row["mistakes"],
                "estimated_time_loss": row["estimated_time_loss"],
                "feedback": " ".join(feedback_items),
            }
        )

    return pd.DataFrame(rows)


def generate_session_report(df: pd.DataFrame) -> dict:
    """
    Generate full AI race engineer style session report.
    """
    mistakes_df = detect_corner_mistakes(df)
    summary_df = mistake_summary(mistakes_df)

    if df.empty:
        return {
            "headline": "No telemetry data available.",
            "strength": "N/A",
            "weakness": "N/A",
            "main_advice": "Upload valid telemetry data.",
            "detailed_feedback": [],
        }

    lap_times = df.groupby("lap")["lap_time"].first()
    best_lap = int(lap_times.idxmin())
    best_lap_time = float(lap_times.min())
    avg_lap_time = float(lap_times.mean())

    if summary_df.empty:
        headline = "Clean session with no major repeated mistakes detected."
        strength = "Good consistency and stable corner execution."
        weakness = "No major weakness detected from the current rules."
        main_advice = "Keep building consistency and compare against faster reference laps."
        top_mistakes = []
    else:
        top = summary_df.iloc[0]
        main_mistake = top["mistake"]

        headline = (
            f"Your main performance loss came from {main_mistake.lower()}."
        )

        strength = "You showed usable pace, especially on cleaner laps with smoother inputs."
        weakness = f"The most repeated issue was {main_mistake.lower()}."
        main_advice = coaching_message_for_mistake(main_mistake)
        top_mistakes = summary_df.head(3).to_dict(orient="records")

    detailed_feedback = []

    if not mistakes_df.empty:
        worst = mistakes_df.sort_values(
            "estimated_time_loss",
            ascending=False,
        ).head(5)

        for _, row in worst.iterrows():
            detailed_feedback.append(
                {
                    "lap": int(row["lap"]),
                    "corner": row["corner"],
                    "mistakes": row["mistakes"],
                    "time_loss": row["estimated_time_loss"],
                    "advice": " ".join(
                        coaching_message_for_mistake(m.strip())
                        for m in row["mistakes"].split(",")
                    ),
                }
            )

    return {
        "headline": headline,
        "best_lap": best_lap,
        "best_lap_time": best_lap_time,
        "avg_lap_time": avg_lap_time,
        "strength": strength,
        "weakness": weakness,
        "main_advice": main_advice,
        "top_mistakes": top_mistakes,
        "detailed_feedback": detailed_feedback,
    }