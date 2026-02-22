import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")

st.set_page_config(page_title="Home - Fraud Detection", layout="wide")

# Sidebar for navigation
st.sidebar.title(f"👤 {st.session_state.username.upper()}")
st.sidebar.divider()

with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio(
        "Select Page:",
        ["🏠 Home", "📊 Dashboard", "💳 Transactions", "🔍 Fraud Analysis", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("login.py")

# Main content
st.markdown("""
<style>
    .welcome-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stat-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Welcome Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"""
    <div class="welcome-header">
        <h1>Welcome back, {st.session_state.username}! 👋</h1>
        <p>Real-time Fraud Detection & Risk Management System</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.info(f"📅 {datetime.now().strftime('%B %d, %Y')}")

# Key Metrics
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        "127,543",
        "+12.5%",
        delta_color="normal"
    )

with col2:
    st.metric(
        "Fraud Cases Detected",
        "1,243",
        "+8.3%",
        delta_color="off"
    )

with col3:
    st.metric(
        "Detection Accuracy",
        "98.7%",
        "+0.2%",
        delta_color="normal"
    )

with col4:
    st.metric(
        "Avg Processing Time",
        "2.3ms",
        "-0.5ms",
        delta_color="normal"
    )

st.divider()

# System Overview
st.subheader("📊 System Overview")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Quick Stats")
    stats_data = {
        "Legitimate Transactions": 126300,
        "Fraudulent Transactions": 1243,
        "Pending Review": 45,
        "Resolved Cases": 1198
    }
    
    for stat, value in stats_data.items():
        st.markdown(f"**{stat}:** {value:,}")

with col2:
    st.markdown("### System Status")
    status_info = {
        "🟢 API Status": "Operational",
        "🟢 ML Model": "Active",
        "🟢 Data Pipeline": "Running",
        "🟢 Database": "Connected"
    }
    
    for status, info in status_info.items():
        st.markdown(f"{status} - **{info}**")

st.divider()

# Recent Alerts
st.subheader("⚠️ Recent Fraud Alerts")

recent_alerts = pd.DataFrame({
    "Timestamp": pd.date_range(start="2026-02-22", periods=5, freq="H"),
    "Transaction ID": ["TXN-" + str(i) for i in range(10001, 10006)],
    "Amount": ["$2,450", "$1,890", "$5,320", "$890", "$3,210"],
    "Status": ["Blocked", "Review", "Blocked", "Approved", "Blocked"],
    "Confidence": ["98.5%", "75.3%", "96.2%", "5.2%", "99.1%"]
})

st.dataframe(recent_alerts, use_container_width=True, hide_index=True)

st.divider()

# Features Section
st.subheader("✨ Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔐 Real-Time Detection
    - Instant fraud identification
    - ML-powered predictions
    - 24/7 monitoring
    """)

with col2:
    st.markdown("""
    ### 📊 Analytics Dashboard
    - Transaction insights
    - Risk metrics
    - Historical trends
    """)

with col3:
    st.markdown("""
    ### 🛡️ Risk Management
    - Automated alerts
    - Case management
    - Compliance reports
    """)