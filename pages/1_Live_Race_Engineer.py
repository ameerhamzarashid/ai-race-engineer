import streamlit as st

from src.coaching_engine import coaching_message_for_mistake
from src.data_loader import load_sample_telemetry
from src.live_replay import current_status, get_replay_frame, get_replay_window
from src.mistake_detector import detect_corner_mistakes
from src.telemetry_cleaning import clean_telemetry
from src.utils import inject_racing_css
from src.visualizations import gauge_chart, gear_indicator, telemetry_line_chart

st.set_page_config(
    page_title="Live Race Engineer",
    page_icon="🏎️",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">Live Race Engineer</div>
    <div class="subtitle">Simulated real-time telemetry replay with live coaching feedback.</div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

if "frame_index" not in st.session_state:
    st.session_state.frame_index = 0

replay_speed = st.sidebar.slider(
    "Replay step size",
    min_value=1,
    max_value=30,
    value=8,
)

if st.sidebar.button("Next telemetry frame"):
    st.session_state.frame_index += replay_speed

if st.sidebar.button("Reset replay"):
    st.session_state.frame_index = 0

auto_mode = st.sidebar.checkbox("Auto advance on refresh", value=False)

if auto_mode:
    st.session_state.frame_index += replay_speed

row = get_replay_frame(df, st.session_state.frame_index)
window_df = get_replay_window(df, st.session_state.frame_index)

if row is None:
    st.error("No telemetry data available.")
    st.stop()

status = current_status(row)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.plotly_chart(
        gauge_chart(row["speed"], "Speed km/h", max_value=320),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        gauge_chart(row["throttle"], "Throttle %", max_value=100),
        use_container_width=True,
    )

with col3:
    st.plotly_chart(
        gauge_chart(row["brake"], "Brake %", max_value=100),
        use_container_width=True,
    )

with col4:
    st.plotly_chart(
        gear_indicator(int(row["gear"])),
        use_container_width=True,
    )

c1, c2, c3, c4 = st.columns(4)

c1.metric("Lap", int(row["lap"]))
c2.metric("Corner", row["corner"])
c3.metric("RPM", int(row["rpm"]))
c4.metric("Status", status)

st.plotly_chart(
    telemetry_line_chart(window_df),
    use_container_width=True,
)

mistakes_df = detect_corner_mistakes(df)

current_lap = int(row["lap"])
current_corner = row["corner"]

current_mistakes = mistakes_df[
    (mistakes_df["lap"] == current_lap)
    & (mistakes_df["corner"] == current_corner)
]

st.subheader("Race Engineer Radio")

if current_mistakes.empty:
    st.markdown(
        """
        <div class="success-box">
            <h4>Clean so far</h4>
            <p>No major issue detected in this corner window. Keep the inputs smooth.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    worst = current_mistakes.sort_values(
        "severity",
        ascending=False,
    ).iloc[0]

    mistake = worst["mistakes"].split(",")[0].strip()
    advice = coaching_message_for_mistake(mistake)

    box_class = "danger-box" if worst["severity"] >= 3 else "warning-box"

    st.markdown(
        f"""
        <div class="{box_class}">
            <h4>{worst['mistakes']}</h4>
            <p><strong>Estimated loss:</strong> {worst['estimated_time_loss']}s</p>
            <p>{advice}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "This first build uses button-based replay. Later we can upgrade it to real WebSocket or simulator telemetry."
)