import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Trends & Insights")

# ✅ Sidebar
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"]
)

# ✅ Data
data = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=90),
    "Recovery Score": np.random.randint(40, 80, 90),
    "Sleep Hours": np.random.uniform(6, 8, 90).round(1),
    "Steps": np.random.randint(6000, 15000, 90)
})

# ✅ Filter
today = pd.Timestamp.today()

if time_range == "Last 7 Days":
    filtered_df = data[data["Date"] >= today - pd.Timedelta(days=7)].copy()
elif time_range == "Last 30 Days":
    filtered_df = data[data["Date"] >= today - pd.Timedelta(days=30)].copy()
else:
    filtered_df = data.copy()

# ✅ Sort (important for line charts)
filtered_df = filtered_df.sort_values("Date")

# =========================
# 📊 Summary
# =========================
st.subheader("Summary Statistics")
summary_stats = filtered_df[["Recovery Score", "Sleep Hours", "Steps"]].describe()
st.dataframe(summary_stats)

# =========================
# 📊 Distribution Section
# =========================
st.subheader("Distribution of Health Metrics")

col1, col2 = st.columns(2)

# 📊 Steps Distribution
with col1:
    fig_steps = px.histogram(
        filtered_df,
        x="Steps",
        nbins=15,
        title="Distribution of Steps"
    )
    st.plotly_chart(fig_steps, use_container_width=True)

# 📊 Calories (simulated)
filtered_df["Calories Burned"] = (filtered_df["Steps"] * 0.04).astype(int)

with col2:
    fig_cal = px.histogram(
        filtered_df,
        x="Calories Burned",
        nbins=15,
        title="Distribution of Calories Burned"
    )
    st.plotly_chart(fig_cal, use_container_width=True)

# =========================
# 📈 Sleep Hours Trend
# =========================
st.subheader("Sleep Hours Trend")

fig_sleep = px.line(
    filtered_df,
    x="Date",
    y="Sleep Hours",
    title="Sleep Hours Over Time",
    markers=True
)

st.plotly_chart(fig_sleep, use_container_width=True)

# =========================
# 📊 Monthly Recovery Score
# =========================
st.subheader("Average Recovery Score by Month")

# ✅ Fix for JSON serialization error
filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").astype(str)

monthly_avg = (
    filtered_df.groupby("Month")["Recovery Score"]
    .mean()
    .reset_index()
)

fig_month = px.bar(
    monthly_avg,
    x="Month",
    y="Recovery Score",
    title="Average Recovery Score per Month",
    text_auto=True
)

st.plotly_chart(fig_month, use_container_width=True)