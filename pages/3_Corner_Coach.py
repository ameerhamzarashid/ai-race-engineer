import streamlit as st

from src.corner_analysis import compare_corners_to_best, corner_metrics
from src.data_loader import get_lap_numbers, load_sample_telemetry
from src.telemetry_cleaning import clean_telemetry
from src.utils import inject_racing_css
from src.visualizations import plot_corner_loss

st.set_page_config(
    page_title="Corner Coach",
    page_icon="🧠",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">Corner Coach</div>
    <div class="subtitle">Compare every corner against your best lap reference.</div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

lap_numbers = get_lap_numbers(df)

selected_lap = st.sidebar.selectbox(
    "Select lap to inspect",
    lap_numbers,
    index=0,
)

corner_df = compare_corners_to_best(df)

if corner_df.empty:
    st.error("No corner analysis available.")
    st.stop()

selected_corner_df = corner_df[corner_df["lap"] == selected_lap].copy()

st.subheader(f"Corner Analysis for Lap {selected_lap}")

st.plotly_chart(
    plot_corner_loss(selected_corner_df),
    use_container_width=True,
)

display_cols = [
    "corner",
    "entry_speed",
    "min_speed",
    "exit_speed",
    "avg_speed",
    "min_speed_best",
    "exit_speed_best",
    "min_speed_loss",
    "exit_speed_loss",
    "estimated_corner_loss",
]

available_cols = [col for col in display_cols if col in selected_corner_df.columns]

st.dataframe(
    selected_corner_df[available_cols].round(3),
    use_container_width=True,
)

st.subheader("Worst Corners Overall")

worst = corner_df.sort_values(
    "estimated_corner_loss",
    ascending=False,
).head(10)

st.dataframe(
    worst[available_cols + ["lap"]].round(3),
    use_container_width=True,
)

with st.expander("Raw corner metrics"):
    metrics = corner_metrics(df)
    st.dataframe(
        metrics.round(3),
        use_container_width=True,
    )