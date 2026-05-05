import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def empty_figure(message: str = "No data available"):
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=18),
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="#0B0F14",
        plot_bgcolor="#0B0F14",
        font=dict(color="#F9FAFB"),
    )

    return fig


def apply_dark_layout(fig, title: str | None = None):
    fig.update_layout(
        title=title,
        paper_bgcolor="#0B0F14",
        plot_bgcolor="#111827",
        font=dict(color="#F9FAFB"),
        margin=dict(l=20, r=20, t=55, b=20),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F9FAFB"),
        ),
    )

    fig.update_xaxes(
        gridcolor="#1F2937",
        zerolinecolor="#1F2937",
    )

    fig.update_yaxes(
        gridcolor="#1F2937",
        zerolinecolor="#1F2937",
    )

    return fig


def gauge_chart(value, title, max_value=100):
    """
    Create a gauge chart.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=float(value),
            title={"text": title},
            gauge={
                "axis": {"range": [0, max_value]},
                "bar": {"color": "#00E676"},
                "bgcolor": "#111827",
                "borderwidth": 1,
                "bordercolor": "#1F2937",
                "steps": [
                    {"range": [0, max_value * 0.5], "color": "#1F2937"},
                    {"range": [max_value * 0.5, max_value * 0.8], "color": "#374151"},
                    {"range": [max_value * 0.8, max_value], "color": "#4B5563"},
                ],
            },
        )
    )

    fig.update_layout(
        height=250,
        paper_bgcolor="#0B0F14",
        font=dict(color="#F9FAFB"),
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def gear_indicator(gear: int):
    fig = go.Figure()

    fig.add_annotation(
        text=str(gear),
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=90, color="#00E676"),
    )

    fig.update_layout(
        height=250,
        paper_bgcolor="#0B0F14",
        plot_bgcolor="#0B0F14",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    return fig


def telemetry_line_chart(df: pd.DataFrame):
    if df.empty:
        return empty_figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["distance"],
            y=df["speed"],
            mode="lines",
            name="Speed",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["distance"],
            y=df["throttle"],
            mode="lines",
            name="Throttle",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["distance"],
            y=df["brake"],
            mode="lines",
            name="Brake",
        )
    )

    return apply_dark_layout(fig, "Live Telemetry Trace")


def plot_speed_trace(lap_df: pd.DataFrame):
    if lap_df.empty:
        return empty_figure()

    fig = px.line(
        lap_df,
        x="distance",
        y="speed",
        title="Speed Trace",
        labels={"distance": "Distance m", "speed": "Speed km/h"},
    )

    return apply_dark_layout(fig)


def plot_inputs_trace(lap_df: pd.DataFrame):
    if lap_df.empty:
        return empty_figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=lap_df["distance"],
            y=lap_df["throttle"],
            mode="lines",
            name="Throttle",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lap_df["distance"],
            y=lap_df["brake"],
            mode="lines",
            name="Brake",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lap_df["distance"],
            y=lap_df["steering"],
            mode="lines",
            name="Steering",
        )
    )

    return apply_dark_layout(fig, "Driver Inputs")


def plot_lap_times(lap_summary: pd.DataFrame):
    if lap_summary.empty:
        return empty_figure()

    fig = px.bar(
        lap_summary,
        x="lap",
        y="lap_time",
        title="Lap Time Comparison",
        labels={"lap": "Lap", "lap_time": "Lap time seconds"},
    )

    return apply_dark_layout(fig)


def plot_sector_summary(sector_df: pd.DataFrame):
    if sector_df.empty:
        return empty_figure()

    fig = px.bar(
        sector_df,
        x="sector",
        y="avg_speed",
        color="lap",
        barmode="group",
        title="Average Speed by Sector",
    )

    return apply_dark_layout(fig)


def plot_track_map(df: pd.DataFrame, color_col: str = "speed"):
    if df.empty or "x" not in df.columns or "y" not in df.columns:
        return empty_figure("Track map data unavailable")

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color=color_col,
        title=f"Track Map Colored by {color_col.title()}",
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return apply_dark_layout(fig)


def plot_corner_loss(corner_df: pd.DataFrame):
    if corner_df.empty:
        return empty_figure()

    fig = px.bar(
        corner_df,
        x="corner",
        y="estimated_corner_loss",
        color="lap",
        title="Estimated Corner Time Loss",
    )

    fig.update_layout(xaxis_tickangle=-45)

    return apply_dark_layout(fig)


def plot_mistake_frequency(summary_df: pd.DataFrame):
    if summary_df.empty:
        return empty_figure("No repeated mistakes detected")

    fig = px.bar(
        summary_df,
        x="mistake",
        y="count",
        color="total_time_loss",
        title="Mistake Frequency",
    )

    fig.update_layout(xaxis_tickangle=-30)

    return apply_dark_layout(fig)


def plot_mistake_timeline(mistakes_df: pd.DataFrame):
    if mistakes_df.empty:
        return empty_figure("No mistakes detected")

    fig = px.scatter(
        mistakes_df,
        x="lap",
        y="corner",
        size="estimated_time_loss",
        color="severity",
        title="Mistake Timeline",
        hover_data=["mistakes", "estimated_time_loss"],
    )

    return apply_dark_layout(fig)