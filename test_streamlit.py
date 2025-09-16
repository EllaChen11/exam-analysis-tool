# 读 Excel
df = pd.read_excel(uploaded_file, engine="openpyxl")

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

# 提供下载
import io
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight")
buf.seek(0)
st.download_button(
    label="💾 下载图表 (PNG)",
    data=buf,
    file_name=f"{student_name}_成绩走势.png",
    mime="image/png"
)
