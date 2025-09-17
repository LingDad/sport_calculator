import streamlit as st
import pandas as pd
import plotly.express as px
import score_criteria as sc

SPORT_IMAGE_URL = "https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=crop&w=1200&q=80"

# streamlit ui
st.image(SPORT_IMAGE_URL, caption="为运动加油！", use_container_width=True)
gender = st.selectbox("性别", ["男", "女"])
grade = st.selectbox("年级", [1, 2, 3, 4, 5, 6])
weight = st.number_input("体重(千克)", min_value=0.0, step=0.1)
height = st.number_input("身高(米)", min_value=0.0, step=0.01)
sit_reach = st.number_input("坐位体前屈(厘米)", min_value=0.0, step=0.1)
sit_up = st.number_input("仰卧起坐(次)", min_value=0.0, step=1.0)
lung_capacity = st.number_input("肺活量(毫升)", min_value=0.0, step=1.0)
run_50 = st.number_input("50米跑(秒)", min_value=0.0, step=0.1)
jump_rope = st.number_input("一分钟跳绳(次)", min_value=0.0, step=1.0)
if grade >= 5:
    run_8r = st.number_input("50米x8往返跑(秒)", min_value=0.0, step=0.1)

if st.button("计算体测分数"):
    bmi_score = sc.get_bmi_score(gender, grade, weight, height)
    lung_capacity_score = sc.get_lung_capacity_score(gender, grade, lung_capacity)
    run_score = sc.get_50m_run_score(gender, grade, run_50)
    sit_reach_score = sc.get_sit_and_reach_score(gender, grade, sit_reach)
    sit_up_score = sc.get_sit_up_score(gender, grade, sit_up)
    jump_rope_score = sc.get_jump_rope_score(gender, grade, jump_rope)
    jump_rope_bonus = sc.get_jump_rope_bonus(gender, grade, jump_rope)
    if grade >= 5:
        run_8r_score = sc.get_50m_8r_run_score(gender, grade, run_8r)
        total_score = sc.get_total_score(grade, bmi_score, lung_capacity_score, run_score, sit_reach_score, sit_up_score, jump_rope_score, run_8r_score)
    else:
        total_score = sc.get_total_score(grade, bmi_score, lung_capacity_score, run_score, sit_reach_score, sit_up_score, jump_rope_score)
        
    if grade >= 5:
        data = [
            ["BMI", bmi_score],
            ["肺活量", lung_capacity_score],
            ["50米跑", run_score],
            ["坐位体前屈", sit_reach_score],
            ["仰卧起坐", sit_up_score],
            ["一分钟跳绳", jump_rope_score],
            ["50米x8往返跑", run_8r_score],
            ["一分钟跳绳加分", jump_rope_bonus],
            ["标准分", total_score],
            ["总分(标准分+加分)", total_score + jump_rope_bonus],
        ]
    else:
        data = [
            ["BMI", bmi_score],
            ["肺活量", lung_capacity_score],
            ["50米跑", run_score],
            ["坐位体前屈", sit_reach_score],
            ["仰卧起坐", sit_up_score],
            ["一分钟跳绳", jump_rope_score],
            ["一分钟跳绳加分", jump_rope_bonus],
            ["标准分", total_score],
            ["总分(标准分+加分)", total_score + jump_rope_bonus],
        ]

    df = pd.DataFrame(data, columns=["项目", "分数"])
    
    # 显示表格
    st.table(df.set_index("项目"))

    # 创建并显示柱状图
    fig = px.bar(df, x="项目", y="分数", title="体测分数柱状图")
    st.plotly_chart(fig)
