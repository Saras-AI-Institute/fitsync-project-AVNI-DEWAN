import streamlit as st
import pandas as pd
from modules.processor import process_data

# Title
st.title("FitSync - Personal Health Analytics")

# Sidebar filter
st.sidebar.header("Filters")

time_range = st.sidebar.selectbox(
    "Select time range",
    options=["last 7 days", "last 30 days", "all time"],
    index=2
)

# Load data
df = process_data()

# Filter by Date
if 'Date' in df.columns:
    if time_range == "last 7 days":
        df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=7))]
    elif time_range == "last 30 days":
        df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=30))]

# Metrics
average_steps = df['Steps'].mean()
average_sleep_hours = df['Sleep_hours'].mean()
average_recovery_score = df['Recovery_Score'].mean()

# Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Steps", f"{average_steps:.0f}")

with col2:
    st.metric("Average Sleep Hours", f"{average_sleep_hours:.1f}")

with col3:
    st.metric("Average Recovery Score", f"{average_recovery_score:.1f}")

# Table
st.write("## Processed Health Data")
st.dataframe(df)