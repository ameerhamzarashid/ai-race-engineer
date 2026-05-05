import streamlit as st

from src.advanced_analysis import lap_loss_summary, top_loss_corners
from src.coaching_engine import (
    generate_corner_feedback,
    generate_session_report,
)
from src.data_loader import load_sample_telemetry
from src.mistake_detector import detect_corner_mistakes, priority_improvements
from src.scoring import calculate_driver_score, score_explanation
from src.telemetry_cleaning import clean_telemetry
from src.utils import format_seconds, inject_racing_css

st.set_page_config(
    page_title="AI Coaching Report",
    page_icon="🎙️",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">AI Coaching Report</div>
    <div class="subtitle">
    Stage 2 race engineer summary with reference lap comparison, time loss and priority advice.
    </div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

report = generate_session_report(df)
scores = calculate_driver_score(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Overall", f"{scores['overall_score']}/100")
col2.metric("Pace", f"{scores['pace_score']}/100")
col3.metric("Consistency", f"{scores['consistency_score']}/100")
col4.metric("Control", f"{scores['control_score']}/100")
col5.metric("Racecraft", f"{scores['racecraft_score']}/100")

st.markdown(
    f"""
    <div class="engineer-box">
        <h3>Race Engineer Summary</h3>
        <p><strong>{report['headline']}</strong></p>
        <p><strong>Best lap:</strong> Lap {report['best_lap']} - {format_seconds(report['best_lap_time'])}</p>
        <p><strong>Average lap:</strong> {format_seconds(report['avg_lap_time'])}</p>
        <p>{score_explanation(scores)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        f"""
        <div class="success-box">
            <h4>Strength</h4>
            <p>{report['strength']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="warning-box">
            <h4>Main Weakness</h4>
            <p>{report['weakness']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="engineer-box">
        <h4>Main Improvement Advice</h4>
        <p>{report['main_advice']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Improvement Priorities")

priority_df = priority_improvements(detect_corner_mistakes(df))

if priority_df.empty:
    st.success("No major repeated priority issue detected.")
else:
    st.dataframe(
        priority_df.round(3),
        use_container_width=True,
    )

st.subheader("Lap Loss Summary")

lap_loss_df = lap_loss_summary(df)

if lap_loss_df.empty:
    st.info("Lap loss summary is not available.")
else:
    st.dataframe(
        lap_loss_df.round(3),
        use_container_width=True,
    )

st.subheader("Worst Corner Losses")

top_corners_df = top_loss_corners(df, n=10)

if top_corners_df.empty:
    st.info("No corner loss table available.")
else:
    display_cols = [
        "lap",
        "corner",
        "main_loss_phase",
        "entry_loss_estimate",
        "apex_loss_estimate",
        "exit_loss_estimate",
        "estimated_time_loss",
        "entry_speed_loss",
        "apex_speed_loss",
        "exit_speed_loss",
        "throttle_pickup_delta",
        "brake_start_delta",
    ]

    available_cols = [col for col in display_cols if col in top_corners_df.columns]

    st.dataframe(
        top_corners_df[available_cols].round(3),
        use_container_width=True,
    )

st.subheader("Worst Corner Feedback")

if not report["detailed_feedback"]:
    st.success("No major corner feedback generated.")
else:
    for item in report["detailed_feedback"]:
        st.markdown(
            f"""
            <div class="danger-box">
                <h4>Lap {item['lap']} - {item['corner']}</h4>
                <p><strong>Main loss phase:</strong> {item['main_loss_phase']}</p>
                <p><strong>Mistake:</strong> {item['mistakes']}</p>
                <p><strong>Estimated loss:</strong> {item['time_loss']}s</p>
                <p>{item['advice']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.subheader("Lap Engineer Notes")

if not report["lap_feedback"]:
    st.info("No lap feedback generated.")
else:
    for item in report["lap_feedback"]:
        st.markdown(
            f"""
            <div class="engineer-box">
                <h4>Lap {item['lap']}</h4>
                <p>{item['feedback']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.subheader("Full Coaching Table")

mistakes_df = detect_corner_mistakes(df)
feedback_df = generate_corner_feedback(mistakes_df)

if feedback_df.empty:
    st.info("No feedback generated.")
else:
    st.dataframe(
        feedback_df,
        use_container_width=True,
    )