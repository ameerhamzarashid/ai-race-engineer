import pandas as pd


def format_seconds(seconds: float | int | None) -> str:
    """
    Format seconds into M:SS.mmm.
    """
    if seconds is None or pd.isna(seconds):
        return "N/A"

    minutes = int(seconds // 60)
    remaining = float(seconds) - minutes * 60

    return f"{minutes}:{remaining:06.3f}"


def safe_round(value, digits: int = 2):
    """
    Safely round a number.
    """
    try:
        if pd.isna(value):
            return None
        return round(float(value), digits)
    except Exception:
        return None


def inject_racing_css():
    """
    Red, white and black racing dashboard CSS.

    Stage 3 theme:
    - Sidebar: red, white and black
    - Main app: dark black racing style
    - Cards: black with red borders
    - Text: white
    - Accent: racing red
    """
    return """
    <style>

    /* Main app background */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(225, 6, 0, 0.20), transparent 28%),
            linear-gradient(135deg, #050505 0%, #0A0A0A 45%, #111111 100%);
        color: #FFFFFF;
    }

    /* Hide Streamlit default top spacing a little */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #E10600 0%, #B00000 42%, #111111 100%);
        border-right: 2px solid #FFFFFF;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }

    /* Sidebar widgets */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stCheckbox,
    [data-testid="stSidebar"] .stRadio {
        background: rgba(0, 0, 0, 0.20);
        border-radius: 12px;
        padding: 0.3rem;
    }

    /* Main headings */
    .main-title {
        font-size: 3.2rem;
        font-weight: 950;
        letter-spacing: -1.5px;
        color: #FFFFFF;
        margin-bottom: 0rem;
        text-transform: uppercase;
    }

    .main-title::after {
        content: "";
        display: block;
        width: 140px;
        height: 5px;
        background: #E10600;
        margin-top: 0.55rem;
        border-radius: 999px;
    }

    .subtitle {
        color: #D1D5DB;
        font-size: 1.05rem;
        margin-top: 0.8rem;
        margin-bottom: 1.6rem;
    }

    /* Card style */
    .race-card {
        padding: 1.25rem;
        border-radius: 18px;
        background:
            linear-gradient(145deg, rgba(17, 17, 17, 0.96), rgba(5, 5, 5, 0.98));
        border: 1px solid rgba(225, 6, 0, 0.55);
        box-shadow:
            0 16px 40px rgba(0, 0, 0, 0.45),
            inset 0 0 0 1px rgba(255, 255, 255, 0.04);
        margin-bottom: 1rem;
    }

    .race-card:hover {
        border-color: #FFFFFF;
        box-shadow:
            0 18px 44px rgba(225, 6, 0, 0.18),
            inset 0 0 0 1px rgba(255, 255, 255, 0.06);
        transition: 0.25s ease;
    }

    .red-text {
        color: #E10600;
        font-weight: 900;
    }

    .white-text {
        color: #FFFFFF;
        font-weight: 900;
    }

    .black-text {
        color: #050505;
        font-weight: 900;
    }

    .green-text {
        color: #FFFFFF;
        font-weight: 900;
    }

    .warning-text {
        color: #FFB4B4;
        font-weight: 900;
    }

    .danger-text {
        color: #E10600;
        font-weight: 900;
    }

    .info-text {
        color: #FFFFFF;
        font-weight: 900;
    }

    .big-number {
        font-size: 2.25rem;
        font-weight: 950;
        color: #FFFFFF;
        line-height: 1;
    }

    .metric-label {
        color: #D1D5DB;
        font-size: 0.9rem;
        margin-top: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .metric-red {
        color: #E10600;
        font-weight: 950;
    }

    /* Race engineer panel */
    .engineer-box {
        padding: 1.45rem;
        border-radius: 18px;
        background:
            linear-gradient(135deg, rgba(225, 6, 0, 0.18), rgba(10, 10, 10, 0.95));
        border: 1px solid rgba(225, 6, 0, 0.65);
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.38);
    }

    .engineer-box h3,
    .engineer-box h4 {
        color: #FFFFFF;
        font-weight: 900;
        margin-bottom: 0.6rem;
    }

    .engineer-box p {
        color: #F3F4F6;
    }

    /* Warning and feedback boxes */
    .danger-box {
        padding: 1rem;
        border-radius: 14px;
        background:
            linear-gradient(135deg, rgba(225, 6, 0, 0.22), rgba(20, 0, 0, 0.80));
        border: 1px solid rgba(225, 6, 0, 0.85);
        margin-bottom: 0.9rem;
    }

    .warning-box {
        padding: 1rem;
        border-radius: 14px;
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(225, 6, 0, 0.14));
        border: 1px solid rgba(255, 255, 255, 0.45);
        margin-bottom: 0.9rem;
    }

    .success-box {
        padding: 1rem;
        border-radius: 14px;
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.13), rgba(17, 17, 17, 0.96));
        border: 1px solid rgba(255, 255, 255, 0.55);
        margin-bottom: 0.9rem;
    }

    /* Streamlit buttons */
    .stButton > button {
        background: #E10600 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        padding: 0.55rem 1rem !important;
        transition: 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #FFFFFF !important;
        color: #E10600 !important;
        border: 1px solid #E10600 !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background:
            linear-gradient(145deg, rgba(17,17,17,0.98), rgba(5,5,5,0.98));
        border: 1px solid rgba(225, 6, 0, 0.45);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.30);
    }

    [data-testid="stMetricLabel"] {
        color: #D1D5DB !important;
        font-weight: 700;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 950;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(225, 6, 0, 0.40);
        border-radius: 14px;
        overflow: hidden;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: #111111;
        color: #FFFFFF;
        border-radius: 12px 12px 0 0;
        border: 1px solid rgba(225, 6, 0, 0.35);
        padding: 0.6rem 1rem;
        font-weight: 800;
    }

    .stTabs [aria-selected="true"] {
        background: #E10600 !important;
        color: #FFFFFF !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #111111;
        color: #FFFFFF !important;
        border-radius: 10px;
        border: 1px solid rgba(225, 6, 0, 0.35);
    }

    /* Inputs */
    .stSelectbox div,
    .stNumberInput div,
    .stTextInput div {
        color: #FFFFFF;
    }

    /* Horizontal rule style */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E10600, transparent);
        margin: 1.5rem 0;
    }

    </style>
    """