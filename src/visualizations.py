import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


RED = "#E10600"
WHITE = "#FFFFFF"
BLACK = "#050505"
DARK = "#111111"
DARKER = "#0A0A0A"
GREY = "#D1D5DB"
GRID = "#2A2A2A"


def empty_figure(message: str = "No data available"):
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=18, color=WHITE),
    )

    fig.update_layout(
        height=350,
        paper_bgcolor=BLACK,
        plot_bgcolor=BLACK,
        font=dict(color=WHITE),
    )

    return fig


def apply_dark_layout(fig, title: str | None = None):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color=WHITE, size=20),
            x=0.02,
        )
        if title
        else None,
        paper_bgcolor=BLACK,
        plot_bgcolor=DARK,
        font=dict(color=WHITE),
        margin=dict(l=24, r=24, t=60, b=30),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=WHITE),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    fig.update_xaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        color=GREY,
        linecolor=GRID,
        showline=True,
    )

    fig.update_yaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        color=GREY,
        linecolor=GRID,
        showline=True,
    )

    return fig


def gauge_chart(value, title, max_value=100):
    """
    Create a red, white and black gauge chart.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=float(value),
            title={"text": title, "font": {"color": WHITE, "size": 18}},
            number={"font": {"color": WHITE, "size": 34}},
            gauge={
                "axis": {
                    "range": [0, max_value],
                    "tickcolor": WHITE,
                    "tickfont": {"color": GREY},
                },
                "bar": {"color": RED},
                "bgcolor": DARK,
                "borderwidth": 1,
                "bordercolor": WHITE,
                "steps": [
                    {"range": [0, max_value * 0.5], "color": "#1A1A1A"},
                    {"range": [max_value * 0.5, max_value * 0.8], "color": "#2A2A2A"},
                    {"range": [max_value * 0.8, max_value], "color": "#3A0A0A"},
                ],
                "threshold": {
                    "line": {"color": WHITE, "width": 4},
                    "thickness": 0.75,
                    "value": max_value * 0.9,
                },
            },
        )
    )

    fig.update_layout(
        height=250,
        paper_bgcolor=BLACK,
        font=dict(color=WHITE),
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def gear_indicator(gear: int):
    fig = go.Figure()

    fig.add_shape(
        type="rect",
        x0=0.12,
        y0=0.12,
        x1=0.88,
        y1=0.88,
        line=dict(color=RED, width=4),
        fillcolor=DARK,
    )

    fig.add_annotation(
        text=str(gear),
        x=0.5,
        y=0.55,
        showarrow=False,
        font=dict(size=92, color=WHITE, family="Arial Black"),
    )

    fig.add_annotation(
        text="GEAR",
        x=0.5,
        y=0.18,
        showarrow=False,
        font=dict(size=14, color=GREY),
    )

    fig.update_layout(
        height=250,
        paper_bgcolor=BLACK,
        plot_bgcolor=BLACK,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
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
            line=dict(color=WHITE, width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["distance"],
            y=df["throttle"],
            mode="lines",
            name="Throttle",
            line=dict(color=RED, width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["distance"],
            y=df["brake"],
            mode="lines",
            name="Brake",
            line=dict(color="#FFB4B4", width=3),
        )
    )

    return apply_dark_layout(fig, "Live Telemetry Trace")


def plot_speed_trace(lap_df: pd.DataFrame):
    if lap_df.empty:
        return empty_figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=lap_df["distance"],
            y=lap_df["speed"],
            mode="lines",
            name="Speed",
            line=dict(color=RED, width=3),
        )
    )

    return apply_dark_layout(fig, "Speed Trace")


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
            line=dict(color=RED, width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lap_df["distance"],
            y=lap_df["brake"],
            mode="lines",
            name="Brake",
            line=dict(color=WHITE, width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lap_df["distance"],
            y=lap_df["steering"],
            mode="lines",
            name="Steering",
            line=dict(color="#FFB4B4", width=2),
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
        color="lap_time",
        color_continuous_scale=[
            [0, WHITE],
            [0.45, "#FFB4B4"],
            [1, RED],
        ],
    )

    fig.update_traces(
        marker_line_color=WHITE,
        marker_line_width=1,
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
        color_continuous_scale=[
            [0, WHITE],
            [1, RED],
        ],
    )

    return apply_dark_layout(fig)


def plot_track_map(df: pd.DataFrame, color_col: str = "speed"):
    if df.empty or "x" not in df.columns or "y" not in df.columns:
        return empty_figure("Track map data unavailable")

    color_scale = [
        [0, WHITE],
        [0.5, "#FFB4B4"],
        [1, RED],
    ]

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color=color_col,
        title=f"Track Map Colored by {color_col.title()}",
        color_continuous_scale=color_scale,
    )

    fig.update_traces(
        marker=dict(size=6, line=dict(width=0)),
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
        color="estimated_corner_loss",
        title="Estimated Corner Time Loss",
        color_continuous_scale=[
            [0, WHITE],
            [1, RED],
        ],
    )

    fig.update_traces(
        marker_line_color=WHITE,
        marker_line_width=1,
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
        color_continuous_scale=[
            [0, WHITE],
            [1, RED],
        ],
    )

    fig.update_traces(
        marker_line_color=WHITE,
        marker_line_width=1,
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
        color_continuous_scale=[
            [0, WHITE],
            [1, RED],
        ],
    )

    fig.update_traces(
        marker=dict(line=dict(color=WHITE, width=1)),
    )

    return apply_dark_layout(fig)