import streamlit as st

from src.data_loader import load_sample_telemetry
from src.mistake_detector import detect_corner_mistakes, mistake_summary
from src.telemetry_cleaning import clean_telemetry
from src.utils import inject_racing_css
from src.visualizations import plot_mistake_frequency, plot_mistake_timeline

st.set_page_config(
    page_title="Mistake Detector",
    page_icon="⚠️",
    layout="wide",
)

st.markdown(inject_racing_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-title">Mistake Detector</div>
    <div class="subtitle">Detect late braking, over-slowing, poor exits and unstable steering.</div>
    """,
    unsafe_allow_html=True,
)

df = clean_telemetry(load_sample_telemetry())

mistakes_df = detect_corner_mistakes(df)
summary_df = mistake_summary(mistakes_df)

if mistakes_df.empty:
    st.success("No mistakes detected.")
    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric("Mistake Events", len(mistakes_df[mistakes_df["severity"] > 0]))
col2.metric("Total Estimated Loss", f"{mistakes_df['estimated_time_loss'].sum():.3f}s")
col3.metric("Highest Severity", int(mistakes_df["severity"].max()))

st.subheader("Mistake Frequency")

st.plotly_chart(
    plot_mistake_frequency(summary_df),
    use_container_width=True,
)

st.subheader("Mistake Timeline")

st.plotly_chart(
    plot_mistake_timeline(mistakes_df),
    use_container_width=True,
)

st.subheader("Detected Mistakes")

st.dataframe(
    mistakes_df.sort_values(
        ["severity", "estimated_time_loss"],
        ascending=False,
    ),
    use_container_width=True,
)

st.subheader("Mistake Summary")

if summary_df.empty:
    st.info("No repeated mistakes found.")
else:
    st.dataframe(
        summary_df.round(3),
        use_container_width=True,
    )