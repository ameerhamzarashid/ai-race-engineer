import streamlit as st

from src.coaching_engine import generate_session_report
from src.data_loader import load_sample_telemetry
from src.metrics import lap_summary, session_summary
from src.scoring import calculate_driver_score
from src.telemetry_cleaning import clean_telemetry
from src.utils import format_seconds, inject_racing_css
from src.visualizations import plot_lap_times, plot_track_map

st.set_page_config(
    page_title="AI Race Engineer",
    page_icon="🏁",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">AI Race Engineer</div>
    <div class="subtitle">
    Real-time sim racing telemetry coach built with Python, Streamlit and AI-style rule logic.
    </div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

summary = session_summary(df)
scores = calculate_driver_score(df)
report = generate_session_report(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="race-card">
            <div class="big-number">{scores['overall_score']}/100</div>
            <div class="metric-label">Driver Score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="race-card">
            <div class="big-number">{format_seconds(summary['best_lap'])}</div>
            <div class="metric-label">Best Lap</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="race-card">
            <div class="big-number">{round(summary['max_speed'], 1)}</div>
            <div class="metric-label">Max Speed km/h</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="race-card">
            <div class="big-number">{summary['laps']}</div>
            <div class="metric-label">Laps Analysed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="engineer-box">
        <h3>Race Engineer Summary</h3>
        <p><strong>{report['headline']}</strong></p>
        <p>{report['main_advice']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Project Modules")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="race-card">
            <h3 class="green-text">Live Race Engineer</h3>
            <p>Replay telemetry like a live session with speed, throttle, brake, gear and coaching status.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="race-card">
            <h3 class="info-text">Corner Coach</h3>
            <p>Find where time is lost through corner entry, apex and exit behaviour.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="race-card">
            <h3 class="warning-text">Mistake Detector</h3>
            <p>Detect late braking, over-slowing, poor exits and unstable steering.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Lap Time Overview")

laps_df = lap_summary(df)

st.plotly_chart(
    plot_lap_times(laps_df),
    use_container_width=True,
)

st.subheader("Track Map")

best_lap = int(laps_df.sort_values("lap_time").iloc[0]["lap"])
best_lap_df = df[df["lap"] == best_lap]

st.plotly_chart(
    plot_track_map(best_lap_df, color_col="speed"),
    use_container_width=True,
)

st.info(
    "Use the sidebar pages to open Live Race Engineer, Lap Analysis, Corner Coach, Mistake Detector, AI Coaching Report and Upload Telemetry."
)