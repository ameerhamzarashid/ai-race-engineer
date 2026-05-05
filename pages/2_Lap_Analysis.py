import streamlit as st

from src.data_loader import get_best_lap_data, get_lap_data, get_lap_numbers, load_sample_telemetry
from src.metrics import compare_lap_to_best, lap_summary, sector_summary
from src.telemetry_cleaning import clean_telemetry
from src.utils import format_seconds, inject_racing_css
from src.visualizations import (
    plot_inputs_trace,
    plot_lap_times,
    plot_sector_summary,
    plot_speed_trace,
    plot_track_map,
)

st.set_page_config(
    page_title="Lap Analysis",
    page_icon="📊",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">Lap Analysis</div>
    <div class="subtitle">Analyse lap pace, speed trace, inputs and sector behaviour.</div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

lap_numbers = get_lap_numbers(df)

selected_lap_number = st.sidebar.selectbox(
    "Select lap",
    lap_numbers,
    index=0,
)

selected_lap = get_lap_data(df, selected_lap_number)
best_lap = get_best_lap_data(df)

comparison = compare_lap_to_best(selected_lap, best_lap)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Selected Lap", selected_lap_number)
col2.metric("Lap Time", format_seconds(comparison["selected_lap_time"]))
col3.metric("Best Lap", format_seconds(comparison["best_lap_time"]))
col4.metric("Time Loss", f"{comparison['time_loss']:.3f}s")

st.subheader("Lap Time Comparison")

laps_df = lap_summary(df)

st.plotly_chart(
    plot_lap_times(laps_df),
    use_container_width=True,
)

st.subheader("Selected Lap Telemetry")

tab1, tab2, tab3 = st.tabs(["Speed Trace", "Driver Inputs", "Track Map"])

with tab1:
    st.plotly_chart(
        plot_speed_trace(selected_lap),
        use_container_width=True,
    )

with tab2:
    st.plotly_chart(
        plot_inputs_trace(selected_lap),
        use_container_width=True,
    )

with tab3:
    color_col = st.selectbox(
        "Color track by",
        ["speed", "throttle", "brake", "gear"],
    )

    st.plotly_chart(
        plot_track_map(selected_lap, color_col=color_col),
        use_container_width=True,
    )

st.subheader("Sector Summary")

sector_df = sector_summary(df)

st.plotly_chart(
    plot_sector_summary(sector_df),
    use_container_width=True,
)

with st.expander("Lap summary table"):
    st.dataframe(
        laps_df.round(3),
        use_container_width=True,
    )