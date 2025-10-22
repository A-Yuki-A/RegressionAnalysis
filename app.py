import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os
from pandas.api.types import is_numeric_dtype

st.title("🍦 アイス売上と各項目の関係を調べよう")

# === フォント設定（GitHub同梱） ===
font_path = os.path.join("fonts", "SourceHanCodeJP-Regular.otf")
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams["font.family"] = "Source Han Code JP"
else:
    st.warning("⚠️ 日本語フォントが見つかりません。fonts/SourceHanCodeJP-Regular.otf を配置してください。")

# === ファイルアップロード ===
uploaded_file = st.file_uploader("アイス売上データ（Excel）をアップロードしてください", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("データの中身")
    st.dataframe(df.head())

    # 「年」「月」“だけ”を除外（列名に月が含まれていても残す）
    cols_excluded_exact = {"年", "月"}
    numeric_cols = [c for c in df.columns if c not in cols_excluded_exact and is_numeric_dtype(df[c])]

    if not numeric_cols:
        st.error("数値データの列が見つかりません。Excelの列が数値として読み込まれているか確認してください。")
        st.stop()

    # 目的変数の選択（数値列のみ）
    y_col = st.selectbox("売上（目的変数）にする列を選んでください", numeric_cols, key="y_select")

    # 説明変数の選択（数値列のみ & yと別）
    x_candidates = [c for c in numeric_cols if c != y_col]
    if not x_candidates:
        st.error("説明変数にできる列がありません。別の目的変数を選んでください。")
        st.stop()
    x_col = st.selectbox("売上に影響しそうな項目（説明変数）を選んでください", x_candidates, key="x_select")

    # 欠損を落としてから計算
    data = df[[x_col, y_col]].dropna()
    x = data[x_col].astype(float)
    y = data[y_col].astype(float)

    # 回帰直線（一次）の計算
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept

    # 相関係数・決定係数
    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2

    # 散布図の描画
    fig, ax = plt.subplots()
    ax.scatter(x, y, label="データ点", alpha=0.7)
    ax.plot(x, y_pred, label="回帰直線", linewidth=2)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()
    st.pyplot(fig)

    # 数値の表示
    st.markdown(f"**回帰式：** y = {slope:.3f}x + {intercept:.3f}")
    st.markdown(f"**相関係数（r）：** {r:.3f}")
    st.markdown(f"**決定係数（R²）：** {r2:.3f}")
else:
    st.info("Excelファイルをアップロードすると、散布図が表示されます。")
