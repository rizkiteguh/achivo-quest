import streamlit as st
import pandas as pd
from PIL import Image
import altair as alt
from datetime import date, datetime

# Assets
ICON = Image.open('img/icon.ico')
LOGO = Image.open("img/logo.png")
NOW = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

# Dataset
OKRS = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRb9wWxkjM9Hkv2n8z8A9YU2WpSp7_C0Ge46TN-uCwQcoHSziamAdGh8y56sKrIUkybNwi7AV-Jam39/pub?gid=1548015023&single=true&output=csv')
OBJECTIVES = pd.pivot_table(
    data=OKRS,
    index='Objective',
    values='Progress',
    aggfunc='mean'
).reset_index()

PERFORMANCE = pd.pivot_table(
    data=OKRS,
    index='Department',
    values='Progress',
    aggfunc='mean'
).reset_index().sort_values(by='Progress', ascending=False)

st.set_page_config(
    page_title='Achivo Quest',
    layout='wide',
    page_icon=ICON
)

# HEADER
head1, head2 = st.columns(2)
with head1:
    st.markdown('## Achivo Quest')
with head2:
    st.markdown(f'<h4 style="text-align: right;">{NOW}</h4>', unsafe_allow_html=True)

# METRICS
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric('Overall achievement', '100%')
with m2:
    st.metric('Metric 2', 100)
with m3:
    st.metric('Metric 3', 100)
with m4:
    st.metric('Confidence score', '100%')

# OBJECTIVE PROGRESS
st.markdown('#### Objectives')

st.dataframe(
    OBJECTIVES,
    column_config={
        'Progress':st.column_config.ProgressColumn(
            'Progress',
            min_value=0,
            max_value=1
        )
    },
    use_container_width=True,
    hide_index=True
)

st.markdown('#### Key Results')
krops1, krops2 = st.columns(2)
with krops1:
    obj = st.selectbox('Objective', options=OKRS['Objective'].unique())
with krops2:
    dept = st.selectbox('Department', options=OKRS[OKRS['Objective']==obj]['Department'].unique())

KR = OKRS[(OKRS['Department']==dept) & (OKRS['Objective']==obj)]
cols = ['Key Results','Tasks','Progress']

st.dataframe(
    KR[cols],
    use_container_width=True,
    hide_index=True
)

st.markdown('#### Performance')
st.dataframe(
    PERFORMANCE,
    column_config={
        'Progress':st.column_config.ProgressColumn(
            'Progress',
            min_value=0,
            max_value=1
        )
    },
    use_container_width=True,
    hide_index=True)