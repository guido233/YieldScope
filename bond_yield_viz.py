import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive Bond Yield Curve Visualization")

# Load data from the provided CSV file
DATA_PATH = 'full_bond_yield_2000_2025.csv'

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.rename(columns={
        '曲线名称': 'Curve Name',
        '日期': 'Date',
        '3月': '3M',
        '6月': '6M',
        '1年': '1Y',
        '3年': '3Y',
        '5年': '5Y',
        '7年': '7Y',
        '10年': '10Y',
        '30年': '30Y'
    }, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

data = load_data(DATA_PATH)

# Display data preview
st.subheader("Data Preview")
st.dataframe(data.head())

# Select date range
date_range = st.date_input(
    "Select Date Range",
    [data['Date'].min(), data['Date'].max()],
    min_value=data['Date'].min(),
    max_value=data['Date'].max()
)

# Filter data based on selected date range
filtered_data = data[
    (data['Date'] >= pd.Timestamp(date_range[0])) &
    (data['Date'] <= pd.Timestamp(date_range[1]))
]

# Melt data for plotting
melted_data = filtered_data.melt(
    id_vars=['Curve Name', 'Date'],
    var_name='Maturity',
    value_name='Yield'
)

# Plot interactive graph
fig = px.line(
    melted_data,
    x='Date',
    y='Yield',
    color='Maturity',
    title='Bond Yield Curve (2000 - 2025)',
    labels={'Yield': 'Yield (%)', 'Date': 'Date', 'Maturity': 'Maturity'}
)

st.plotly_chart(fig, use_container_width=True)

