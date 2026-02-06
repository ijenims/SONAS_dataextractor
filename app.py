# app.py

import streamlit as st
import io
from pathlib import Path

from logic import (
    parse_uploaded_filename,
    read_raw_sensor_csv,
    expand_sensor_data,
    validate_and_fix_timeseries,
    split_by_unit_id,
    save_unit_csvs,
)
from logic.visualizer import plot_timeseries_xyz
from logic.naming import make_output_filename

st.title("Sensor CSV → unit別CSV 変換")

uploaded_file = st.file_uploader(
    "CSVファイルをアップロード",
    type="csv",
)

output_dir = Path("output")

if uploaded_file is not None:
    try:
        # ① ファイル名解析
        meta = parse_uploaded_filename(uploaded_file.name)

        # ② CSV読み込み
        raw_df = read_raw_sensor_csv(uploaded_file)

        # ③ JSON展開
        expanded_df = expand_sensor_data(raw_df)

        # ④ 時系列検証・補正
        validated_df = validate_and_fix_timeseries(expanded_df)

        # ⑤ unit_idごとに分割
        unit_dfs = split_by_unit_id(validated_df)

        # ⑥ CSV保存
        save_unit_csvs(
            unit_dfs=unit_dfs,
            output_dir=output_dir,
            start_epoch=meta.start_epoch,
        )

        st.success(f"完了：{len(unit_dfs)} 個のCSVを生成しました")
        st.info("各CSVは下のボタンからダウンロードしてください")

        # 時系列グラフ可視化
        for unit_id, df_unit in unit_dfs.items():
            filename = make_output_filename(unit_id, meta.start_epoch)
            fig = plot_timeseries_xyz(df_unit, filename)
            st.plotly_chart(fig, width="stretch")

        st.subheader("unit別CSVダウンロード")

        for unit_id, df_unit in unit_dfs.items():
            filename = make_output_filename(unit_id, meta.start_epoch)

            buffer = io.StringIO()
            df_unit.to_csv(buffer, index=False)
            csv_bytes = buffer.getvalue().encode("utf-8")

            st.download_button(
                label=f"⬇ {filename}",
                data=csv_bytes,
                file_name=filename,
                mime="text/csv",
            )

    except Exception as e:
        st.error("処理中にエラーが発生しました")
        st.exception(e)