# SONAS_TO_CSV

（最終更新日：2026-02-06）

センサCSVファイルを読み込み、  
`sensor_data` 列に格納された JSON 時系列データを展開し、  
**unit_id ごとに分割された時系列CSVを生成・可視化するツール**。

Streamlit ベースの業務向け前処理ツール。

---

## 機能概要

- ローカルCSVファイルをアップロード
- `sensor_data`（JSON配列）から以下を抽出
  - epoch
  - x, y, z
- epoch 昇順に並べた時系列データを生成
- unit_id ごとに CSV を分割出力
- x, y, z を **unit_id ごとに1枚の時系列グラフで可視化**
- 時系列破損（epoch重複・値不一致）はエラーで停止

---

## 入力CSV仕様

### ファイル名形式

```

[開始epoch]-[終了epoch]_accel_data.csv

```

例：

```

1753027200.000000-1753030800.000000_accel_data.csv

```

※ 開始epochは出力CSV・グラフタイトルに使用される

---

### 使用列

| 列名          | 内容                     |
| ------------- | ------------------------ |
| unit_id       | センサID                 |
| sampling_freq | サンプリング周波数       |
| cutoff_freq   | カットオフ周波数         |
| sensor_data   | JSON配列（時系列データ） |

`sensor_data` の例：

```json
[
  { "epoch": 1753027200.01, "x": 0.1, "y": 0.0, "z": 0.2 },
  { "epoch": 1753027200.02, "x": 0.1, "y": 0.1, "z": 0.2 }
]
```

---

## 出力CSV仕様

### ファイル名

```

id*[unit_id]*[YYYYMMDD_hhmm].csv

```

例：

```

id_3_20250721_1200.csv

```

※ 日時は **入力CSVファイル名の開始epoch** から生成

---

### 列構成（固定）

| 列順 | 列名     | 内容             |
| ---- | -------- | ---------------- |
| 0    | epoch    | UNIX epoch（秒） |
| 1    | datetime | datetime型       |
| 2    | x        | 加速度 x         |
| 3    | y        | 加速度 y         |
| 4    | z        | 加速度 z         |

---

## グラフ表示仕様

- unit_id ごとに **1枚の時系列グラフ**
- x, y, z を同一グラフ上に重ね描き
- 横軸：datetime
- 縦軸：加速度
- **グラフタイトル：保存CSVファイル名（パス除外）**

---

## ディレクトリ構成

```

SONAS_TO_CSV/
├─ app.py # Streamlit UI（入口）
├─ logic/
│ ├─ **init**.py
│ ├─ reader.py # CSV読み込み・ファイル名解析
│ ├─ expander.py # JSON展開
│ ├─ validator.py # 時系列検証（unit_id単位）
│ ├─ splitter.py # unit_id分割
│ ├─ saver.py # CSV保存
│ ├─ naming.py # 出力ファイル命名規則
│ └─ visualizer.py # 時系列グラフ生成
├─ output/ # 生成CSV（自動生成）
├─ requirements.txt
└─ README.md

```

---

## セットアップ

### 1. 仮想環境（任意）

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 依存関係インストール

```bash
pip install -r requirements.txt
```

---

## 起動方法

```bash
streamlit run app.py
```

ブラウザが自動で起動し、CSVアップロード画面が表示される。

---

## 時系列検証ルール（重要）

- **unit_id ごとに検証**
- 完全重複（epoch,x,y,z 同一）
  → 自動除去
- 同一 unit_id 内で
  - epoch 同一
  - 値が不一致
    → **エラーで停止（データ破損）**

※ 複数センサ間で epoch が同一なのは問題なし

---

## 注意事項

- epoch は float（小数点以下含む）として処理
- 高サンプリングデータでは epoch が代表時刻の場合あり
- pandas × VSCode（Pylance）の型警告は **実行に影響なし**
- Streamlit の `use_container_width` は廃止予定のため未使用

---

## 想定用途

- センサログの前処理
- FFT / 振動解析前のデータ整形
- unit別データ切り出し・可視確認

---

## 備考

- 本ツールは **SOLID原則を前提に設計**
- 命名規則・可視化・保存処理は責務分離済み
- 仕様変更時も影響範囲は最小

（更新日：2026-02-06）
