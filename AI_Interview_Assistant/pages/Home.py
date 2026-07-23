# pages/Home.py
"""
Home Dashboard Quick Navigation Page.
Serves as an introductory user manual and quick guide for the system.
"""

import os
import streamlit as st
from utils.authentication import init_session

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

st.markdown("<h1 class='gradient-header'>Overview & Guide</h1>", unsafe_allow_html=True)
st.write("Welcome to your personal preparation companion. Follow this step-by-step roadmap to maximize your performance.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Guidelines or Roadmap
st.markdown(
    """
    <div class='glass-card'>
        <h3>🚀 Step-by-Step Preparation Roadmap</h3>
        <ol>
            <li><b>1. Analyze Resume:</b> Go to the <b>Resume Analysis</b> page. Upload your resume (PDF/DOCX) and view the extracted skills, education, and experience.</li>
            <li><b>2. Compute ATS Score:</b> Paste a Target Job Description on the same page. Compare your resume skills and keywords to calculate your ATS compatibility match.</li>
            <li><b>3. Start a Mock Session:</b> Head to the <b>Interview</b> page. Select your interview domain, difficulty, and quantity of questions to start a simulated verbal-to-text interview.</li>
            <li><b>4. Review Dashboard:</b> Review your progress over time in the <b>Dashboard</b> page. Leverage Plotly charts to target your weaker skill clusters.</li>
            <li><b>5. Export Summary Report:</b> Navigate to the <b>Reports</b> page. Compile all session metrics, answers, and improvement courses into a professional PDF report.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='accent-card'>
        <h3>💡 Top Preparation Tip</h3>
        <p>Ensure that your resume text contains standard industry keywords. The ATS Scorer matches nouns and entities from job descriptions to detect skills. If you are missing skills, check out the recommendations engine in the reports page!</p>
    </div>
    """,
    unsafe_allow_html=True
)
