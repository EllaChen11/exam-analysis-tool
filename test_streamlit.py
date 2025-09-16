import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import io

# 字体设置（跨平台支持中文）
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

REQUIRED_COLS = ["姓名", "总分", "日期"]

st.title("📊 学生成绩分析工具 (Web版)")

# 上传 Excel 文件
uploaded_file = st.file_uploader("请选择Excel文件", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        st.stop()

    # 检查列名
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        st.error(f"Excel缺少必要列: {missing}")
        st.stop()

    # 数据预处理
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df = df.dropna(subset=["姓名", "总分", "日期"])
    df = df.sort_values(by="日期")
    df["总分"] = pd.to_numeric(df["总分"], errors="coerce")
    df = df.dropna(subset=["总分"])

    st.success("✅ 文件加载成功！")

    # 选择学生姓名
    student_name = st.selectbox("请选择学生姓名", df["姓名"].unique())

    if st.button("分析并绘图"):
        stu = df[df["姓名"] == student_name].copy()
        if stu.empty:
            st.warning(f"未找到 {student_name} 的记录")
        else:
            # 每次考试的班级中位数
            median_df = df.groupby("日期")["总分"].median().reset_index()

            # 绘制图表
            fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
            dates = stu["日期"].dt.strftime("%Y-%m-%d").tolist()
            median_dates = median_df["日期"].dt.strftime("%Y-%m-%d").tolist()

            ax.plot(dates, stu["总分"], marker='o', label=f"{student_name} 总分")
            ax.plot(median_dates, median_df["总分"], marker='s', linestyle='--', label="班级总分中位数")

            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=45, ha="right")

            ax.set_title(f"{student_name} 历次成绩走势")
            ax.set_xlabel("考试日期")
            ax.set_ylabel("总分")
            ax.grid(True)
            ax.legend()

            st.pyplot(fig)

            # 提供下载图表功能
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="💾 下载图表 (PNG)",
                data=buf,
                file_name=f"{student_name}_成绩走势.png",
                mime="image/png"
            )
