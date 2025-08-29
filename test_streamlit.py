import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ 设置全局字体（Streamlit Cloud 无需上传/下载字体）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']  
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

st.title("学生成绩分析工具")

uploaded_file = st.file_uploader("选择 Excel 文件", type=["xls","xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 检查必需列
    required_cols = ["姓名", "总分", "日期"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Excel 缺少必要列：{[c for c in required_cols if c not in df.columns]}")
    else:
        # 数据处理
        df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
        df = df.dropna(subset=["姓名", "总分", "日期"])
        df["总分"] = pd.to_numeric(df["总分"], errors="coerce")

        # 输入学生姓名
        student_name = st.text_input("请输入学生姓名")
        if student_name:
            stu = df[df["姓名"] == student_name]
            if stu.empty:
                st.warning(f"未找到 {student_name} 的记录")
            else:
                median_df = df.groupby("日期")["总分"].median().reset_index()

                # 绘图
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.plot(stu["日期"], stu["总分"], marker='o', label=f"{student_name} 总分")
                ax.plot(median_df["日期"], median_df["总分"], marker='s', linestyle='--', label="班级中位数")

                ax.set_title(f"{student_name} 历次成绩走势")
                ax.set_xlabel("考试日期")
                ax.set_ylabel("总分")
                ax.legend()
                ax.grid(True)

                st.pyplot(fig)
