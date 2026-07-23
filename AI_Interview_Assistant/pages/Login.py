# pages/Login.py
"""
User Login Page.
Authenticates existing users and initializes their session.
"""

import os
import streamlit as st
from utils.authentication import authenticate, login_user, init_session

init_session()

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"Error loading CSS: {e}")

load_css()

st.markdown("<h1 class='gradient-header'>Sign In to Your Account</h1>", unsafe_allow_html=True)
st.write("Access your dashboard, resume analysis details, and begin mock interviews.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

if st.session_state.logged_in:
    st.info(f"You are currently logged in as: **{st.session_state.username}**")
    if st.button("Logout"):
        from utils.authentication import logout_user
        logout_user()
    st.stop()

# Login Form Container
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Sign In")
        
    st.markdown("</div>", unsafe_allow_html=True)

if submit_button:
    if not username or not password:
        st.error("⚠️ Please fill in both fields.")
    else:
        user = authenticate(username.strip(), password)
        if user:
            login_user(user)
            st.success("🎉 Login successful! Welcome back.")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")
