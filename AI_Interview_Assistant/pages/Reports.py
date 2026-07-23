# pages/Reports.py
"""
Reports & Recommendations Page.
Generates downloadable PDF performance reviews containing resume details,
ATS scores, interview evaluations, and personalized training resources.
"""

import os
import streamlit as st
from utils.authentication import init_session
from utils.recommendation_engine import RecommendationEngine
from utils.report_generator import ReportGenerator
from database.queries import (
    get_latest_resume, get_interview_history, 
    get_answers_by_session, get_user_by_id, save_report
)

init_session()

# Check Authentication
if not st.session_state.logged_in:
    st.warning("⚠️ Please **Login** or **Register** first to access reports and recommendations.")
    st.stop()

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"Error loading CSS: {e}")

load_css()

# Create directories if missing
os.makedirs("reports", exist_ok=True)

st.markdown("<h1 class='gradient-header'>Reports & Training Recommendations</h1>", unsafe_allow_html=True)
st.write("Generate downloadable PDF reports summarizing your resume stats, ATS alignment, interview performance, and skill gap courses.")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

history = get_interview_history(st.session_state.user_id)
resume = get_latest_resume(st.session_state.user_id)

if not history:
    st.info("💡 You do not have any finished interview records. Please complete a practice session on the **Interview** page first to generate reports.")
    st.stop()

# Build dropdown selection for session reports
session_options = {}
for session in history:
    date_str = session["created_at"][:16]
    label = f"Session ({date_str}) - Score: {session['overall_score']:.1f}% [ID: {session['session_id'][:8]}...]"
    session_options[label] = session
    
selected_label = st.selectbox("Select interview session to compile report:", list(session_options.keys()))
selected_session = session_options[selected_label]
session_id = selected_session["session_id"]

if session_id:
    # 1. Fetch all detailed answers and questions
    answers = get_answers_by_session(session_id)
    
    # 2. Extract missing skills/concepts from evaluations to run recommendation engine
    missing_items = []
    for ans in answers:
        if ans.get("missing_concepts"):
            # Split comma separated concepts
            items = [item.strip() for item in ans["missing_concepts"].split(",") if item.strip()]
            missing_items.extend(items)
            
    # Also grab missing keywords from session state ATS result if matching this session
    if "ats_result" in st.session_state and st.session_state.ats_result:
        ats = st.session_state.ats_result
        missing_items.extend(ats["matching"]["missing_skills"])
        
    # Remove duplicates and clean
    missing_items = list(set(missing_items))
    
    # 3. Generate Recommendations
    engine = RecommendationEngine()
    recs = engine.get_recommendations(missing_items)
    
    # 4. Display recommendations directly on UI
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🎓 Recommended Training Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='accent-card'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Target Roles")
        st.write(recs["career_paths"] or "Software Engineer / Web Developer")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 📚 Suggested Online Courses")
        for course in recs["courses"]:
            st.write(f"🔹 **{course['title']}** - *{course['platform']}*")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🏆 Target Certifications")
        for cert in recs["certifications"]:
            st.write(f"🔸 **{cert}**")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 5. Generate and Compile PDF Report
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📄 Compile PDF Report")
    
    pdf_filename = f"reports/Report_{session_id}.pdf"
    
    if st.button("Build PDF Report"):
        with st.spinner("Compiling database records into PDF structure..."):
            user_info = dict(get_user_by_id(st.session_state.user_id))
            
            # Formulate ATS details if available in session
            ats_info = None
            if "ats_result" in st.session_state:
                ats_info = st.session_state.ats_result
                
            ReportGenerator.generate_pdf(
                user_info=user_info,
                resume_info=resume,
                ats_info=ats_info,
                interview_answers=answers,
                recommendations=recs,
                output_path=pdf_filename
            )
            
            # Save report to DB reports tracking
            save_report(st.session_state.user_id, session_id, pdf_filename)
            
            st.success("🎉 PDF Report compiled successfully! Click the button below to download.")
            
    # Show download button if file exists
    if os.path.exists(pdf_filename):
        try:
            with open(pdf_filename, "rb") as f:
                st.download_button(
                    label="📥 Download Performance Report (PDF)",
                    data=f.read(),
                    file_name=f"Interview_Prep_Report_{session_id[:8]}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error accessing generated PDF file: {e}")
