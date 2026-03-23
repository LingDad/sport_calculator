import streamlit as st
import pandas as pd
import plotly.express as px
import score_criteria as sc

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="小学生体测计算器",
    page_icon="🏃",
    layout="centered",
)

# ============================================================
# 样式
# ============================================================
st.markdown("""
<style>
    .big-score {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        padding: 0.5rem 0 0 0;
        line-height: 1;
    }
    .grade-label {
        font-size: 1.5rem;
        text-align: center;
        padding: 0.2rem 0 0.5rem 0;
    }
    .section-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #555;
        margin: 0.8rem 0 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 标题
# ============================================================
st.title("🏃 小学生体质健康测试计算器")
st.caption("依据《国家学生体质健康标准》（2024年修订）")

# ============================================================
# 基本信息
# ============================================================
st.header("📋 基本信息")
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("性别", ["男", "女"], key="gender")
with col2:
    grade = st.selectbox("年级", [1, 2, 3, 4, 5, 6], key="grade",
                         format_func=lambda x: f"{x}年级")

# ============================================================
# 测试项目输入
# ============================================================
st.header("📏 测试数据")

# --- 身体形态 ---
st.markdown("**🏋️ 身体形态（BMI）**")
col_w, col_h = st.columns(2)
with col_w:
    weight = st.number_input("体重（千克）", min_value=10.0, max_value=150.0, value=30.0, step=0.1)
with col_h:
    height = st.number_input("身高（米）", min_value=0.80, max_value=2.00, value=1.30, step=0.01)

# --- 肺活量 ---
st.markdown("**🫁 肺活量**")
lung = st.number_input("肺活量（毫升）", min_value=0, max_value=8000, value=1500, step=10)

# --- 50米跑 ---
st.markdown("**🏃 50米跑**")
run50 = st.number_input("50米跑成绩（秒）", min_value=5.0, max_value=20.0, value=10.0, step=0.1)

# --- 坐位体前屈 ---
st.markdown("**🤸 坐位体前屈**")
sit_reach = st.number_input("坐位体前屈（厘米）", min_value=-20.0, max_value=30.0, value=5.0, step=0.1)

# --- 一分钟跳绳 ---
st.markdown("**🪢 一分钟跳绳**")
jump_rope = st.number_input("一分钟跳绳（次）", min_value=0, max_value=300, value=80, step=1)

# --- 仰卧起坐（3-6年级）---
sit_up_count = 0
if grade >= 3:
    st.markdown("**💪 一分钟仰卧起坐**")
    sit_up_count = st.number_input("一分钟仰卧起坐（次）", min_value=0, max_value=100, value=30, step=1)

# --- 50米×8往返跑（5-6年级）---
run8_seconds = 0
if grade >= 5:
    st.markdown("**🔄 50米×8往返跑**")
    col_m, col_s = st.columns(2)
    with col_m:
        run8_min = st.number_input("分钟", min_value=0, max_value=5, value=1, step=1, key="run8_min")
    with col_s:
        run8_sec = st.number_input("秒", min_value=0, max_value=59, value=45, step=1, key="run8_sec")
    run8_seconds = run8_min * 60 + run8_sec
    st.caption(f"⏱️ 往返跑成绩：{run8_min}分{run8_sec}秒（共 {run8_seconds} 秒）")

# ============================================================
# 计算
# ============================================================
st.divider()

if st.button("🧮 计算体测成绩", type="primary", use_container_width=True):

    # --- 计算各项得分 ---
    bmi_score = sc.get_bmi_score(gender, grade, weight, height)
    lung_score = sc.get_lung_score(gender, grade, lung)
    run50_score = sc.get_run50_score(gender, grade, run50)
    sit_reach_score = sc.get_sit_reach_score(gender, grade, sit_reach)
    jump_rope_score = sc.get_jump_rope_score(gender, grade, jump_rope)
    jump_rope_bonus = sc.get_jump_rope_bonus(gender, grade, jump_rope)

    scores = {
        "bmi": bmi_score,
        "lung": lung_score,
        "run50": run50_score,
        "sit_reach": sit_reach_score,
        "jump_rope": jump_rope_score,
    }

    if grade >= 3:
        sit_up_score = sc.get_sit_up_score(gender, grade, sit_up_count)
        scores["sit_up"] = sit_up_score

    if grade >= 5:
        run8_score = sc.get_run8_score(gender, grade, run8_seconds)
        scores["run8"] = run8_score

    # --- 加权总分 ---
    total = sc.get_total_score(grade, scores)
    final = total + jump_rope_bonus
    grade_label = sc.get_grade_label(final)

    # --- BMI 显示 ---
    bmi_value = weight / (height ** 2) if height > 0 else 0

    # --- 显示结果 ---
    st.header("📊 测试结果")

    # 总分大字
    st.markdown(f'<div class="big-score">{final}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="grade-label">{grade_label}</div>', unsafe_allow_html=True)

    # --- 详细得分表 ---
    st.markdown("**各项得分明细**")

    items = [
        ("🏋️ BMI", f"{bmi_value:.1f}", bmi_score, sc.WEIGHTS[grade]["bmi"]),
        ("🫁 肺活量", f"{lung} 毫升", lung_score, sc.WEIGHTS[grade]["lung"]),
        ("🏃 50米跑", f"{run50} 秒", run50_score, sc.WEIGHTS[grade]["run50"]),
        ("🤸 坐位体前屈", f"{sit_reach} 厘米", sit_reach_score, sc.WEIGHTS[grade]["sit_reach"]),
    ]

    if grade >= 3:
        items.append(("💪 仰卧起坐", f"{sit_up_count} 次", sit_up_score, sc.WEIGHTS[grade]["sit_up"]))

    items.append(("🪢 跳绳", f"{jump_rope} 次", jump_rope_score, sc.WEIGHTS[grade]["jump_rope"]))

    if grade >= 5:
        items.append(("🔄 往返跑", f"{run8_min}'{run8_sec}\"", run8_score, sc.WEIGHTS[grade]["run8"]))

    df = pd.DataFrame(items, columns=["项目", "成绩", "得分", "权重"])
    df["权重"] = df["权重"].apply(lambda x: f"{x:.0%}")
    df["等级"] = df["得分"].apply(sc.get_grade_label)

    st.dataframe(df.set_index("项目"), use_container_width=True)

    # --- 加分与汇总 ---
    st.markdown("**总分计算**")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("标准分", f"{total}")
    col_b.metric("跳绳加分", f"+{jump_rope_bonus}")
    col_c.metric("最终总分", f"{final}")

    # --- 柱状图 ---
    st.markdown("**得分分布**")
    chart_data = pd.DataFrame(
        [(row[0], row[2]) for row in items],
        columns=["项目", "得分"]
    )
    fig = px.bar(
        chart_data, x="项目", y="得分",
        color="得分",
        color_continuous_scale=["#ff4b4b", "#ffa500", "#00cc96"],
        range_color=[0, 100],
    )
    fig.update_layout(
        yaxis_range=[0, 105],
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=10),
    )
    fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="及格线")
    fig.add_hline(y=90, line_dash="dash", line_color="green", annotation_text="优秀线")
    st.plotly_chart(fig, use_container_width=True)

    # --- 雷达图 ---
    st.markdown("**能力雷达图**")
    radar_data = pd.DataFrame(
        [(row[0].split(" ")[1] if " " in row[0] else row[0], row[2]) for row in items],
        columns=["项目", "得分"]
    )
    fig_radar = px.line_polar(
        radar_data, r="得分", theta="项目",
        line_close=True,
        range_r=[0, 100],
    )
    fig_radar.update_traces(fill="toself", fillcolor="rgba(99, 110, 250, 0.2)")
    fig_radar.update_layout(margin=dict(t=10))
    st.plotly_chart(fig_radar, use_container_width=True)
