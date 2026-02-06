# logic/splitter.py

from __future__ import annotations

from typing import Dict
import pandas as pd


def split_by_unit_id(df: pd.DataFrame) -> Dict[int, pd.DataFrame]:
    """
    責務：
      - 正規化・検証済みdfを unit_id ごとに分割する

    入力df想定列：
      unit_id, epoch, datetime, x, y, z
    """
    unit_dfs: Dict[int, pd.DataFrame] = {}

    for unit_id, g in df.groupby("unit_id"):
        unit_dfs[int(unit_id)] = (
            g.drop(columns="unit_id")
             .reset_index(drop=True)
        )

    return unit_dfs