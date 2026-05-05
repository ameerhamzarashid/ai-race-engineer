import streamlit as st

from src.data_loader import load_uploaded_telemetry, validate_telemetry_columns
from src.telemetry_cleaning import clean_telemetry
from src.utils import inject_racing_css
from src.visualizations import plot_inputs_trace, plot_speed_trace, plot_track_map

st.set_page_config(
    page_title="Upload Telemetry",
    page_icon="📁",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">Upload Telemetry</div>
    <div class="subtitle">Upload your own sim racing telemetry CSV file.</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    Required columns:

    `timestamp, lap, distance, speed, throttle, brake, steering, gear, rpm, x, y, sector, corner, lap_time`
    """
)

uploaded_file = st.file_uploader(
    "Upload telemetry CSV",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to preview and validate your telemetry.")
    st.stop()

try:
    df = load_uploaded_telemetry(uploaded_file)
except Exception as exc:
    st.error("Could not read uploaded CSV.")
    st.exception(exc)
    st.stop()

valid, missing = validate_telemetry_columns(df)

if not valid:
    st.error("Uploaded file is missing required columns.")
    st.write(missing)
    st.stop()

df = clean_telemetry(df)

st.success("Telemetry file loaded successfully.")

st.subheader("Data Preview")

st.dataframe(
    df.head(50),
    use_container_width=True,
)

lap_numbers = sorted(df["lap"].dropna().astype(int).unique().tolist())

selected_lap = st.selectbox(
    "Preview lap",
    lap_numbers,
)

lap_df = df[df["lap"].astype(int) == selected_lap]

tab1, tab2, tab3 = st.tabs(["Speed", "Inputs", "Track Map"])

with tab1:
    st.plotly_chart(
        plot_speed_trace(lap_df),
        use_container_width=True,
    )

with tab2:
    st.plotly_chart(
        plot_inputs_trace(lap_df),
        use_container_width=True,
    )

with tab3:
    color_col = st.selectbox(
        "Color by",
        ["speed", "throttle", "brake", "gear"],
    )

    st.plotly_chart(
        plot_track_map(lap_df, color_col=color_col),
        use_container_width=True,
    )