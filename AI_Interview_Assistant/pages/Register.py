# pages/Register.py
"""
User Registration Page.
Enables new users to create accounts. Passwords are securely hashed.
"""

import os
import streamlit as st
from utils.authentication import register, init_session

# Load session variables
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

st.markdown("<h1 class='gradient-header'>Create your Account</h1>", unsafe_allow_html=True)
st.write("Join the AI-Powered Interview Preparation Assistant to start your practice sessions.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

if st.session_state.logged_in:
    st.info(f"You are currently logged in as {st.session_state.username}.")
    st.stop()

# Registration Form Card
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    with st.form("registration_form"):
        full_name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email Address", placeholder="johndoe@example.com")
        username = st.text_input("Choose Username", placeholder="johndoe123")
        password = st.text_input("Password", type="password", placeholder="Enter a secure password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")
        
        submit_button = st.form_submit_button("Register Account")
        
    st.markdown("</div>", unsafe_allow_html=True)

if submit_button:
    # Basic Validations
    if not username or not password or not email or not full_name:
        st.error("⚠️ All fields are required.")
    elif password != confirm_password:
        st.error("⚠️ Passwords do not match.")
    elif len(password) < 6:
        st.error("⚠️ Password must be at least 6 characters long.")
    elif "@" not in email or "." not in email:
        st.error("⚠️ Please enter a valid email address.")
    else:
        success, msg = register(username.strip(), password, email.strip(), full_name.strip())
        if success:
            st.success("🎉 Account created successfully! Please navigate to the **Login** page to sign in.")
        else:
            st.error(f"❌ Registration failed: {msg}")
