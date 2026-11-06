import streamlit as st
import pandas as pd

st.title(
    "AI経理業務アシスタント"
)

uploaded_file = st.file_uploader(
    "AP管理表をアップロード",
    type="xlsx"
)

if uploaded_file:

    df = pd.read_excel(
        uploaded_file
    )

    st.dataframe(df)

    total_amount = df["金額"].sum()

    st.metric(
        "総支払額",
        f"{total_amount:,}円"
    )

    st.metric(
        "取引先数",
        df["取引先"].nunique()
    )

    summary = (
        df.groupby("取引先")
          ["金額"]
          .sum()
    )

    st.subheader(
        "取引先別支払額"
    )

    st.dataframe(summary)

    st.bar_chart(summary)

    errors = df[
        df["取引先"].isna()
    ]

    st.subheader(
        "エラー一覧"
    )

    st.dataframe(errors)

    top_vendor = (
        summary.idxmax()
    )

    top_amount = (
        summary.max()
    )

    comment = f"""
    分析結果

    最大支払先は
    {top_vendor}

    支払額は
    {top_amount:,}円です。

    支払集中状況を確認してください。
    """

    st.info(comment)

    currency = (
        df.groupby("通貨")
          ["金額"]
          .sum()
    )

    st.dataframe(currency)

    csv = summary.to_csv()

    st.download_button(
        "集計結果ダウンロード",
        csv,
        "summary.csv"
    )

    summary.to_excel(
        "payment_report.xlsx"
    )