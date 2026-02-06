# logic/saver.py

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
from .naming import make_output_filename

def save_unit_csvs(
    unit_dfs: Dict[int, pd.DataFrame],
    output_dir: Path,
    start_epoch: float,
) -> None:
    """
    責務：
      - unit_id別DataFrameをCSVとして保存する
      - 命名規則：id_[unit_id]_[YYYYMMDD_hhmm].csv

    前提：
      - df列：epoch, datetime, x, y, z
      - start_epoch：入力ファイル名先頭のepoch
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    ts = pd.to_datetime(start_epoch, unit="s").strftime("%Y%m%d_%H%M")

    for unit_id, df in unit_dfs.items():
        filename = make_output_filename(unit_id, start_epoch)
        path = output_dir / filename
        df.to_csv(path, index=False)