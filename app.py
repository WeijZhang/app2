# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 12:17:46 2023

@author: A
"""
#%%
import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# 请确保model.pkl的路径与实际路径相匹配
MODEL_PATH = 'model.pkl'
# 载入预先训练好的模型
model = load(MODEL_PATH)

# 定义一个函数来处理输入并进行预测
def predict_properties(input_features):
    # 1. 定义 RM_SS 和 RM_AB
    RM_SS = input_features['Mass_ratio_sewage_sludge'] / 100
    RM_AB = input_features['Mass_ratio_algae_biomass'] / 100

    # 2. 计算 RM_C, RM_H, RM_O, RM_S, RM_N, RM_Ash
    RM_C = input_features['C_sewage_sludge'] * RM_SS + input_features['C_algae_biomass'] * RM_AB
    RM_H = input_features['H_sewage_sludge'] * RM_SS + input_features['H_algae_biomass'] * RM_AB
    RM_O = input_features['O_sewage_sludge'] * RM_SS + input_features['O_algae_biomass'] * RM_AB
    RM_S = input_features['S_sewage_sludge'] * RM_SS + input_features['S_algae_biomass'] * RM_AB
    RM_N = input_features['N_sewage_sludge'] * RM_SS + input_features['N_algae_biomass'] * RM_AB
    RM_Ash = input_features['Ash_sewage_sludge'] * RM_SS + input_features['Ash_algae_biomass'] * RM_AB

    # 3. 计算 RM_HC, RM_OC, RM_NC
    RM_HC = (12 * RM_H) / (1 * RM_C)
    RM_OC = (16 * RM_O) / (16 * RM_C)
    RM_NC = (14 * RM_N) / (16 * RM_C)

    # 4. 合并输入特征并转换为 NumPy 数组
    input_array = np.array([[
        RM_C, RM_H, RM_O, RM_S, RM_N, RM_Ash, RM_HC, RM_OC, RM_NC,
        input_features['Solid_content'],
        input_features['Temperature'],
        input_features['Residence_time'],
        18, 1000, 84.93, 309
    ]])

    # 5. 使用模型进行预测
    prediction = model.predict(input_array)
    return prediction
#%%
# 使用 CSS 来自定义 Streamlit 应用的样式
st.markdown(f"""
    <style>
    html, body {{
        font-family: 'Times New Roman', Times, serif;
    }}
    [class*="st-"] {{
        font-family: 'Times New Roman', Times, serif;
    }}
    h1 {{
        font-size: 27px; /* 设置表头字体大小 */
    }}
    .reportview-container {{
        background-color: #ADD8E6; /* 修改为浅蓝色背景 */
    }}
    .sidebar .sidebar-content {{
        background-color: #456789; /* 侧边栏颜色 */
    }}
    </style>
    """, unsafe_allow_html=True)

#%%
st.markdown('<h1 class="big-font">Predict properties of bio-oil producted from co-liquefaction</h1>', unsafe_allow_html=True)


# 输入字段布局
col1, col2, col3 = st.columns(3)



with col1:
    st.markdown(f'<div class="st-bc">', unsafe_allow_html=True)
    st.markdown('**Sewage Sludge**')
    c_sewage_sludge = st.number_input('C (wt.%)', min_value=0.0, value=50.0, step=0.1, key='c_sew_sludge')
    h_sewage_sludge = st.number_input('H (wt.%)', min_value=0.0, value=5.0, step=0.1, key='h_sew_sludge')
    o_sewage_sludge = st.number_input('O (wt.%)', min_value=0.0, value=40.0, step=0.1, key='o_sew_sludge')
    s_sewage_sludge = st.number_input('S (wt.%)', min_value=0.0, value=0.5, step=0.1, key='s_sew_sludge')
    n_sewage_sludge = st.number_input('N (wt.%)', min_value=0.0, value=1.5, step=0.1, key='n_sew_sludge')
    ash_sewage_sludge = st.number_input('Ash (wt.%)', min_value=0.0, value=5.0, step=0.1, key='ash_sew_sludge')
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="st-ba">', unsafe_allow_html=True)
    st.markdown('**Algae Biomass**')
    c_algae_biomass = st.number_input('C (wt.%)', min_value=0.0, value=50.0, step=0.1, key='c_alg_biomass')
    h_algae_biomass = st.number_input('H (wt.%)', min_value=0.0, value=6.0, step=0.1, key='h_alg_biomass')
    o_algae_biomass = st.number_input('O (wt.%)', min_value=0.0, value=44.0, step=0.1, key='o_alg_biomass')
    s_algae_biomass = st.number_input('S (wt.%)', min_value=0.0, value=0.0, step=0.1, key='s_alg_biomass')
    n_algae_biomass = st.number_input('N (wt.%)', min_value=0.0, value=1.0, step=0.1, key='n_alg_biomass')
    ash_algae_biomass = st.number_input('Ash (wt.%)', min_value=0.0, value=5.0, step=0.1, key='ash_alg_biomass')
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="st-oc">', unsafe_allow_html=True)
    st.markdown('**Operating Conditions**')
    temperature = st.number_input('Temperature (°C)', min_value=0.0, value=300.0, step=0.1, key='temp')
    solid_content = st.number_input('Solid content (%)', min_value=0.0, value=20.0, step=0.1, key='solid_cont')
    residence_time = st.number_input('Residence time (min)', min_value=0.0, value=60.0, step=0.1, key='res_time')
    mass_ratio_sewage_sludge = st.number_input('Mass ratio of Sewage sludge (%)', min_value=0.0, value=50.0, step=0.1, key='mass_ratio_sew')
    mass_ratio_algae_biomass = st.number_input('Mass ratio of Algae biomass (%)', min_value=0.0, value=50.0, step=0.1, key='mass_ratio_alg')
    st.markdown('</div>', unsafe_allow_html=True)
# 收集所有输入数据
input_features = {
    'C_sewage_sludge': c_sewage_sludge,
    'H_sewage_sludge': h_sewage_sludge,
    'O_sewage_sludge': o_sewage_sludge,
    'S_sewage_sludge': s_sewage_sludge,
    'N_sewage_sludge': n_sewage_sludge,
    'Ash_sewage_sludge': ash_sewage_sludge,
    'C_algae_biomass': c_algae_biomass,
    'H_algae_biomass': h_algae_biomass,
    'O_algae_biomass': o_algae_biomass,
    'S_algae_biomass': s_algae_biomass,
    'N_algae_biomass': n_algae_biomass,
    'Ash_algae_biomass': ash_algae_biomass,
    'Temperature': temperature,
    'Solid_content': solid_content,
    'Residence_time': residence_time,
    'Mass_ratio_sewage_sludge': mass_ratio_sewage_sludge,
    'Mass_ratio_algae_biomass': mass_ratio_algae_biomass,
}
#%%
# 当用户点击预测按钮时执行
# 在每列之上显示标题
st.write('Prediction of bio-oil properties:')# 定义三列
col1, col2, col3 = st.columns(3)

# 当用户点击预测按钮时执行
if st.button('Predict'):
    prediction = predict_properties(input_features)
    
    # 提取每个预测值并格式化
    yield_oil = prediction[0, 0]  # 假设预测结果是一个二维数组
    n_oil = prediction[0, 1]
    er_oil = prediction[0, 2]

    # 在三列中显示预测结果
    col1.write(f'Yield_oil (%): {yield_oil:.2f}')
    col2.write(f'N_oil (%): {n_oil:.2f}')
    col3.write(f'ER_oil (%): {er_oil:.2f}')
else:
    # 按钮未点击时也在三列中显示标签
    col1.write('Yield_oil (%) =')
    col2.write('N_oil (%) =')
    col3.write('ER_oil (%) =')


#%%
