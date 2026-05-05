import math
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import SAMPLE_TELEMETRY_PATH


def corner_name(distance: float) -> str:
    """
    Assign simple corner zones based on distance.
    Track length is approximately 4200 metres.
    """
    corners = [
        (0, 350, "Main Straight"),
        (350, 620, "Turn 1"),
        (620, 900, "Turn 2"),
        (900, 1250, "Back Straight"),
        (1250, 1520, "Turn 3"),
        (1520, 1850, "Turn 4"),
        (1850, 2250, "Middle Straight"),
        (2250, 2520, "Turn 5"),
        (2520, 2820, "Turn 6"),
        (2820, 3300, "Long Straight"),
        (3300, 3570, "Turn 7"),
        (3570, 3850, "Turn 8"),
        (3850, 4200, "Final Straight"),
    ]

    for start, end, name in corners:
        if start <= distance < end:
            return name

    return "Main Straight"


def sector_number(distance: float) -> int:
    if distance < 1400:
        return 1
    if distance < 2800:
        return 2
    return 3


def is_corner(distance: float) -> bool:
    return "Turn" in corner_name(distance)


def generate_lap(
    lap_number: int,
    lap_time: float,
    track_length: float = 4200,
    samples: int = 700,
    driver_noise: float = 1.0,
    mistake_lap: bool = False,
) -> pd.DataFrame:
    """
    Generate one synthetic lap of telemetry.
    """
    distances = np.linspace(0, track_length, samples)
    timestamps = np.linspace((lap_number - 1) * lap_time, lap_number * lap_time, samples)

    rows = []

    for i, distance in enumerate(distances):
        corner = corner_name(distance)
        sector = sector_number(distance)
        corner_flag = is_corner(distance)

        base_speed = 255

        if corner_flag:
            base_speed = 115

        if corner in ["Turn 1", "Turn 3", "Turn 5", "Turn 7"]:
            base_speed = 95

        if corner in ["Turn 2", "Turn 4", "Turn 6", "Turn 8"]:
            base_speed = 135

        wave = 12 * math.sin(distance / 180)
        noise = np.random.normal(0, driver_noise)

        speed = base_speed + wave + noise

        if not corner_flag:
            speed += 30 * math.sin(distance / 400) + 15

        speed = max(40, min(speed, 310))

        brake = 0
        throttle = 90

        corner_start_zones = [
            (320, 430),
            (1180, 1320),
            (2180, 2320),
            (3220, 3370),
        ]

        medium_brake_zones = [
            (580, 650),
            (1480, 1570),
            (2480, 2570),
            (3530, 3630),
        ]

        for start, end in corner_start_zones:
            if start <= distance <= end:
                brake = np.random.randint(65, 100)
                throttle = np.random.randint(0, 15)

        for start, end in medium_brake_zones:
            if start <= distance <= end:
                brake = np.random.randint(35, 70)
                throttle = np.random.randint(0, 25)

        if corner_flag and brake == 0:
            throttle = np.random.randint(20, 65)

        if not corner_flag and brake == 0:
            throttle = np.random.randint(80, 101)

        steering = 0

        if corner_flag:
            steering_direction = 1 if int(distance // 400) % 2 == 0 else -1
            steering = steering_direction * np.random.uniform(12, 38)

        steering += np.random.normal(0, 2)

        # Add deliberate mistakes on some laps.
        if mistake_lap:
            if lap_number in [3, 5] and corner in ["Turn 1", "Turn 5"]:
                # Late braking and over-slowing
                if distance % 4200 > 390 and distance % 4200 < 470:
                    brake = np.random.randint(85, 100)
                    throttle = 0
                    speed -= 18

            if lap_number in [4, 6] and corner in ["Turn 3", "Turn 7"]:
                # Late throttle pickup
                throttle = max(0, throttle - 30)
                speed -= 10

            if lap_number in [2, 6] and corner in ["Turn 4", "Turn 8"]:
                # Unstable steering
                steering += np.random.normal(0, 12)

        gear = int(np.clip(speed // 38 + 1, 1, 8))
        rpm = int(np.clip(3500 + speed * 35 + throttle * 20, 3500, 12500))

        angle = (distance / track_length) * 2 * math.pi
        radius_x = 900 + 120 * math.sin(3 * angle)
        radius_y = 550 + 80 * math.cos(2 * angle)

        x = radius_x * math.cos(angle)
        y = radius_y * math.sin(angle)

        rows.append(
            {
                "timestamp": round(float(timestamps[i]), 3),
                "lap": lap_number,
                "distance": round(float(distance), 3),
                "speed": round(float(speed), 3),
                "throttle": round(float(throttle), 3),
                "brake": round(float(brake), 3),
                "steering": round(float(steering), 3),
                "gear": gear,
                "rpm": rpm,
                "x": round(float(x), 3),
                "y": round(float(y), 3),
                "sector": sector,
                "corner": corner,
                "lap_time": round(float(lap_time), 3),
            }
        )

    return pd.DataFrame(rows)


def generate_sample_telemetry(output_path: Path = SAMPLE_TELEMETRY_PATH) -> Path:
    """
    Generate a complete sample session with multiple laps.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    np.random.seed(42)

    lap_times = [92.8, 91.9, 93.4, 92.5, 94.1, 93.8, 91.6, 92.1]

    all_laps = []

    for idx, lap_time in enumerate(lap_times, start=1):
        mistake_lap = idx not in [2, 7]
        lap_df = generate_lap(
            lap_number=idx,
            lap_time=lap_time,
            driver_noise=1.5 if mistake_lap else 0.8,
            mistake_lap=mistake_lap,
        )
        all_laps.append(lap_df)

    session_df = pd.concat(all_laps, ignore_index=True)
    session_df.to_csv(output_path, index=False)

    return output_path


if __name__ == "__main__":
    path = generate_sample_telemetry()
    print(f"Sample telemetry generated at: {path}")