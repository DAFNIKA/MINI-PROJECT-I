# app.py
"""
AI-Powered Interview Preparation Assistant.
Main entry point for the Streamlit web application.
Manages database initialization, global session state, and general landing page UI.
"""

import os
import streamlit as st
from database.database import init_db
from utils.authentication import init_session, logout_user

# 1. Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="AI Interview Prep Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Initialization
# Runs on startup to verify tables exist
init_db()

# 3. Global Session Management
init_session()

# 4. Global CSS Stylesheet loading
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"Error loading CSS: {e}")

load_css()

# 5. Sidebar Navigation Header & Login Status
st.sidebar.markdown(
    """
    <div style='text-align: center;'>
        <h2>💼 AI Interview Prep</h2>
        <p style='color: #9CA3AF;'>Prepare with confidence</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as: **{st.session_state.username}**")
    st.sidebar.info(f"Welcome, {st.session_state.full_name or st.session_state.username}!")
    if st.sidebar.button("Log Out"):
        logout_user()
else:
    st.sidebar.warning("You are currently offline / guest user.")
    st.sidebar.info("Please navigate to **Login** or **Register** to access core features.")

# 6. Main Landing Page UI
st.markdown("<h1 class='gradient-header'>AI-Powered Interview Preparation Assistant</h1>", unsafe_allow_html=True)
st.subheader("Master your technical and HR interviews using Machine Learning and NLP.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Grid Layout for Features
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class='glass-card'>
            <h3>📊 Resume Parser & ATS Matching</h3>
            <p>Upload your PDF or Word resume. Our NLP pipeline extracts technical skills, education, and experiences. Compare your profile against job descriptions to calculate an ATS Score and get targeted feedback on missing keywords.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class='glass-card'>
            <h3>🤖 Sentence-Transformers Answer Evaluation</h3>
            <p>Answer AI-generated questions and receive immediate scoring. Our SBERT models calculate the semantic similarity between your answer and an ideal response, providing detailed feedback on missing technical concepts.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class='glass-card'>
            <h3>🧠 Smart Interview Simulator</h3>
            <p>Generate highly personalized Technical, HR, Behavioral, and Scenario questions based directly on your resume skills and difficulty preferences (Easy, Medium, Hard).</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class='glass-card'>
            <h3>📈 Analytics Dashboard & PDF Reports</h3>
            <p>Track your historical progress with visual analytics charts. Assess your skills gaps with Plotly visualizations and download comprehensive PDF performance reports to share with mentors.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Quick Access Call To Action
if not st.session_state.logged_in:
    st.info("💡 To get started, go to **Register** or **Login** pages in the sidebar to build your profile.")
else:
    st.success("✅ You are logged in! Navigate to **Resume Analysis** or **Interview** pages in the sidebar to start preparing.")
