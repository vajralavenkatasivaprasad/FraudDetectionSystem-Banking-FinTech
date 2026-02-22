import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

st.set_page_config(page_title="Login - Fraud Detection System", layout="centered")

# Custom CSS for login page
st.markdown("""
<style>
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 30px;
        border-radius: 10px;
        background-color: #f0f2f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-title {
        text-align: center;
        color: #1f77b4;
        font-size: 32px;
        margin-bottom: 30px;
    }
    .login-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<div class="login-title">🏦 Fraud Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="login-subtitle">Banking & FinTech Security</div>', unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Demo users (in production, use a database)
VALID_USERS = {
    "admin": "admin123",
    "user1": "password123",
    "analyst": "analyst456",
    "manager": "manager789"
}

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Login")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("🔓 Login", use_container_width=True):
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_time = datetime.now()
            st.success(f"✅ Welcome, {username}!")
            st.balloons()
            st.switch_page("pages/home.py")
        else:
            st.error("❌ Invalid username or password")

with col2:
    st.markdown("### Demo Credentials")
    st.info("""
    **Admin Account:**
    - Username: `admin`
    - Password: `admin123`
    
    **User Account:**
    - Username: `user1`
    - Password: `password123`
    
    **Analyst Account:**
    - Username: `analyst`
    - Password: `analyst456`
    """)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center style='color: #999;'>© 2026 Fraud Detection System. All rights reserved.</center>", unsafe_allow_html=True)
