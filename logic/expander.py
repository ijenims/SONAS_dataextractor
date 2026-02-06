# logic/expander.py

from __future__ import annotations

import json
from typing import List, Dict

import pandas as pd


def expand_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    責務：
      - sensor_data(JSON配列)を展開
      - epoch, datetime, x, y, z を持つ正規化DataFrameを返す
      - epoch昇順でソート

    入力df想定列：
      unit_id, sensor_data
    """
    rows: List[Dict] = []

    for _, row in df.iterrows():
        unit_id = int(row["unit_id"])

        # JSON文字列を安全側でロード
        json_list = json.loads(
            row["sensor_data"]
            .replace("'", '"')
        )

        for item in json_list:
            rows.append(
                {
                    "unit_id": unit_id,
                    "epoch": float(item["epoch"]),
                    "x": float(item["x"]),
                    "y": float(item["y"]),
                    "z": float(item["z"]),
                }
            )

    out = pd.DataFrame(rows)

    # epoch → datetime
    out["datetime"] = pd.to_datetime(out["epoch"], unit="s")

    # 列順を固定
    out = out[["unit_id", "epoch", "datetime", "x", "y", "z"]]

    # 時系列保証
    out = out.sort_values("epoch").reset_index(drop=True)

    return out