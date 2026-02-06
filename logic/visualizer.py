# logic/visualizer.py

from __future__ import annotations
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go


def plot_timeseries_xyz(
    df: pd.DataFrame,
    output_filename: str,
):
    """
    責務：
      - x, y, z の時系列グラフを1枚生成
      - 表示のみ（保存しない）

    df列想定：
      epoch, datetime, x, y, z
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["x"],
        mode="lines",
        name="x",
    ))
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["y"],
        mode="lines",
        name="y",
    ))
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["z"],
        mode="lines",
        name="z",
    ))

    fig.update_layout(
        title=Path(output_filename).name,
        xaxis_title="Time",
        yaxis_title="Acceleration",
        legend_title="Axis",
    )

    return fig