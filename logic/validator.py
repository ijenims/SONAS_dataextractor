# logic/validator.py

from __future__ import annotations
import pandas as pd


def validate_and_fix_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    """
    責務：
      - unit_id ごとに epoch の昇順性を保証
      - unit_id内の完全重複（epoch,x,y,z同一）を除去
      - unit_id内で epoch重複かつ値不一致は例外で停止
    """
    # unit_id → epoch でソート（全体の見通しも良くなる）
    df = df.sort_values(["unit_id", "epoch"]).reset_index(drop=True)

    # unit_id内の完全重複は安全に削除
    dup_all = df.duplicated(subset=["unit_id", "epoch", "x", "y", "z"])
    if dup_all.any():
        df = df.loc[~dup_all].reset_index(drop=True)

    # unit_id内で epoch が重複してる行を抽出
    dup_epoch = df.duplicated(subset=["unit_id", "epoch"], keep=False)
    if dup_epoch.any():
        conflicted = df.loc[dup_epoch].copy()

        # その中で値が同一ならdup_allで消えてるはずなので、
        # ここに残るのは「同一epochで値が違う」＝破損
        raise ValueError(
            "unit_id内で epoch重複かつ値不一致を検出（データ破損）\n"
            f"{conflicted.head()}"
        )

    return df