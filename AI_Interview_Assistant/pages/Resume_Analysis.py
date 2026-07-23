# pages/Resume_Analysis.py
"""
Resume Analysis & ATS Scorer Page.
Allows users to upload resumes, extract structural details/skills,
and evaluate compatibility against job descriptions.
"""

import os
import streamlit as st
import plotly.graph_objects as go
from utils.authentication import init_session
from utils.resume_parser import ResumeParser
from utils.skill_extractor import SkillExtractor
from utils.jd_matcher import JDMatcher
from utils.ats_score import ATSScorer
from database.queries import save_resume, save_user_skills, save_job_description, get_latest_resume

init_session()

# Check Authentication
if not st.session_state.logged_in:
    st.warning("⚠️ Please **Login** or **Register** first to access the Resume Analysis dashboard.")
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

# Create directories if they don't exist
os.makedirs("resumes", exist_ok=True)

st.markdown("<h1 class='gradient-header'>Resume Analysis & ATS Compatibility</h1>", unsafe_allow_html=True)
st.write("Upload your resume, verify extracted metadata, and measure alignment with target job descriptions.")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Session state initialization for parsed resume
if "parsed_resume" not in st.session_state:
    # Try loading latest resume from database to restore session
    latest = get_latest_resume(st.session_state.user_id)
    if latest:
        st.session_state.parsed_resume = latest
    else:
        st.session_state.parsed_resume = None

# Tab layout
tab1, tab2 = st.tabs(["📄 Resume Parser", "🎯 ATS Match Score"])

