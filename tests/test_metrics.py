import pandas as pd

from src.metrics import session_summary
from src.utils import format_seconds


def test_format_seconds():
    assert format_seconds(91.5) == "1:31.500"


def test_session_summary():
    df = pd.DataFrame(
        {
            "lap": [1, 1, 2, 2],
            "lap_time": [92.0, 92.0, 91.0, 91.0],
            "speed": [100, 120, 130, 140],
        }
    )

    result = session_summary(df)

    assert result["laps"] == 2
    assert result["best_lap"] == 91.0
    assert result["max_speed"] == 140