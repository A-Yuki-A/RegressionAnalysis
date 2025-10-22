import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os

st.title("🍦 アイス売上と各項目の関係を調べよう")

# === フォント設定 ===
# 現在のディレクトリを基準にフォントパスを指定
font_path = os.path.join("fonts", "SourceHanCodeJP-Regular.otf")

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams["font.family"] = "Source Han Code JP"
else:
    st.warning("⚠️ 日本語フォントが見つかりません。fonts フォルダに SourceHanCodeJP-Regular.otf を置いてください。")

# === ファイルアップロード ===
uploaded_file = st.file_uploader("アイス売上データ（Excel）をアップロードしてください", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("データの中身")
    st.dataframe(df.head())

    # 「年」「月」を除外した列を抽出
    valid_columns = [c for c in df.columns if not any(word in c for word in ["年", "月"])]

    # 目的変数（売上）
    y_col = st.selectbox("売上（目的変数）にする列を選んでください", valid_columns)

    # 説明変数（売上に影響しそうな項目）
    x_candidates = [c for c in valid_columns if c != y_col]
    x_col = st.selectbox("売上に影響しそうな項目（説明変数）を選んでください", x_candidates)

    # データの抽出
    x = df[x_col]
    y = df[y_col]

    # 回帰直線の計算
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept

    # 相関係数・決定係数
    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2

    # 散布図の描画
    fig, ax = plt.subplots()
    ax.scatter(x, y, label="データ点", alpha=0.7)
    ax.plot(x, y_pred, color="red", label="回帰直線")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()
    st.pyplot(fig)

    # 結果の表示
    st.markdown(f"**回帰式：** y = {slope:.2f}x + {intercept:.2f}")
    st.markdown(f"**相関係数（r）：** {r:.3f}")
    st.markdown(f"**決定係数（R²）：** {r2:.3f}")
else:
    st.info("Excelファイルをアップロードすると、散布図が表示されます。")
