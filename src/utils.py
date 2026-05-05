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
    Add custom dark racing dashboard CSS.
    """
    return """
    <style>
    .stApp {
        background: linear-gradient(135deg, #070A0F 0%, #0B0F14 45%, #111827 100%);
        color: #F9FAFB;
    }

    [data-testid="stSidebar"] {
        background-color: #080C12;
        border-right: 1px solid #1F2937;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -1px;
        color: #F9FAFB;
        margin-bottom: 0rem;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .race-card {
        padding: 1.2rem;
        border-radius: 18px;
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid #1F2937;
        box-shadow: 0 16px 40px rgba(0,0,0,0.35);
        margin-bottom: 1rem;
    }

    .green-text {
        color: #00E676;
        font-weight: 800;
    }

    .warning-text {
        color: #FFC107;
        font-weight: 800;
    }

    .danger-text {
        color: #FF1744;
        font-weight: 800;
    }

    .info-text {
        color: #00B0FF;
        font-weight: 800;
    }

    .big-number {
        font-size: 2.2rem;
        font-weight: 900;
        color: #00E676;
        line-height: 1;
    }

    .metric-label {
        color: #9CA3AF;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }

    .engineer-box {
        padding: 1.4rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(0,230,118,0.12), rgba(0,176,255,0.08));
        border: 1px solid rgba(0,230,118,0.35);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .danger-box {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(255,23,68,0.12);
        border: 1px solid rgba(255,23,68,0.45);
        margin-bottom: 0.8rem;
    }

    .warning-box {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(255,193,7,0.12);
        border: 1px solid rgba(255,193,7,0.45);
        margin-bottom: 0.8rem;
    }

    .success-box {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(0,230,118,0.12);
        border: 1px solid rgba(0,230,118,0.35);
        margin-bottom: 0.8rem;
    }
    </style>
    """