# pages/Dashboard.py
"""
Performance Dashboard Page.
Visualizes candidate interview results, score progression,
and domain competency breakdowns using Plotly.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.authentication import init_session
from database.queries import get_interview_history

init_session()

# Check Authentication
if not st.session_state.logged_in:
    st.warning("⚠️ Please **Login** or **Register** first to access the Performance Dashboard.")
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

st.markdown("<h1 class='gradient-header'>Performance Analytics Dashboard</h1>", unsafe_allow_html=True)
st.write("Track your practice progression, review score summaries, and isolate knowledge gaps.")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Fetch History
history = get_interview_history(st.session_state.user_id)

if not history:
    st.info("💡 You have not completed any mock interviews yet. Launch an interview session on the **Interview** page to generate analytics.")
    st.stop()

# Convert history to DataFrame
df = pd.DataFrame(history)
# Formats timestamp to readable date
df["date"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")

# --- METRIC CARDS ---
total_sessions = len(df)
avg_score = df["overall_score"].mean()
best_score = df["overall_score"].max()
latest_score = df.iloc[0]["overall_score"]

m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.markdown(
        f"""
        <div class='glass-card' style='text-align: center;'>
            <span class='metric-label'>Interviews Completed</span>
            <div class='metric-value'>{total_sessions}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with m_col2:
    st.markdown(
        f"""
        <div class='glass-card' style='text-align: center;'>
            <span class='metric-label'>Average Score</span>
            <div class='metric-value'>{avg_score:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with m_col3:
    st.markdown(
        f"""
        <div class='glass-card' style='text-align: center;'>
            <span class='metric-label'>Personal Best</span>
            <div class='metric-value'>{best_score:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with m_col4:
    st.markdown(
        f"""
        <div class='glass-card' style='text-align: center;'>
            <span class='metric-label'>Latest Score</span>
            <div class='metric-value'>{latest_score:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# --- VISUALIZATION CHARTS ---
col1, col2 = st.columns(2)

with col1:
    # 1. Progress Over Time Line Chart
    st.markdown("### 📈 Preparation Progress Graph")
    df_chronological = df.iloc[::-1] # Reverse to display oldest first
    
    fig_line = px.line(
        df_chronological, 
        x="date", 
        y="overall_score",
        markers=True,
        labels={"date": "Date & Time", "overall_score": "Score (%)"},
        color_discrete_sequence=["#6366F1"]
    )
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Outfit"},
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
        margin=dict(l=20, r=20, t=20, b=20),
        height=320
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    # 2. Performance Distribution Bracket
    st.markdown("### 📊 Scoring Bracket Distribution")
    
    # Bucket scores
    def get_bracket(score):
        if score >= 80: return "Excellent (>=80%)"
        elif score >= 60: return "Good (60-79%)"
        elif score >= 40: return "Average (40-59%)"
        else: return "Needs Improvement (<40%)"
        
    df["bracket"] = df["overall_score"].apply(get_bracket)
    bracket_counts = df["bracket"].value_counts().reset_index()
    bracket_counts.columns = ["Bracket", "Count"]
    
    fig_pie = px.pie(
        bracket_counts, 
        values="Count", 
        names="Bracket",
        color_discrete_sequence=["#10B981", "#6366F1", "#F59E0B", "#EF4444"],
        hole=0.4
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Outfit"},
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=20, b=20),
        height=320
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# 3. Bar Chart of Historical Sessions
st.markdown("### 🏆 Session History Logs")
fig_bar = px.bar(
    df,
    x="session_id",
    y="overall_score",
    labels={"session_id": "Session ID Key", "overall_score": "Match Accuracy (%)"},
    color="overall_score",
    color_continuous_scale="Viridis",
)
fig_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font={'color': "white", 'family': "Outfit"},
    xaxis=dict(showticklabels=False), # Hide messy hash keys
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=20, b=20),
    height=280
)
st.plotly_chart(fig_bar, use_container_width=True)
