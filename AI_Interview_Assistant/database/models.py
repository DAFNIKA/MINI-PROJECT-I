# database/models.py
"""
SQL DDL Schemas for the SQLite Database.
Defines all the tables required for the AI-Powered Interview Preparation Assistant.
"""

CREATE_TABLES_SQL = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "resumes": """
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            education TEXT, -- JSON representation of parsed education
            experience TEXT, -- JSON representation of parsed experience
            parsed_details TEXT, -- JSON representation of other metadata
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "skills": """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            category TEXT, -- e.g., Technical, Soft Skill, Framework, Tool
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "job_descriptions": """
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description_text TEXT NOT NULL,
            required_skills TEXT, -- Comma-separated list of skills
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "interview_questions": """
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, -- NULL means system-seeded questions
            question_text TEXT NOT NULL,
            ideal_answer TEXT,
            category TEXT NOT NULL, -- e.g., Technical, HR, Behavioral, Scenario
            difficulty TEXT NOT NULL, -- Easy, Medium, Hard
            skill_reference TEXT, -- Associated skill keyword (e.g. Python, SQL)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "candidate_answers": """
        CREATE TABLE IF NOT EXISTS candidate_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            session_id TEXT, -- Links this answer to a specific interview session
            answer_text TEXT NOT NULL,
            similarity_score REAL NOT NULL,
            feedback TEXT NOT NULL,
            missing_concepts TEXT, -- Comma-separated list
            grammar_score REAL,
            communication_score REAL,
            confidence_score REAL,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES interview_questions(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "interview_results": """
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT UNIQUE NOT NULL, -- Tracks questions grouped in one session
            overall_score REAL NOT NULL,
            skills_score TEXT, -- JSON breakdown of scores by skill category
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "reports": """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            pdf_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (session_id) REFERENCES interview_results(session_id) ON DELETE CASCADE
        );
    """
}