# --- TAB 1: RESUME PARSER ---
with tab1:
    st.subheader("Upload and Parse Resume")
    
    uploaded_file = st.file_uploader("Choose a file (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        if st.button("Analyze Resume"):
            with st.spinner("Processing file with NLP extraction..."):
                # Save file to disk
                file_path = os.path.join("resumes", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract text based on file format
                raw_text = ""
                if uploaded_file.name.lower().endswith(".pdf"):
                    raw_text = ResumeParser.extract_text_from_pdf(file_path)
                elif uploaded_file.name.lower().endswith(".docx"):
                    raw_text = ResumeParser.extract_text_from_docx(file_path)
                
                if not raw_text.strip():
                    st.error("❌ Failed to extract readable text. The document might be empty or scanned.")
                else:
                    # Parse contents
                    contact = ResumeParser.extract_contact_info(raw_text)
                    education = ResumeParser.extract_education(raw_text)
                    experience = ResumeParser.extract_experience(raw_text)
                    
                    # Extract skills
                    extractor = SkillExtractor()
                    skills_dict = extractor.extract_skills(raw_text)
                    
                    # Flatten skills to list for DB storage
                    flat_skills = []
                    for cat_skills in skills_dict.values():
                        flat_skills.extend(cat_skills)
                    
                    # Save to DB
                    parsed_details = {
                        "contact": contact,
                        "skills": skills_dict
                    }
                    resume_id = save_resume(
                        user_id=st.session_state.user_id,
                        filename=uploaded_file.name,
                        raw_text=raw_text,
                        education=education,
                        experience=experience,
                        parsed_details=parsed_details
                    )
                    
                    # Save skills to skills table
                    save_user_skills(st.session_state.user_id, flat_skills, category="Technical")
                    
                    # Store in session state
                    st.session_state.parsed_resume = {
                        "filename": uploaded_file.name,
                        "raw_text": raw_text,
                        "education": education,
                        "experience": experience,
                        "parsed_details": parsed_details
                    }
                    st.success("🎉 Resume parsed and saved successfully!")
                    
    # Display parsed resume details if available
    if st.session_state.parsed_resume:
        res = st.session_state.parsed_resume
        details = res["parsed_details"]
        contact = details.get("contact", {})
        skills = details.get("skills", {})
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"### Current Parsed Resume: `{res['filename']}`")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### 👤 Contact Information")
            st.write(f"**Name:** {contact.get('name', 'N/A')}")
            st.write(f"**Email:** {contact.get('email', 'N/A')}")
            st.write(f"**Phone:** {contact.get('phone', 'N/A')}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### 🎓 Education")
            if res["education"]:
                for edu in res["education"]:
                    st.markdown(f"- {edu}")
            else:
                st.write("No explicit education records detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### 🧠 Extracted Technical Skills")
            
            has_skills = False
            for cat, items in skills.items():
                if items:
                    has_skills = True
                    st.write(f"**{cat}:**")
                    # Display as styled badges/tags
                    badges_html = " ".join([f"<span class='badge badge-easy' style='margin-right:5px; margin-bottom:5px;'>{item}</span>" for item in items])
                    st.markdown(badges_html, unsafe_allow_html=True)
                    st.write("")
            
            if not has_skills:
                st.write("No standard skills detected from taxonomy.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### 💼 Experience / Projects")
            if res["experience"]:
                for idx, exp in enumerate(res["experience"]):
                    st.markdown(f"**Record {idx+1}:**")
                    st.text(exp)
                    st.markdown("<div class='divider' style='margin:10px 0;'></div>", unsafe_allow_html=True)
            else:
                st.write("No explicit work history or projects detected.")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("💡 Please upload and analyze a resume to view parser summaries.")

# --- TAB 2: ATS MATCH SCORE ---
with tab2:
    st.subheader("ATS Compatibility Checker")
    
    if not st.session_state.parsed_resume:
        st.warning("⚠️ You must parse a resume in the first tab before calculating an ATS match score.")
    else:
        # Job Description Form
        with st.form("jd_form"):
            job_title = st.text_input("Target Job Title", placeholder="e.g. Senior Python Developer")
            jd_text = st.text_area("Job Description", placeholder="Paste the full job post details here...", height=200)
            submit_jd = st.form_submit_button("Calculate ATS Match Score")
            
        if submit_jd:
            if not job_title or not jd_text.strip():
                st.error("⚠️ Please specify both Job Title and Job Description.")
            else:
                with st.spinner("Analyzing Job Description compatibility..."):
                    # Save Job Description
                    save_job_description(st.session_state.user_id, job_title, jd_text)
                    
                    # Extract JD Skills
                    matcher = JDMatcher()
                    jd_skills = matcher.analyze_jd(jd_text)
                    
                    # Match
                    resume_skills = st.session_state.parsed_resume["parsed_details"].get("skills", {})
                    match_result = matcher.match_skills(resume_skills, jd_skills)
                    
                    # Score
                    res = st.session_state.parsed_resume
                    evaluation = ATSScorer.calculate_score(
                        resume_text=res["raw_text"],
                        jd_text=jd_text,
                        matched_skills=match_result["matched_skills"],
                        missing_skills=match_result["missing_skills"],
                        contact_info=res["parsed_details"].get("contact", {}),
                        education=res["education"],
                        experience=res["experience"]
                    )
                    
                    # Store match evaluation in session state to persist
                    st.session_state.ats_result = {
                        "job_title": job_title,
                        "score_metrics": evaluation,
                        "matching": match_result
                    }
                    st.success("🎉 ATS Matching completed successfully!")
                    
        # Render Results if available in session
        if "ats_result" in st.session_state:
            res_data = st.session_state.ats_result
            metrics = res_data["score_metrics"]
            matching = res_data["matching"]
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown(f"### Match Evaluation for position: **{res_data['job_title']}**")
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                # Gauge Chart for Overall Score
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = metrics["overall_score"],
                    title = {'text': "Overall ATS Compatibility", 'font': {'size': 18}},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#6366F1"},
                        'bgcolor': "rgba(255,255,255,0.05)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(255,255,255,0.2)",
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                            {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                            {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
                        ],
                    }
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white", 'family': "Outfit"},
                    margin=dict(l=20, r=20, t=50, b=20),
                    height=280
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Breakdown Sub-scores
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.write(f"**Text Relevance Similarity:** {metrics['text_similarity']}%")
                st.write(f"**Core Skill Coverage:** {metrics['skill_score']}%")
                st.write(f"**Structure Completeness:** {metrics['structure_score']}%")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='accent-card'>", unsafe_allow_html=True)
                st.markdown("#### 🌟 Improvement Recommendations")
                for sug in metrics["suggestions"]:
                    st.write(sug)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display Skill matches
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🤝 Skills Match Analytics")
                
                st.write("**Matched Keywords:**")
                if matching["matched_skills"]:
                    matched_html = " ".join([f"<span class='badge badge-easy' style='margin-right:5px; margin-bottom:5px;'>{item}</span>" for item in matching["matched_skills"]])
                    st.markdown(matched_html, unsafe_allow_html=True)
                else:
                    st.write("No matched keywords found.")
                    
                st.write("")
                st.write("**Missing Keywords from Job Description:**")
                if matching["missing_skills"]:
                    missing_html = " ".join([f"<span class='badge badge-hard' style='margin-right:5px; margin-bottom:5px;'>{item}</span>" for item in matching["missing_skills"]])
                    st.markdown(missing_html, unsafe_allow_html=True)
                else:
                    st.write("No missing keywords detected. Perfect match!")
                st.markdown("</div>", unsafe_allow_html=True)
