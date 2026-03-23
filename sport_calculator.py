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
# 移动端优先样式
# ============================================================
st.markdown("""
<style>
    /* 缩小 Streamlit 默认边距，移动端更紧凑 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* 页面大标题 */
    h1 {
        font-size: 1.4rem !important;
        margin-bottom: 0 !important;
    }

    /* 主区块标题 */
    .sec {
        font-size: 1.1rem;
        font-weight: 700;
        color: #262730;
        margin: 1.2rem 0 0.4rem 0;
        padding-bottom: 0.25rem;
        border-bottom: 2px solid #ff4b4b;
    }

    /* 子项标签 */
    .item {
        font-size: 0.9rem;
        font-weight: 600;
        color: #444;
        margin: 0.6rem 0 0.1rem 0;
    }

    /* 总分大字 */
    .big-score {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        line-height: 1;
        padding: 0.3rem 0 0 0;
    }
    .grade-label {
        font-size: 1.15rem;
        text-align: center;
        padding: 0.1rem 0 0.4rem 0;
    }

    /* metric 卡片文字缩小 */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }

    /* 表格字体 */
    .stDataFrame {
        font-size: 0.85rem;
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
st.markdown('<div class="sec">📋 基本信息</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("性别", ["男", "女"], key="gender")
with col2:
    grade = st.selectbox("年级", [1, 2, 3, 4, 5, 6], key="grade",
                         format_func=lambda x: f"{x}年级")

# ============================================================
# 测试项目输入
# ============================================================
st.markdown('<div class="sec">📏 测试数据</div>', unsafe_allow_html=True)

# --- 身体形态 ---
st.markdown('<div class="item">🏋️ 身体形态（BMI）</div>', unsafe_allow_html=True)
col_w, col_h = st.columns(2)
with col_w:
    weight = st.number_input("体重（千克）", min_value=10.0, max_value=150.0, value=30.0, step=0.1)
with col_h:
    height = st.number_input("身高（米）", min_value=0.80, max_value=2.00, value=1.30, step=0.01)

# --- 肺活量 ---
st.markdown('<div class="item">🫁 肺活量</div>', unsafe_allow_html=True)
lung = st.number_input("肺活量（毫升）", min_value=0, max_value=8000, value=1500, step=10)

# --- 50米跑 ---
st.markdown('<div class="item">🏃 50米跑</div>', unsafe_allow_html=True)
run50 = st.number_input("成绩（秒）", min_value=5.0, max_value=20.0, value=10.0, step=0.1, key="run50")

# --- 坐位体前屈 ---
st.markdown('<div class="item">🤸 坐位体前屈</div>', unsafe_allow_html=True)
sit_reach = st.number_input("成绩（厘米）", min_value=-20.0, max_value=30.0, value=5.0, step=0.1, key="reach")

# --- 一分钟跳绳 ---
st.markdown('<div class="item">🪢 一分钟跳绳</div>', unsafe_allow_html=True)
jump_rope = st.number_input("次数", min_value=0, max_value=300, value=80, step=1, key="rope")

# --- 仰卧起坐（3-6年级）---
sit_up_count = 0
if grade >= 3:
    st.markdown('<div class="item">💪 一分钟仰卧起坐</div>', unsafe_allow_html=True)
    sit_up_count = st.number_input("次数", min_value=0, max_value=100, value=30, step=1, key="situp")

# --- 50米×8往返跑（5-6年级）---
run8_seconds = 0
if grade >= 5:
    st.markdown('<div class="item">🔄 50米×8往返跑</div>', unsafe_allow_html=True)
    col_m, col_s = st.columns(2)
    with col_m:
        run8_min = st.number_input("分", min_value=0, max_value=5, value=1, step=1, key="r8m")
    with col_s:
        run8_sec = st.number_input("秒", min_value=0, max_value=59, value=45, step=1, key="r8s")
    run8_seconds = run8_min * 60 + run8_sec

# ============================================================
# 计算
# ============================================================
st.divider()

if st.button("🧮 计算成绩", type="primary", use_container_width=True):

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

    # --- BMI ---
    bmi_value = weight / (height ** 2) if height > 0 else 0

    # --- 显示结果 ---
    st.markdown('<div class="sec">📊 测试结果</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="big-score">{final}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="grade-label">{grade_label}</div>', unsafe_allow_html=True)

    # --- 汇总 metric ---
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("标准分", f"{total}")
    col_b.metric("跳绳加分", f"+{jump_rope_bonus}")
    col_c.metric("最终总分", f"{final}")

    # --- 详细得分 ---
    items = [
        ("BMI", f"{bmi_value:.1f}", bmi_score, sc.WEIGHTS[grade]["bmi"]),
        ("肺活量", f"{lung}ml", lung_score, sc.WEIGHTS[grade]["lung"]),
        ("50米跑", f"{run50}s", run50_score, sc.WEIGHTS[grade]["run50"]),
        ("体前屈", f"{sit_reach}cm", sit_reach_score, sc.WEIGHTS[grade]["sit_reach"]),
    ]
    if grade >= 3:
        items.append(("仰卧起坐", f"{sit_up_count}次", sit_up_score, sc.WEIGHTS[grade]["sit_up"]))
    items.append(("跳绳", f"{jump_rope}次", jump_rope_score, sc.WEIGHTS[grade]["jump_rope"]))
    if grade >= 5:
        items.append(("往返跑", f"{run8_min}'{run8_sec}\"", run8_score, sc.WEIGHTS[grade]["run8"]))

    df = pd.DataFrame(items, columns=["项目", "成绩", "得分", "权重"])
    df["权重"] = df["权重"].apply(lambda x: f"{x:.0%}")
    df["等级"] = df["得分"].apply(sc.get_grade_label)
    st.dataframe(df.set_index("项目"), use_container_width=True)

    # --- 柱状图 ---
    chart_data = pd.DataFrame(
        [(r[0], r[2]) for r in items], columns=["项目", "得分"]
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
        margin=dict(t=5, b=5, l=5, r=5),
        height=280,
    )
    fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="及格")
    fig.add_hline(y=90, line_dash="dash", line_color="green", annotation_text="优秀")
    st.plotly_chart(fig, use_container_width=True)

    # --- 雷达图 ---
    radar_data = pd.DataFrame(
        [(r[0], r[2]) for r in items], columns=["项目", "得分"]
    )
    fig_r = px.line_polar(
        radar_data, r="得分", theta="项目",
        line_close=True, range_r=[0, 100],
    )
    fig_r.update_traces(fill="toself", fillcolor="rgba(99,110,250,0.2)")
    fig_r.update_layout(margin=dict(t=5, b=5, l=30, r=30), height=280)
    st.plotly_chart(fig_r, use_container_width=True)
