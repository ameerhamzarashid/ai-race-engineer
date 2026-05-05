# AI Race Engineer

AI Race Engineer is a red, white and black motorsport-style telemetry coaching dashboard built with Python, Streamlit, Pandas, NumPy and Plotly.

The project analyses simulated sim racing telemetry and gives race engineer style feedback on braking, throttle application, steering behaviour, corner execution, lap consistency and estimated time loss.

It is designed as a portfolio-ready AI and data analytics project that demonstrates dashboard development, telemetry analysis, rule-based AI logic, performance scoring and user-focused visual design.

---

## Project Overview

Sim racing telemetry contains detailed information about how a driver controls the car across a lap. This includes speed, throttle, brake pressure, steering angle, gear selection, RPM, distance, sector, corner and lap time.

AI Race Engineer uses this telemetry to:

- Analyse lap performance
- Compare laps against the best reference lap
- Detect common driving mistakes
- Estimate where time is being lost
- Generate race engineer style coaching feedback
- Produce a personalised training plan

The first version uses a generated sample telemetry dataset, so the project can run without needing a real simulator connection.

---

## Key Features

- Real-time style telemetry replay
- Red, white and black racing dashboard theme
- Red and white sidebar design
- Live speed, throttle and brake gauges
- Gear indicator
- Lap time analysis
- Speed trace visualisation
- Throttle, brake and steering trace
- Track map visualisation
- Corner by corner analysis
- Best lap reference comparison
- Entry, apex and exit phase analysis
- Mistake detection
- Estimated time loss by corner
- Estimated time loss by lap
- AI-style race engineer coaching report
- Driver performance score
- Personalised training plan
- Telemetry CSV upload support
- GitHub-ready structure

---

## Dashboard Pages

### Home

The homepage gives a high-level overview of the session.

It shows:

- Overall driver score
- Best lap
- Maximum speed
- Number of laps analysed
- Race engineer summary
- Lap time overview
- Track map preview

---

### Live Race Engineer

This page simulates a live race engineer dashboard.

It includes:

- Speed gauge
- Throttle gauge
- Brake gauge
- Gear display
- Current lap
- Current corner
- RPM
- Driving status
- Live telemetry trace
- Race engineer feedback panel

This page works like a replay system. The user can advance through telemetry frames and see changing car behaviour.

---

### Lap Analysis

This page analyses individual laps.

It includes:

- Selected lap time
- Best lap comparison
- Estimated time loss
- Speed trace
- Throttle trace
- Brake trace
- Steering trace
- Track map
- Sector summary
- Lap summary table

---

### Corner Coach

This page compares every corner against the best lap reference.

It analyses:

- Entry speed
- Apex speed
- Minimum speed
- Exit speed
- Steering stability
- Brake point
- Throttle pickup
- Estimated corner loss

The page helps identify where the driver is losing time within specific corners.

---

### Mistake Detector

This page detects repeated driving mistakes.

Detected mistakes include:

- Late braking
- Early braking
- Late brake release
- Over-slowing
- Low apex speed
- Poor corner exit
- Late throttle pickup
- Unstable steering
- Too much coasting
- Brake and throttle overlap

The page shows:

- Mistake frequency
- Mistake timeline
- Severity score
- Estimated time loss
- Mistake summary table

---

### AI Coaching Report

This page generates a race engineer style coaching report.

It includes:

- Overall score
- Pace score
- Consistency score
- Control score
- Racecraft score
- Best lap
- Average lap
- Strengths
- Main weakness
- Improvement advice
- Worst corner feedback
- Lap engineer notes
- Full coaching table

---

### Upload Telemetry

This page allows users to upload their own telemetry CSV file.

The uploaded file must contain the required telemetry columns. After upload, the app validates the file and previews:

- Speed trace
- Driver inputs
- Track map

---

### Training Plan

This page creates a personalised practice plan based on the most costly telemetry mistakes.

It includes:

- Main training focus
- Priority drills
- Measurable improvement targets
- Explanation of why each drill was selected
- Mistakes behind the plan

---

## Detected Driving Mistakes

The system can detect and explain the following issues:

| Mistake | Meaning |
|---|---|
| Late braking | The driver brakes later than the best reference lap and may destabilise the car |
| Early braking | The driver brakes too early and loses time before the corner |
| Late brake release | The driver holds the brake too long into the corner |
| Over-slowing | The driver reduces speed too much before or during the apex |
| Low apex speed | The car is too slow in the middle of the corner |
| Poor corner exit | The driver loses speed when leaving the corner |
| Late throttle pickup | The driver applies throttle too late after the apex |
| Unstable steering | The steering input has too many corrections |
| Too much coasting | The driver spends too long with little throttle and little brake |
| Brake and throttle overlap | Brake and throttle are used together unnecessarily |

---

## Tech Stack

| Area | Technology |
|---|---|
| Programming Language | Python |
| Dashboard | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualisation | Plotly |
| AI Logic | Rule-based coaching engine |
| Testing | Pytest |
| Version Control | Git and GitHub |

---

## Project Structure

```text
ai-race-engineer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── .gitkeep
│
├── data/
│   ├── sample/
│   │   └── sample_telemetry.csv
│   ├── uploads/
│   └── processed/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── generate_sample_data.py
│   ├── data_loader.py
│   ├── telemetry_cleaning.py
│   ├── live_replay.py
│   ├── metrics.py
│   ├── corner_analysis.py
│   ├── advanced_analysis.py
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
│   ├── 6_Upload_Telemetry.py
│   └── 7_Training_Plan.py
│
└── tests/
    └── test_metrics.py
