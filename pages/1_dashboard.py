import streamlit as st
import pandas as pd
import numpy as np

# ✅ Wide layout
st.set_page_config(layout="wide")

# ✅ Sidebar
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"]
)

# Title
st.title("FitSync - Personal Health Analytics")

# ✅ Generate MORE data (90 days instead of 30)
data = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=90),
    "Recovery Score": np.random.randint(40, 80, 90),
    "Sleep Hours": np.random.uniform(6, 8, 90).round(1),
    "Steps": np.random.randint(6000, 12000, 90)
})

# ✅ Filter logic (WORKING PROPERLY)
today = pd.Timestamp.today()

if time_range == "Last 7 Days":
    filtered_data = data[data["Date"] >= today - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    filtered_data = data[data["Date"] >= today - pd.Timedelta(days=30)]
else:
    filtered_data = data

# ✅ Sort data (important for line chart)
filtered_data = filtered_data.sort_values("Date")

# ✅ Top metrics (dynamic)
col1, col2, col3 = st.columns(3)

col1.metric("Average Steps", int(filtered_data["Steps"].mean()))
col2.metric("Average Sleep Hours", round(filtered_data["Sleep Hours"].mean(), 1))
col3.metric("Average Recovery Score", round(filtered_data["Recovery Score"].mean(), 1))

# ✅ Charts layout
col1, col2 = st.columns(2)

# 📈 Line chart
with col1:
    st.subheader("Recovery Score & Sleep Trend")
    st.line_chart(
        filtered_data.set_index("Date")[["Recovery Score", "Sleep Hours"]],
        use_container_width=True
    )

# 📊 Scatter chart (clean & safe)
with col2:
    st.subheader("Recovery Score vs Daily Steps")
    st.scatter_chart(
        data=filtered_data,
        x="Steps",
        y="Recovery Score",
        use_container_width=True
    )