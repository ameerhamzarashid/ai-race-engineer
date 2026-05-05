import streamlit as st

from src.coaching_engine import generate_training_plan
from src.data_loader import load_sample_telemetry
from src.mistake_detector import detect_corner_mistakes, priority_improvements
from src.telemetry_cleaning import clean_telemetry
from src.utils import inject_racing_css

st.set_page_config(
    page_title="Training Plan",
    page_icon="🏋️",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">Training Plan</div>
    <div class="subtitle">
    Personalised practice plan based on your most costly telemetry mistakes.
    </div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

plan = generate_training_plan(df)
mistakes_df = detect_corner_mistakes(df)
priority_df = priority_improvements(mistakes_df)

st.markdown(
    f"""
    <div class="engineer-box">
        <h3>Next Session Focus: {plan['focus']}</h3>
        <p>{plan['summary']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Priority Training Drills")

for drill in plan["drills"]:
    st.markdown(
        f"""
        <div class="race-card">
            <h4>Priority {drill['priority']}: {drill['mistake']}</h4>
            <p><strong>Drill:</strong> {drill['drill']}</p>
            <p><strong>Target:</strong> {drill['target']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Why These Drills Were Chosen")

if priority_df.empty:
    st.success("No major repeated issue detected.")
else:
    st.dataframe(
        priority_df.round(3),
        use_container_width=True,
    )

st.subheader("Detected Mistakes Behind the Plan")

if mistakes_df.empty:
    st.success("No mistake table available.")
else:
    st.dataframe(
        mistakes_df.sort_values(
            ["severity", "estimated_time_loss"],
            ascending=False,
        ),
        use_container_width=True,
    )

st.markdown(
    """
    <div class="engineer-box">
        <h4>How to use this plan</h4>
        <p>
        Do not try to fix every issue at once. Pick the first priority and drive 5 clean laps focusing only on that.
        After that, check whether the same mistake is still appearing in the Mistake Detector page.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)