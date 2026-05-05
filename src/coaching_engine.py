import pandas as pd

from src.advanced_analysis import lap_loss_summary, top_loss_corners
from src.mistake_detector import (
    detect_corner_mistakes,
    mistake_summary,
    priority_improvements,
)


def coaching_message_for_mistake(mistake: str) -> str:
    """
    Convert mistake labels into clear race engineer advice.
    """
    messages = {
        "Late braking": "Brake a few metres earlier and prioritise car stability before turn-in.",
        "Early braking": "You are giving away time before the corner. Move the braking point slightly later while keeping the brake pressure smooth.",
        "Late brake release": "Release the brake more progressively before apex. Holding brake too long is reducing minimum speed.",
        "Over-slowing": "You are carrying too little minimum speed. Ease off the brake earlier and keep more momentum through the apex.",
        "Low apex speed": "Focus on maintaining a stronger rolling speed at the apex without adding steering corrections.",
        "Poor corner exit": "Prioritise exit speed. Open the steering earlier and build throttle more confidently after the apex.",
        "Late throttle pickup": "Start feeding in throttle earlier after the apex. Avoid waiting too long once the car is rotated.",
        "Unstable steering": "Smooth the steering input. Too many corrections scrub speed and make throttle application harder.",
        "Too much coasting": "Reduce coasting time. Be more decisive between braking, rotation and throttle pickup.",
        "Brake and throttle overlap": "Avoid pressing brake and throttle together unless intentionally balancing the car.",
        "Entry speed loss": "Carry more confidence into corner entry while keeping the car stable.",
        "Exit speed loss": "Focus on throttle timing and steering release to improve exit speed.",
        "General inconsistency": "Aim for repeatable braking points, smoother steering and cleaner throttle application.",
        "Clean corner": "Good corner. Keep repeating this rhythm.",
    }

    return messages.get(
        mistake,
        "Focus on smoother inputs, cleaner rotation and more consistent corner execution.",
    )


def coaching_drill_for_mistake(mistake: str) -> str:
    """
    Convert mistake into a practical training drill.
    """
    drills = {
        "Late braking": "Brake marker drill: choose a fixed braking board and brake 5 metres earlier for 5 laps, then move later gradually.",
        "Early braking": "Confidence drill: move your braking point 3 metres later each lap until the car starts to feel unstable.",
        "Late brake release": "Trail-brake release drill: focus on reducing brake pressure smoothly as steering angle increases.",
        "Over-slowing": "Minimum speed drill: use one gear higher through the corner and aim to carry 3 to 5 km/h more apex speed.",
        "Low apex speed": "Apex rolling speed drill: avoid sudden brake release and focus on keeping the car balanced through the middle.",
        "Poor corner exit": "Exit priority drill: sacrifice a little entry speed and focus only on earlier throttle and straighter steering on exit.",
        "Late throttle pickup": "Throttle timing drill: begin with 20 percent throttle just after apex, then build smoothly to full throttle.",
        "Unstable steering": "Smooth hands drill: reduce steering corrections and aim for one clean steering input into the corner.",
        "Too much coasting": "No-coast drill: make sure every corner phase has a clear action, braking, rotating or accelerating.",
        "Brake and throttle overlap": "Pedal discipline drill: practise clean brake release before throttle application.",
    }

    return drills.get(
        mistake,
        "Consistency drill: repeat the same braking marker, apex and throttle pickup point for 5 consecutive laps.",
    )


def generate_corner_feedback(mistakes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate feedback for every detected mistake row.
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
                "main_loss_phase": row.get("main_loss_phase", "Unknown"),
                "primary_mistake": row.get("primary_mistake", "Unknown"),
                "mistakes": row["mistakes"],
                "estimated_time_loss": row["estimated_time_loss"],
                "feedback": " ".join(feedback_items),
            }
        )

    return pd.DataFrame(rows)


def generate_lap_feedback(df: pd.DataFrame, lap_number: int) -> str:
    """
    Generate a race engineer style paragraph for one lap.
    """
    mistakes_df = detect_corner_mistakes(df)

    if mistakes_df.empty:
        return "No major mistakes were detected for this lap."

    lap_df = mistakes_df[mistakes_df["lap"] == int(lap_number)].copy()

    if lap_df.empty:
        return "This appears to be the reference lap or there is no major issue detected."

    total_loss = lap_df["estimated_time_loss"].sum()

    worst_corners = (
        lap_df.sort_values("estimated_time_loss", ascending=False)
        .head(3)["corner"]
        .tolist()
    )

    primary = (
        lap_df[lap_df["primary_mistake"] != "General inconsistency"]
        ["primary_mistake"]
        .mode()
    )

    main_issue = primary.iloc[0] if not primary.empty else "general inconsistency"

    advice = coaching_message_for_mistake(main_issue)

    return (
        f"Lap {lap_number} lost an estimated {total_loss:.2f}s compared with the best reference lap. "
        f"The biggest losses came from {', '.join(worst_corners)}. "
        f"The main pattern is {main_issue.lower()}. {advice}"
    )


