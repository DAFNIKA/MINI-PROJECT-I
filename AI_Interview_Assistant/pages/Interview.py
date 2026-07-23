# pages/Interview.py
"""
Mock Interview Simulator Page.
Facilitates dynamic technical, HR, and behavioral interview sessions.
Features real-time SBERT semantic evaluation of responses.
"""

import os
import uuid
import streamlit as st
from utils.authentication import init_session
from utils.ai_evaluator import AIEvaluator
from database.queries import (
    get_latest_resume, get_seeded_questions_by_skills, 
    save_candidate_answer, save_interview_result
)

init_session()

# Check Authentication
if not st.session_state.logged_in:
    st.warning("⚠️ Please **Login** or **Register** first to access the Mock Interview simulator.")
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

# Check if resume is parsed, needed for skill-based question generation
latest_resume = get_latest_resume(st.session_state.user_id)

st.markdown("<h1 class='gradient-header'>AI Mock Interview Simulator</h1>", unsafe_allow_html=True)
st.write("Test your knowledge. Select a difficulty, enter your response, and receive instant AI feedback.")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# State Machine variables initialization
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "current_q_evaluated" not in st.session_state:
    st.session_state.current_q_evaluated = False
if "current_evaluation" not in st.session_state:
    st.session_state.current_evaluation = None
if "session_scores" not in st.session_state:
    st.session_state.session_scores = []

# --- CONFIGURATION INTERFACE ---
if not st.session_state.interview_active:
    st.subheader("Configure Interview Session")
    
    if not latest_resume:
        st.info("💡 Seeding default general questions. To receive hyper-personalized technical questions matching your specific profile, upload your resume in the **Resume Analysis** page first.")
        
    with st.form("interview_config"):
        difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
        
        start_btn = st.form_submit_button("Launch Mock Interview")
        
    if start_btn:
        with st.spinner("Compiling questions..."):
            # Gather user skills if resume exists
            user_skills = []
            if latest_resume:
                skills_data = latest_resume["parsed_details"].get("skills", {})
                for items in skills_data.values():
                    user_skills.extend(items)
            
            # Fetch questions matching profile
            fetched_qs = get_seeded_questions_by_skills(
                skills=user_skills,
                difficulty=difficulty,
                limit=num_questions
            )
            
            if not fetched_qs:
                st.error("❌ Failed to load questions. Please check database connectivity.")
            else:
                # Set up active interview session
                st.session_state.questions = fetched_qs
                st.session_state.current_q_idx = 0
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.interview_active = True
                st.session_state.current_q_evaluated = False
                st.session_state.current_evaluation = None
                st.session_state.session_scores = []
                st.rerun()

# --- ACTIVE INTERVIEW INTERFACE ---
else:
    q_list = st.session_state.questions
    idx = st.session_state.current_q_idx
    total_q = len(q_list)
    
    st.markdown(f"### 📝 Question {idx + 1} of {total_q}")
    st.progress((idx) / total_q)
    
    current_q = q_list[idx]
    
    # Question Card Display
    st.markdown(
        f"""
        <div class='glass-card'>
            <span class='badge badge-medium' style='margin-bottom: 10px;'>{current_q['category']}</span>
            <span class='badge badge-hard' style='margin-bottom: 10px; margin-left: 5px;'>{current_q['difficulty']}</span>
            <h4>{current_q['question_text']}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Answer text area
    user_answer = st.text_area("Your Answer:", placeholder="Type your response here...", height=150, key=f"ans_input_{idx}")
    
    # Buttons for submission
    col1, col2 = st.columns([1, 4])
    
    # Action buttons based on evaluation state
    if not st.session_state.current_q_evaluated:
        with col1:
            submit_answer = st.button("Submit Answer")
            
        if submit_answer:
            if not user_answer.strip():
                st.error("⚠️ Please type an answer before submitting.")
            else:
                with st.spinner("AI evaluating answer semantic relevance..."):
                    evaluator = AIEvaluator()
                    evaluation = evaluator.evaluate_answer(
                        user_answer=user_answer,
                        ideal_answer=current_q["ideal_answer"]
                    )
                    
                    # Save individual answer to DB
                    save_candidate_answer(
                        question_id=current_q["id"],
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        answer_text=user_answer,
                        similarity_score=evaluation["similarity_score"],
                        feedback=evaluation["feedback"],
                        missing_concepts=", ".join(evaluation["missing_concepts"]),
                        grammar_score=evaluation["grammar_score"],
                        communication_score=evaluation["communication_score"],
                        confidence_score=evaluation["confidence_score"]
                    )
                    
                    st.session_state.session_scores.append(evaluation["similarity_score"])
                    st.session_state.current_evaluation = evaluation
                    st.session_state.current_q_evaluated = True
                    st.rerun()
    else:
        # Display evaluation metrics
        evaluation = st.session_state.current_evaluation
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### AI Evaluation Result")
        
        ec1, ec2, ec3, ec4 = st.columns(4)
        with ec1:
            st.metric("Semantic Match", f"{evaluation['similarity_score']}%")
        with ec2:
            st.metric("Grammar", f"{evaluation['grammar_score']}%")
        with ec3:
            st.metric("Communication", f"{evaluation['communication_score']}%")
        with ec4:
            st.metric("Confidence", f"{evaluation['confidence_score']}%")
            
        st.markdown("<div class='accent-card'>", unsafe_allow_html=True)
        st.markdown("#### 🤖 Feedback")
        st.write(evaluation["feedback"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.info(f"💡 **Ideal Concept Tip:** {current_q['ideal_answer']}")
        
        # Next / Finish Button
        with col1:
            if idx + 1 < total_q:
                next_btn = st.button("Next Question")
                if next_btn:
                    st.session_state.current_q_idx += 1
                    st.session_state.current_q_evaluated = False
                    st.session_state.current_evaluation = None
                    st.rerun()
            else:
                finish_btn = st.button("Finish Interview")
                if finish_btn:
                    # Calculate overall session score
                    overall_score = sum(st.session_state.session_scores) / len(st.session_state.session_scores)
                    
                    # Compute skill breakdowns if needed, let's keep it simple and record
                    save_interview_result(
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        overall_score=overall_score,
                        skills_score={"Global": overall_score}
                    )
                    
                    # Store session outcome summary
                    st.session_state.last_session_summary = {
                        "session_id": st.session_state.session_id,
                        "overall_score": round(overall_score, 1)
                    }
                    
                    # Clear interview state
                    st.session_state.interview_active = False
                    st.session_state.questions = []
                    st.session_state.current_q_idx = 0
                    st.session_state.session_id = None
                    st.session_state.current_q_evaluated = False
                    st.session_state.current_evaluation = None
                    st.session_state.session_scores = []
                    
                    st.success("🎉 You have completed the mock interview session!")
                    st.rerun()

# --- POST INTERVIEW SUMMARY ---
if "last_session_summary" in st.session_state and not st.session_state.interview_active:
    summary = st.session_state.last_session_summary
    st.markdown("<div class='accent-card'>", unsafe_allow_html=True)
    st.markdown("### 🏆 Interview Session Complete!")
    st.write(f"Your overall semantic match accuracy: **{summary['overall_score']}%**")
    st.write("All scores have been recorded. You can inspect comprehensive skill charts on the Dashboard or download a full interview summary PDF in the Reports page.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Dashboard"):
            st.switch_page("pages/Dashboard.py")
    with col2:
        if st.button("Generate Reports"):
            st.switch_page("pages/Reports.py")
            
    # Clear summary once read/navigated
    if st.button("Start New Practice"):
        del st.session_state.last_session_summary
        st.rerun()
