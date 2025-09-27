import streamlit as st
import pandas as pd
import altair as alt
# import plotly.express as px
import numpy as np
from utils import convert_month_num_to_name


st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

transactions = pd.read_csv('../../data/transactions.csv')
transactions["Debit"] = transactions["Debit"].fillna(0)
transactions["Credit"] = transactions["Credit"].fillna(0)
transactions["Actual"] = transactions["Credit"] - transactions["Debit"]
transactions['Date'] = pd.to_datetime(transactions.Date)
transactions['Date'] = transactions['Date'].dt.strftime('%d/%m/%Y')
transactions["Month"] = pd.to_datetime(transactions["Date"]).dt.month
transactions["Year"] = pd.to_datetime(transactions["Date"]).dt.year


with st.sidebar:
    st.title('💵 Personal Finances Dashboard')
    
    year_list = list(transactions.Year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = transactions[transactions.Year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="Actual", ascending=False)

    month_list = list(df_selected_year.Month.unique())
    start_month, end_month = st.select_slider(
        'Select a month range',
        options=month_list,
        value=(month_list[0], month_list[-1])

    )   
    st.write("You wanna wassup between", convert_month_num_to_name(start_month), "and", convert_month_num_to_name(end_month))



categories = pd.read_csv('../../data/categories.csv')

transactions_with_steroids = pd.merge(transactions, categories, on='Sub-category', how='left')
transactions_with_steroids = transactions_with_steroids.loc[transactions_with_steroids['Year'] == selected_year]
transactions_with_steroids = transactions_with_steroids.loc[(transactions_with_steroids['Month'] >= start_month) & (transactions_with_steroids['Month'] <= end_month)]
transactions_with_steroids["Income surplus/(deficit)"] = np.where(transactions_with_steroids['Category Type'] == 'Income', transactions_with_steroids['Actual'], 0)
transactions_with_steroids["Expense surplus/(deficit)"] = np.where(transactions_with_steroids['Category Type'] == 'Expense', transactions_with_steroids['Actual'], 0)

grouped_transactions = transactions_with_steroids.groupby(["Category Type","Category"])[['Actual']].sum()  

st.write("### Monthly report")
st.dataframe(grouped_transactions, height=250, use_container_width=True)

def calculate_financial_freedom():
    passive_income = transactions_with_steroids.loc[transactions_with_steroids['Category'] == '✌🏽 Passive', 'Actual'].sum()
    needs = transactions_with_steroids.loc[transactions_with_steroids['Type'] == 'Need', 'Actual'].sum()

    return passive_income - abs(needs)

st.metric(label="Financial Freedom", value=calculate_financial_freedom(), delta=-1, delta_color="normal", help="Passive Income - Needs")