import streamlit as st
import pandas as pd
from PIL import Image
from datetime import date, datetime
from numerize import numerize
import math

# Assets
ICON = Image.open('img/icon.ico')
LOGO = Image.open("img/logo.png")
NOW = date(2023,12,8)

st.set_page_config(
    page_title='Achivo Quest',
    layout='wide',
    page_icon=ICON
)

# Dataset
@st.cache_data
def get_df():
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRb9wWxkjM9Hkv2n8z8A9YU2WpSp7_C0Ge46TN-uCwQcoHSziamAdGh8y56sKrIUkybNwi7AV-Jam39/pub?gid=1548015023&single=true&output=csv')
    return df

OKRS = get_df()

OBJECTIVES = pd.pivot_table(
    data=OKRS,
    index='Objective',
    values=['Sprint Point','Weight'],
    aggfunc='sum'
).reset_index()
OBJECTIVES['Progress'] = OBJECTIVES['Weight'] / OBJECTIVES['Sprint Point']
OBJECTIVES = OBJECTIVES[['Objective','Progress']]

PERFORMANCE = pd.pivot_table(
    data=OKRS,
    index='Department',
    values=['Sprint Point','Weight'],
    aggfunc='sum'
).reset_index()
PERFORMANCE['Progress'] = PERFORMANCE['Weight'] / PERFORMANCE['Sprint Point']
PERFORMANCE.sort_values(by='Progress', ascending=False, inplace=True)
PERFORMANCE = PERFORMANCE[['Department','Progress']]

salary_df = pd.pivot_table(
        data=OKRS,
        index=['Assigne','Department'],
        values=['Salary Quarterly','Weight','Sprint Point'],
        aggfunc=
            {
                'Salary Quarterly':'mean',
                'Weight':'sum',
                'Sprint Point':'sum'
            }
    ).reset_index()
salary_df['Utilization'] = salary_df['Weight'] / salary_df['Sprint Point']
salary_df['Value Realized'] = salary_df['Utilization'] * salary_df['Salary Quarterly']

cost = float(salary_df['Salary Quarterly'].sum())
realized = float(salary_df['Value Realized'].sum())

salary_df.drop(columns=['Weight','Salary Quarterly'], inplace=True)

# HEADER
head1, head2 = st.columns(2)
with head1:
    st.markdown('## Achivo Quest: Central Dashboard')
with head2:
    st.markdown(f'<h2 style="text-align: right;">Q{math.ceil(NOW.month/3)} {NOW.year}</h2>', unsafe_allow_html=True)

# METRICS
m1, m2 = st.columns([1,4])
with m1:
    overall = OKRS['Weight'].sum()/OKRS['Sprint Point'].sum()*100.0
    st.metric('Overall achievement', f'{overall:.2f}%')

    st.metric(
        'Salary utilization', 
        f'{numerize.numerize(realized)} IDR', 
        f'{numerize.numerize(realized-cost)} IDR',
        delta_color='normal',)
with m2:
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

# OBJECTIVE PROGRESS

st.markdown('#### Key Results')
obj = st.selectbox('Objective', options=OKRS['Objective'].unique())

KR = OKRS[OKRS['Objective']==obj].sort_values(by='Sprint Point', ascending=False)
cols = ['Tasks','Sprint Point','Start Date','End Date','Progress']

st.dataframe(
    KR[cols],
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

st.markdown('#### Performance')
st.markdown('##### Department')
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

st.markdown('##### Employee')
st.dataframe(
    salary_df.sort_values(by='Sprint Point', ascending=False),
    column_config={
        'Utilization':st.column_config.ProgressColumn(
            'Utilization',
            min_value=0,
            max_value=1
        )
    },
    use_container_width=True,
    hide_index=True
)