# AI Race Engineer

AI Race Engineer is a real-time sim racing telemetry coaching dashboard built with Python, Streamlit, Pandas and Plotly.

The project analyses speed, throttle, brake, steering, gear, RPM, lap performance and corner behaviour to detect driving mistakes and generate race engineer style coaching feedback.

## Features

- Simulated real-time telemetry replay
- Live speed, throttle and brake gauges
- Gear indicator
- Lap time analysis
- Speed trace
- Throttle, brake and steering trace
- Track map visualisation
- Corner by corner coaching
- Mistake detection
- AI-style race engineer feedback
- Driver performance score
- Telemetry CSV upload
- GitHub-ready project structure

## Detected Mistakes

The system can detect:

- Late braking
- Early braking
- Over-slowing
- Poor corner exit
- Late throttle pickup
- Unstable steering

## Tech Stack

| Area | Tool |
|---|---|
| Programming Language | Python |
| Dashboard | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualisation | Plotly |
| Rule-based AI Logic | Custom Python engine |
| Testing | Pytest |
| Version Control | Git and GitHub |

## Project Structure

```text
ai-race-engineer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── sample/
│   ├── uploads/
│   └── processed/
│
├── src/
│   ├── config.py
│   ├── generate_sample_data.py
│   ├── data_loader.py
│   ├── telemetry_cleaning.py
│   ├── live_replay.py
│   ├── metrics.py
│   ├── corner_analysis.py
│   ├── mistake_detector.py
│   ├── coaching_engine.py
│   ├── scoring.py
│   ├── visualizations.py
│   └── utils.py
│
├── pages/
│   ├── 1_Live_Race_Engineer.py
│   ├── 2_Lap_Analysis.py
│   ├── 3_Corner_Coach.py
│   ├── 4_Mistake_Detector.py
│   ├── 5_AI_Coaching_Report.py
│   └── 6_Upload_Telemetry.py
│
└── tests/
    └── test_metrics.py