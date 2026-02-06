# logic/reader.py

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import BinaryIO

import pandas as pd
import numpy as np


# =========
# ファイル名メタ情報
# =========

@dataclass(frozen=True)
class UploadedCsvMeta:
    filename: str
    start_epoch: float
    end_epoch: float


_FILENAME_RE = re.compile(
    r"^(?P<start>\d+(?:\.\d+)?)-(?P<end>\d+(?:\.\d+)?)_accel_data\.csv$"
)


def parse_uploaded_filename(filename: str) -> UploadedCsvMeta:
    """
    責務：
      - アップロードCSVのファイル名を解析
      - 開始epoch / 終了epochを取り出す
    """
    m = _FILENAME_RE.match(filename)
    if not m:
        raise ValueError(f"Unexpected filename format: {filename}")

    return UploadedCsvMeta(
        filename=filename,
        start_epoch=float(m.group("start")),
        end_epoch=float(m.group("end")),
    )


# =========
# CSV読み込み
# =========

def read_raw_sensor_csv(file_obj: BinaryIO) -> pd.DataFrame:
    """
    責務：
      - CSVを読み込んで生DataFrameを返す
      - JSON展開・検証・分割は一切しない

    使用列：
      unit_id, sampling_freq, cutoff_freq, sensor_data
    """
    usecols = [
        "unit_id",
        "sampling_freq",
        "cutoff_freq",
        "sensor_data",
    ]

    dtypes = {
        "unit_id": np.int16,
        "sampling_freq": np.int32,
        "cutoff_freq": np.int32,
        "sensor_data": "string",
    }

    df = pd.read_csv(
        file_obj,
        usecols=usecols,
        dtype=dtypes,
    )

    return df