def generate_session_report(df: pd.DataFrame) -> dict:
    """
    Generate a full Stage 2 race engineer report.
    """
    mistakes_df = detect_corner_mistakes(df)
    summary_df = mistake_summary(mistakes_df)
    priority_df = priority_improvements(mistakes_df)
    lap_loss_df = lap_loss_summary(df)
    top_corners_df = top_loss_corners(df, n=5)

    if df.empty:
        return {
            "headline": "No telemetry data available.",
            "strength": "N/A",
            "weakness": "N/A",
            "main_advice": "Upload valid telemetry data.",
            "best_lap": None,
            "best_lap_time": None,
            "avg_lap_time": None,
            "top_mistakes": [],
            "priorities": [],
            "detailed_feedback": [],
            "lap_feedback": [],
        }

    lap_times = df.groupby("lap")["lap_time"].first().dropna()

    best_lap = int(lap_times.idxmin())
    best_lap_time = float(lap_times.min())
    avg_lap_time = float(lap_times.mean())

    if summary_df.empty:
        headline = "Clean session with no major repeated mistakes detected."
        strength = "Your inputs are reasonably consistent and the car is staying stable through most corners."
        weakness = "No major repeated weakness was detected by the current rule engine."
        main_advice = "Keep building repeatability and compare against faster reference laps."
        top_mistakes = []
        priorities = []
    else:
        top = summary_df.iloc[0]
        main_mistake = top["mistake"]

        total_loss = mistakes_df["estimated_time_loss"].sum()

        headline = (
            f"Main performance loss: {main_mistake}. "
            f"Estimated total loss across analysed laps: {total_loss:.2f}s."
        )

        strength = identify_strength(df, mistakes_df)
        weakness = f"The most important weakness is {main_mistake.lower()}."
        main_advice = coaching_message_for_mistake(main_mistake)

        top_mistakes = summary_df.head(5).round(3).to_dict(orient="records")
        priorities = priority_df.head(5).round(3).to_dict(orient="records")

    detailed_feedback = []

    if not top_corners_df.empty:
        for _, row in top_corners_df.iterrows():
            lap = int(row["lap"])
            corner = row["corner"]

            matching = mistakes_df[
                (mistakes_df["lap"] == lap)
                & (mistakes_df["corner"] == corner)
            ]

            if matching.empty:
                continue

            mistake_row = matching.iloc[0]
            primary = mistake_row.get("primary_mistake", "General inconsistency")

            detailed_feedback.append(
                {
                    "lap": lap,
                    "corner": corner,
                    "main_loss_phase": mistake_row.get("main_loss_phase", "Unknown"),
                    "mistakes": mistake_row["mistakes"],
                    "time_loss": mistake_row["estimated_time_loss"],
                    "advice": coaching_message_for_mistake(primary),
                }
            )

    lap_feedback = []

    if not lap_loss_df.empty:
        worst_laps = (
            lap_loss_df.sort_values("estimated_total_loss", ascending=False)
            .head(3)["lap"]
            .tolist()
        )

        for lap in worst_laps:
            lap_feedback.append(
                {
                    "lap": int(lap),
                    "feedback": generate_lap_feedback(df, int(lap)),
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
        "priorities": priorities,
        "detailed_feedback": detailed_feedback,
        "lap_feedback": lap_feedback,
    }


def identify_strength(df: pd.DataFrame, mistakes_df: pd.DataFrame) -> str:
    """
    Identify a positive driver strength from telemetry behaviour.
    """
    if df.empty:
        return "No telemetry available."

    avg_throttle = df["throttle"].mean()
    steering_std = df["steering"].std()
    brake_mean = df["brake"].mean()

    if not mistakes_df.empty:
        mistake_text = " ".join(mistakes_df["mistakes"].tolist())

        if "Poor corner exit" not in mistake_text and avg_throttle > 55:
            return "Your throttle commitment is strong and corner exits are generally confident."

        if "Unstable steering" not in mistake_text and steering_std < 18:
            return "Your steering inputs are relatively stable, which helps keep the car balanced."

        if "Late braking" not in mistake_text and brake_mean > 8:
            return "Your braking references are mostly controlled and repeatable."

    return "Your best laps show good pace potential when the inputs are smooth and repeatable."


def generate_training_plan(df: pd.DataFrame) -> dict:
    """
    Generate a Stage 2 training plan from mistake priorities.
    """
    mistakes_df = detect_corner_mistakes(df)
    priority_df = priority_improvements(mistakes_df)

    if priority_df.empty:
        return {
            "focus": "Consistency building",
            "summary": "No major repeated weakness was detected. Focus on repeatability.",
            "drills": [
                {
                    "priority": 1,
                    "mistake": "Consistency",
                    "drill": "Repeat the same braking point, apex and throttle pickup for 5 consecutive laps.",
                    "target": "Keep lap time variation below 0.5 seconds.",
                }
            ],
        }

    drills = []

    for _, row in priority_df.head(5).iterrows():
        mistake = row["mistake"]

        drills.append(
            {
                "priority": int(row["priority"]),
                "mistake": mistake,
                "drill": coaching_drill_for_mistake(mistake),
                "target": target_for_mistake(mistake),
            }
        )

    top_focus = priority_df.iloc[0]["mistake"]

    return {
        "focus": top_focus,
        "summary": (
            f"Your next practice session should focus mainly on {top_focus.lower()}. "
            "Work on one issue at a time instead of trying to fix everything in one lap."
        ),
        "drills": drills,
    }


def target_for_mistake(mistake: str) -> str:
    """
    Give measurable improvement target for each mistake.
    """
    targets = {
        "Late braking": "Reduce late braking deltas to under 5 metres.",
        "Early braking": "Reduce early braking by moving the marker 3 to 5 metres later.",
        "Late brake release": "Reduce brake release delay to under 8 metres.",
        "Over-slowing": "Increase minimum speed by 3 to 5 km/h.",
        "Low apex speed": "Improve apex speed by at least 3 km/h.",
        "Poor corner exit": "Improve exit speed by 5 km/h.",
        "Late throttle pickup": "Start throttle pickup 8 to 12 metres earlier.",
        "Unstable steering": "Reduce steering corrections through the apex.",
        "Too much coasting": "Reduce coasting points by at least 30 percent.",
        "Brake and throttle overlap": "Keep pedal overlap near zero in normal corners.",
    }

    return targets.get(
        mistake,
        "Improve consistency and reduce repeated time loss.",
    )