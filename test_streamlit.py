import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st
import io

# ✅ 使用仓库中的 NotoSansSC-Light.otf 字体
FONT_PATH = "NotoSansSC-Light.otf"
my_font = fm.FontProperties(fname=FONT_PATH)

# 避免负号显示为方块
plt.rcParams['axes.unicode_minus'] = False   

REQUIRED_COLS = ["姓名", "总分", "日期"]

st.title("📊 学生成绩分析工具 (Web版)")

# 上传 Excel 文件
uploaded_file = st.file_uploader("请选择Excel文件", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
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
            dates = stu["日期"].dt.strftime("%Y-%m-%d")
            median_dates = median_df["日期"].dt.strftime("%Y-%m-%d")

            ax.plot(dates, stu["总分"], marker='o', label=f"{student_name} 总分")
            ax.plot(median_dates, median_df["总分"], marker='s', linestyle='--', label="班级总分中位数")
            ax.set_xticks(dates)

            # ✅ 设置中文字体
            ax.set_title(f"{student_name} 历次成绩走势", fontproperties=my_font)
            ax.set_xlabel("考试日期", fontproperties=my_font)
            ax.set_ylabel("总分", fontproperties=my_font)
            ax.legend(prop=my_font)
            ax.grid(True)

            st.pyplot(fig)

            # 提供下载图片功能
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            st.download_button(
                label="💾 下载图表 (PNG)",
                data=buf.getvalue(),
                file_name=f"{student_name}_成绩走势.png",
                mime="image/png"
            )
