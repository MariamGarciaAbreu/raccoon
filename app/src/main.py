import streamlit as st
import pandas as pd
import utils

st.set_page_config(
    page_title="Personal Finances Dashboard",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="expanded")

@st.cache_data
def get_data_from_csv():
    return (pd.read_csv('../../data/transactions.csv'), pd.read_csv('../../data/categories.csv'))

transactions, categories = get_data_from_csv()

# ---- DATA TREATMENT ----
transactions["Debit"] = transactions["Debit"].fillna(0)
transactions["Credit"] = transactions["Credit"].fillna(0)
transactions["Actual"] = transactions["Credit"] - transactions["Debit"]
transactions['Date'] = pd.to_datetime(transactions.Date, format='%d/%m/%Y')
transactions['Date'] = transactions['Date'].dt.strftime('%m/%d/%Y')
transactions["Month"] = pd.to_datetime(transactions["Date"]).dt.month
transactions["Year"] = pd.to_datetime(transactions["Date"]).dt.year
transactions_with_categories = pd.merge(transactions, categories, on='Sub-category', how='left')

# ---- SIDEBAR ----
with st.sidebar:
    st.title('Choose a date range')
    
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
    st.write("You wanna wassup between", utils.convert_month_num_to_name(start_month), "and", utils.convert_month_num_to_name(end_month))

filtered_transactions = transactions_with_categories.query('Year == @selected_year and Month >= @start_month and Month <= @end_month')

if filtered_transactions.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() 

# ---- MAIN PAGE ----
def calculate_financial_freedom_values():
    passive_income = filtered_transactions.loc[filtered_transactions['Category'] == '✌🏽 Passive', 'Actual'].sum()
    needs = filtered_transactions.loc[filtered_transactions['Type'] == 'Need', 'Actual'].sum()

    if needs == 0:
        return 0
    
    return passive_income - abs(needs), round((needs / passive_income)* 100, 2)

col1, col2, col3 = st.columns(3)

with col1:
    total_income = filtered_transactions.query('`Category Type` == "Income"')["Actual"].sum()
    st.metric("Total Income", utils.format_currency(total_income))
with col2:
    total_expenses = filtered_transactions.query('`Category Type` == "Expense"')["Actual"].sum()
    st.metric("Total Expenses", utils.format_currency(total_expenses))
with col3:
    financial_freedom_amount, financial_freedom_percentage = calculate_financial_freedom_values()
    st.metric(label="Financial Freedom", value=utils.format_currency(financial_freedom_amount), delta=financial_freedom_percentage, delta_color="normal", help="Passive Income - Needs")

st.markdown("""---""")
