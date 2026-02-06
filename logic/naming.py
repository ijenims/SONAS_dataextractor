# logic/naming.py

from __future__ import annotations
from datetime import datetime
import pandas as pd


def make_output_filename(unit_id: int, start_epoch: float) -> str:
    """
    責務：
      - 出力CSV / グラフ用のファイル名を生成する
      - 命名規則：id_[unit_id]_[YYYYMMDD_hhmm].csv
    """
    ts = pd.to_datetime(start_epoch, unit="s").strftime("%Y%m%d_%H%M")
    return f"id_{unit_id}_{ts}.csv"