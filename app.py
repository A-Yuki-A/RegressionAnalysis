import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os
from pandas.api.types import is_numeric_dtype

st.title("🍦 アイス売上と各項目の関係を調べよう")

# === フォント設定（OTF版・絶対パス指定） ===
font_path = os.path.abspath(os.path.join("fonts", "SourceHanCodeJP-Regular.otf"))
if os.path.exists(font_path):
    try:
        fm.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = "Source Han Code JP"
    except Exception as e:
        st.warning(f"⚠️ フォントの読み込みに失敗しました: {e}")
else:
    st.warning("⚠️ fonts フォルダに SourceHanCodeJP-Regular.otf が見つかりません。")

# === ファイルアップロード ===
uploaded_file = st.file_uploader("アイス売上データ（Excel）をアップロードしてください", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("データの中身")
    st.dataframe(df.head())

    # 「年」「月」だけを除外（例：最高気温月平均 は残す）
    cols_excluded_exact = {"年", "月"}
    numeric_cols = [c for c in df.columns if c not in cols_excluded_exact and is_numeric_dtype(df[c])]

    if not numeric_cols:
        st.error("数値データの列が見つかりません。Excelの列が数値として読み込まれているか確認してください。")
        st.stop()

    # 目的変数（売上）
    y_col = st.selectbox("売上（目的変数）にする列を選んでください", numeric_cols, key="y_select")

    # 説明変数（売上に影響しそうな項目）
    x_candidates = [c for c in numeric_cols if c != y_col]
    if not x_candidates:
        st.error("説明変数にできる列がありません。別の目的変数を選んでください。")
        st.stop()
    x_col = st.selectbox("売上に影響しそうな項目（説明変数）を選んでください", x_candidates, key="x_select")

    # 欠損を除去してから計算
    data = df[[x_col, y_col]].dropna()
    x = data[x_col].astype(float)
    y = data[y_col].astype(float)

    # 回帰直線の計算（一次）
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept

    # 相関係数・決定係数
    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2

    # 散布図の描画
    fig, ax = plt.subplots()
    ax.scatter(x, y, label="データ点", alpha=0.7)
    ax.plot(x, y_pred, color="red", linewidth=2, label="回帰直線")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()
    st.pyplot(fig)

    # 数値の表示
    st.markdown(f"**回帰式：** y = {slope:.3f}x + {intercept:.3f}")
    st.markdown(f"**相関係数（r）：** {r:.3f}")
    st.markdown(f"**決定係数（R²）：** {r2:.3f}")

    # ===== ここから 予測機能 =====
    st.subheader("🔮 x の値から y を予測しよう")

    xmin, xmax = float(np.nanmin(x)), float(np.nanmax(x))
    # ステップはレンジの100分の1（極端に小さい場合は 0.1）
    step = max((xmax - xmin) / 100.0, 0.1)

    x_input = st.number_input(
        f"予測したい {x_col}（x）の値を入力してください",
        value=float(np.nanmedian(x)),
        step=step
    )

    # 範囲外のとき注意喚起（外挿）
    if x_input < xmin or x_input > xmax:
        st.warning(
            f"入力した x は学習データ範囲（{xmin:.3f} ～ {xmax:.3f}）外です。外挿になるため予測の信頼性は下がります。"
        )

    y_hat = slope * x_input + intercept
    st.success(f"**予測された {y_col}（y）**： {y_hat:.3f}")

else:
    st.info("Excelファイルをアップロードすると、散布図と回帰直線、指標、予測フォームが表示されます。")
