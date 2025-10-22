import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("🍦 アイス売上と各項目の関係を調べよう")

# Excelファイルの読み込み
uploaded_file = st.file_uploader("アイス売上データ（Excel）をアップロードしてください", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("データの中身")
    st.dataframe(df.head())

    # 売上列を選択（自動検出 or 手動選択）
    y_col = st.selectbox("売上（目的変数）にする列を選んでください", df.columns)

    # 説明変数を選択
    x_col = st.selectbox("売上に影響しそうな項目（説明変数）を選んでください", [c for c in df.columns if c != y_col])

    # 散布図と回帰直線を描く
    x = df[x_col]
    y = df[y_col]

    # 回帰直線の計算
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept

    # 相関係数と決定係数
    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2

    # グラフ描画
    fig, ax = plt.subplots()
    ax.scatter(x, y, label="データ点", alpha=0.7)
    ax.plot(x, y_pred, color="red", label="回帰直線")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()
    st.pyplot(fig)

    # 結果の表示
    st.write(f"**回帰式：** y = {slope:.2f}x + {intercept:.2f}")
    st.write(f"**相関係数（r）：** {r:.3f}")
    st.write(f"**決定係数（R²）：** {r2:.3f}")
else:
    st.info("Excelファイルをアップロードすると、散布図が表示されます。")
