from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
UPLOAD_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"

SAMPLE_TELEMETRY_PATH = SAMPLE_DIR / "sample_telemetry.csv"

REQUIRED_COLUMNS = [
    "timestamp",
    "lap",
    "distance",
    "speed",
    "throttle",
    "brake",
    "steering",
    "gear",
    "rpm",
    "x",
    "y",
    "sector",
    "corner",
    "lap_time",
]

DASHBOARD_COLORS = {
    "background": "#0B0F14",
    "card": "#111827",
    "border": "#1F2937",
    "primary": "#00E676",
    "warning": "#FFC107",
    "danger": "#FF1744",
    "info": "#00B0FF",
    "text": "#F9FAFB",
    "muted": "#9CA3AF",
}