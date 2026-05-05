import streamlit as st

from src.coaching_engine import generate_corner_feedback, generate_session_report
from src.data_loader import load_sample_telemetry
from src.mistake_detector import detect_corner_mistakes
from src.scoring import calculate_driver_score
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
    <div class="subtitle">Race engineer style performance summary generated from telemetry patterns.</div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

report = generate_session_report(df)
scores = calculate_driver_score(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Overall Score", f"{scores['overall_score']}/100")
col2.metric("Pace Score", f"{scores['pace_score']}/100")
col3.metric("Consistency", f"{scores['consistency_score']}/100")
col4.metric("Control", f"{scores['control_score']}/100")

st.markdown(
    f"""
    <div class="engineer-box">
        <h3>Race Engineer Summary</h3>
        <p><strong>{report['headline']}</strong></p>
        <p><strong>Best lap:</strong> Lap {report['best_lap']} - {format_seconds(report['best_lap_time'])}</p>
        <p><strong>Average lap:</strong> {format_seconds(report['avg_lap_time'])}</p>
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

st.subheader("Top Mistakes")

if report["top_mistakes"]:
    st.dataframe(
        report["top_mistakes"],
        use_container_width=True,
    )
else:
    st.success("No major repeated mistakes detected.")

st.subheader("Worst Corner Feedback")

for item in report["detailed_feedback"]:
    st.markdown(
        f"""
        <div class="danger-box">
            <h4>Lap {item['lap']} - {item['corner']}</h4>
            <p><strong>Mistake:</strong> {item['mistakes']}</p>
            <p><strong>Estimated loss:</strong> {item['time_loss']}s</p>
            <p>{item['advice']}</p>
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