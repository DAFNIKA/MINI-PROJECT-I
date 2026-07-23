# pages/Profile.py
"""
User Profile & Interview History Viewer Page.
Enables review of previous session transcript logs, questions, answers, and evaluations.
"""

import os
import streamlit as st
from utils.authentication import init_session
from database.queries import (
    get_user_by_id, get_latest_resume, 
    get_interview_history, get_answers_by_session
)

init_session()

# Check Authentication
if not st.session_state.logged_in:
    st.warning("⚠️ Please **Login** or **Register** first to access Profile settings and interview logs.")
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

st.markdown("<h1 class='gradient-header'>User Profile & History Review</h1>", unsafe_allow_html=True)
st.write("Review user account configurations, verify credentials, and examine detailed logs of past mock interviews.")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Fetch user metadata
user = get_user_by_id(st.session_state.user_id)
resume = get_latest_resume(st.session_state.user_id)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 👤 User Information")
    st.write(f"**Full Name:** {user['full_name'] or 'N/A'}")
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Member Since:** {user['created_at'][:10]}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Resume Details")
    if resume:
        st.write(f"**Active Resume File:** `{resume['filename']}`")
        st.write(f"**Last Upload Time:** {resume['uploaded_at'][:16]}")
        
        # Count extracted skills
        skills_data = resume["parsed_details"].get("skills", {})
        total_skills = sum(len(items) for items in skills_data.values())
        st.write(f"**Extracted Skills Count:** {total_skills}")
    else:
        st.info("No resume uploaded yet. Visit the **Resume Analysis** page to parse your resume.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# --- INTERVIEW HISTORY DETAILS ---
st.markdown("### 📜 Detailed Interview History Review")

history = get_interview_history(st.session_state.user_id)

if not history:
    st.info("💡 You do not have any saved interview records. Start practicing in the **Interview** section.")
else:
    # Build dropdown selections for historical sessions
    session_options = {}
    for session in history:
        date_str = session["created_at"][:16]
        label = f"Session ({date_str}) - Score: {session['overall_score']:.1f}% [ID: {session['session_id'][:8]}...]"
        session_options[label] = session["session_id"]
        
    selected_label = st.selectbox("Select a previous session to inspect:", list(session_options.keys()))
    selected_session_id = session_options[selected_label]
    
    if selected_session_id:
        st.write("")
        st.markdown(f"#### Transcripts for session: `{selected_session_id}`")
        
        # Load answers from DB
        answers = get_answers_by_session(selected_session_id)
        
        if not answers:
            st.warning("No answer transcripts were found for this session.")
        else:
            for i, ans in enumerate(answers):
                # Accordion container for each question
                with st.expander(f"Question {i+1}: {ans['question_text'][:80]}... - Match: {ans['similarity_score']:.1f}%"):
                    st.markdown(f"**Full Question:** {ans['question_text']}")
                    st.markdown(f"**Your Answer:** \n> {ans['answer_text']}")
                    st.markdown(f"**Ideal Answer Reference:** \n* {ans['ideal_answer']}")
                    
                    # Display sub-scores in metrics layout
                    sc1, sc2, sc3, sc4 = st.columns(4)
                    with sc1:
                        st.metric("Semantic Fit", f"{ans['similarity_score']:.1f}%")
                    with sc2:
                        st.metric("Grammar Integrity", f"{ans['grammar_score']:.1f}%" if ans['grammar_score'] is not None else "N/A")
                    with sc3:
                        st.metric("Communication Clarity", f"{ans['communication_score']:.1f}%" if ans['communication_score'] is not None else "N/A")
                    with sc4:
                        st.metric("Confidence Indicator", f"{ans['confidence_score']:.1f}%" if ans['confidence_score'] is not None else "N/A")
                        
                    # Feedback box
                    st.markdown("<div class='accent-card' style='margin-top: 10px;'>", unsafe_allow_html=True)
                    st.markdown("**🤖 AI Feedback & Recommendations:**")
                    st.write(ans["feedback"])
                    if ans["missing_concepts"]:
                        st.write(f"*Missing concepts or key terms:* **{ans['missing_concepts']}**")
                    st.markdown("</div>", unsafe_allow_html=True)
