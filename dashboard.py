import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")

st.set_page_config(page_title="Dashboard - Fraud Detection", layout="wide")

st.title("📊 Advanced Analytics Dashboard")

# Sidebar Navigation
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.username.upper()}")
    page = st.radio(
        "Navigate:",
        ["🏠 Home", "📊 Dashboard", "💳 Transactions", "🔍 Fraud Analysis", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    # Date range filter
    st.markdown("### Filters")
    date_range = st.select_slider(
        "Select date range (days)",
        options=list(range(1, 31)),
        value=(7, 30)
    )
    
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("login.py")

# Generate sample data
np.random.seed(42)
dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq="D")
fraud_counts = np.random.randint(20, 100, 30)
legit_counts = np.random.randint(2000, 5000, 30)
transaction_amounts = np.random.uniform(100, 10000, 30)

df_daily = pd.DataFrame({
    "Date": dates,
    "Fraudulent": fraud_counts,
    "Legitimate": legit_counts,
    "Avg Amount": transaction_amounts
})

# KPI Section
col1, col2, col3, col4 = st.columns(4)

total_transactions = df_daily["Fraudulent"].sum() + df_daily["Legitimate"].sum()
fraud_rate = (df_daily["Fraudulent"].sum() / total_transactions * 100)

with col1:
    st.metric("Total Transactions", f"{total_transactions:,}", "+2.3%")
with col2:
    st.metric("Fraud Rate", f"{fraud_rate:.2f}%", "-0.5%", delta_color="inverse")
with col3:
    st.metric("Avg Confidence", "96.8%", "+1.2%")
with col4:
    st.metric("Cases Resolved", "98.5%", "+0.3%")

st.divider()

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Fraud vs Legitimate Transactions")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_daily["Date"], y=df_daily["Legitimate"], 
                             mode='lines+markers', name='Legitimate', 
                             line=dict(color='#2ecc71', width=3)))
    fig.add_trace(go.Scatter(x=df_daily["Date"], y=df_daily["Fraudulent"], 
                             mode='lines+markers', name='Fraudulent', 
                             line=dict(color='#e74c3c', width=3)))
    fig.update_layout(hovermode='x unified', height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Transaction Distribution")
    fig = px.pie(values=[85.2, 12.1, 2.7], 
                 names=["Legitimate", "Suspicious", "Fraudulent"],
                 color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c'])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Average Transaction Amount Trend")
    fig = px.area(df_daily, x="Date", y="Avg Amount", 
                  color_discrete_sequence=['#3498db'])
    fig.update_layout(hovermode='x', height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⏰ Transactions by Hour")
    hourly_data = pd.DataFrame({
        "Hour": [f"{i:02d}:00" for i in range(24)],
        "Count": np.random.randint(100, 500, 24)
    })
    fig = px.bar(hourly_data, x="Hour", y="Count", 
                 color_discrete_sequence=['#9b59b6'])
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Fraud Severity Distribution
st.subheader("🔴 Fraud Severity Analysis")
severity_data = pd.DataFrame({
    "Severity": ["Critical", "High", "Medium", "Low"],
    "Count": [45, 120, 310, 768],
    "Amount": ["$125,400", "$98,600", "$45,230", "$12,540"]
})

col1, col2 = st.columns([2, 1])
with col1:
    fig = px.bar(severity_data, x="Severity", y="Count",
                 color="Severity",
                 color_discrete_map={"Critical": "#e74c3c", "High": "#e67e22", 
                                    "Medium": "#f39c12", "Low": "#f1c40f"})
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.dataframe(severity_data, use_container_width=True, hide_index=True)

st.divider()

# Top Countries/Regions
st.subheader("🌍 Fraud Distribution by Region")
region_data = pd.DataFrame({
    "Region": ["USA", "UK", "Canada", "Australia", "India", "Germany"],
    "Frauds": [380, 245, 123, 98, 156, 89],
    "Percentage": ["30.5%", "19.6%", "9.8%", "7.8%", "12.5%", "7.1%"]
})

fig = px.bar(region_data, x="Region", y="Frauds", 
             color_discrete_sequence=['#3498db'])
fig.update_layout(height=350, showlegend=False)

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.dataframe(region_data, use_container_width=True, hide_index=True)