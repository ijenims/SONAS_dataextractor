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


# =====================
# ページ設定
# =====================
st.set_page_config(
    page_title="Sonas data-extractor",
    layout="wide",
)

# =====================
# サイドバー
# =====================
with st.sidebar:
    st.header("操作パネル")

    uploaded_file = st.file_uploader(
        "CSVファイルをアップロード",
        type="csv",
    )

    status_area = st.empty()
    guide_area = st.empty()

    st.divider()
    st.subheader("ダウンロード")

    download_area = st.container()

# =====================
# メインエリア
# =====================
st.title("SONAS Acc_Data Extractor")
st.subheader("生データより子機ユニット番号別に加速度データを抽出")

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

        # ⑥ CSV保存（ローカル用・Cloudでは参照のみ）
        save_unit_csvs(
            unit_dfs=unit_dfs,
            output_dir=output_dir,
            start_epoch=meta.start_epoch,
        )

        # ===== サイドバー表示 =====
        status_area.success(f"アップロード完了：{len(unit_dfs)} 個のCSVを生成しました")
        guide_area.info("下のボタンからCSVをダウンロードしてください")

        # ===== グラフ表示（メイン）=====
        for unit_id, df_unit in unit_dfs.items():
            filename = make_output_filename(unit_id, meta.start_epoch)
            fig = plot_timeseries_xyz(df_unit, filename)
            st.plotly_chart(fig, width="stretch")

        # ===== ダウンロードボタン（サイドバー）=====
        with download_area:
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
        status_area.error("エラーが発生しました")
        st.exception(e)