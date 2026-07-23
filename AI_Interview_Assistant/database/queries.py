# database/queries.py
"""
Database Queries Module.
Implements the CRUD operations for users, resumes, skills, job descriptions,
interview questions, answers, results, and reports.
"""

import json
from database.database import get_db_connection

# --- USER QUERIES ---

def create_user(username, password_hash, email, full_name=None):
    """
    Creates a new user in the database.
    Returns the user ID on success, or None on failure.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, email, full_name)
            VALUES (?, ?, ?, ?);
            """,
            (username, password_hash, email, full_name)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    """
    Retrieves user record by username.
    Returns a dict-like Row or None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?;", (username,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user by username: {e}")
        return None
    finally:
        conn.close()

def get_user_by_id(user_id):
    """
    Retrieves user record by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None
    finally:
        conn.close()


# --- RESUME QUERIES ---

def save_resume(user_id, filename, raw_text, education=None, experience=None, parsed_details=None):
    """
    Saves parsed resume text and structure for a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        edu_str = json.dumps(education) if education else None
        exp_str = json.dumps(experience) if experience else None
        details_str = json.dumps(parsed_details) if parsed_details else None
        
        cursor.execute(
            """
            INSERT INTO resumes (user_id, filename, raw_text, education, experience, parsed_details)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (user_id, filename, raw_text, edu_str, exp_str, details_str)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error saving resume: {e}")
        return None
    finally:
        conn.close()

def get_latest_resume(user_id):
    """
    Fetches the most recently uploaded resume for a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT 1;",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            res = dict(row)
            res["education"] = json.loads(res["education"]) if res["education"] else []
            res["experience"] = json.loads(res["experience"]) if res["experience"] else []
            res["parsed_details"] = json.loads(res["parsed_details"]) if res["parsed_details"] else {}
            return res
        return None
    except Exception as e:
        print(f"Error fetching latest resume: {e}")
        return None
    finally:
        conn.close()


# --- SKILLS QUERIES ---

def save_user_skills(user_id, skills_list, category="Technical"):
    """
    Saves a list of skills associated with a user. Avoids duplicates.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete existing skills for user in this category to refresh
        cursor.execute("DELETE FROM skills WHERE user_id = ? AND category = ?;", (user_id, category))
        
        for skill in set(skills_list):
            if skill.strip():
                cursor.execute(
                    "INSERT INTO skills (user_id, skill_name, category) VALUES (?, ?, ?);",
                    (user_id, skill.strip(), category)
                )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving user skills: {e}")
        return False
    finally:
        conn.close()

def get_user_skills(user_id):
    """
    Returns list of skills for a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT skill_name, category FROM skills WHERE user_id = ?;", (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching user skills: {e}")
        return []
    finally:
        conn.close()


# --- JOB DESCRIPTION QUERIES ---

def save_job_description(user_id, title, description_text, required_skills=None):
    """
    Saves job description details for matching.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO job_descriptions (user_id, title, description_text, required_skills)
            VALUES (?, ?, ?, ?);
            """,
            (user_id, title, description_text, required_skills)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error saving job description: {e}")
        return None
    finally:
        conn.close()

def get_latest_job_description(user_id):
    """
    Retrieves the latest job description matching configuration.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM job_descriptions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1;",
            (user_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching job description: {e}")
        return None
    finally:
        conn.close()


# --- INTERVIEW QUESTIONS QUERIES ---

def get_seeded_questions_by_skills(skills, difficulty, limit=5):
    """
    Retrieves default (seeded) interview questions matching user skills and difficulty.
    Fallback to general HR/Behavioral if not enough technical matches are found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    questions = []
    try:
        # Match technical questions linked to skill names
        if skills:
            placeholders = ",".join(["?"] * len(skills))
            query = f"""
                SELECT * FROM interview_questions 
                WHERE user_id IS NULL 
                AND category = 'Technical'
                AND difficulty = ? 
                AND LOWER(skill_reference) IN ({placeholders})
                ORDER BY RANDOM() LIMIT ?;
            """
            params = [difficulty] + [s.lower() for s in skills] + [limit]
            cursor.execute(query, params)
            questions.extend([dict(r) for r in cursor.fetchall()])

        # If we need more questions, fill with HR / Behavioral / Scenario questions of same difficulty
        needed = limit - len(questions)
        if needed > 0:
            cursor.execute(
                """
                SELECT * FROM interview_questions 
                WHERE user_id IS NULL 
                AND category IN ('HR', 'Behavioral', 'Scenario')
                AND difficulty = ?
                ORDER BY RANDOM() LIMIT ?;
                """,
                (difficulty, needed)
            )
            questions.extend([dict(r) for r in cursor.fetchall()])
            
        return questions
    except Exception as e:
        print(f"Error fetching questions: {e}")
        return []
    finally:
        conn.close()

def save_custom_interview_question(user_id, question_text, ideal_answer, category, difficulty, skill_reference=None):
    """
    Saves an interview question generated specifically for a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO interview_questions (user_id, question_text, ideal_answer, category, difficulty, skill_reference)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (user_id, question_text, ideal_answer, category, difficulty, skill_reference)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error saving custom question: {e}")
        return None
    finally:
        conn.close()


# --- CANDIDATE ANSWERS QUERIES ---

def save_candidate_answer(question_id, user_id, session_id, answer_text, similarity_score, feedback, 
                            missing_concepts=None, grammar_score=None, communication_score=None, confidence_score=None):
    """
    Records candidate answer evaluation results.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO candidate_answers (
                question_id, user_id, session_id, answer_text, similarity_score, feedback, 
                missing_concepts, grammar_score, communication_score, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                question_id, user_id, session_id, answer_text, similarity_score, feedback, 
                missing_concepts, grammar_score, communication_score, confidence_score
            )
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error saving answer: {e}")
        return None
    finally:
        conn.close()

def get_answers_by_session(session_id):
    """
    Retrieves all evaluated answers belonging to a particular interview session.
    Joins with questions for UI display.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT ca.*, iq.question_text, iq.ideal_answer, iq.category, iq.difficulty, iq.skill_reference 
            FROM candidate_answers ca
            JOIN interview_questions iq ON ca.question_id = iq.id
            WHERE ca.session_id = ?
            ORDER BY ca.id ASC;
            """,
            (session_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching answers by session: {e}")
        return []
    finally:
        conn.close()


# --- INTERVIEW RESULTS QUERIES ---

def save_interview_result(user_id, session_id, overall_score, skills_score=None):
    """
    Saves summary metrics for a completed interview session.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        skills_score_str = json.dumps(skills_score) if skills_score else None
        cursor.execute(
            """
            INSERT INTO interview_results (user_id, session_id, overall_score, skills_score)
            VALUES (?, ?, ?, ?);
            """,
            (user_id, session_id, overall_score, skills_score_str)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error saving interview result: {e}")
        return None
    finally:
        conn.close()

def get_interview_history(user_id):
    """
    Retrieves all interview results for a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM interview_results 
            WHERE user_id = ? 
            ORDER BY created_at DESC;
            """,
            (user_id,)
        )
        rows = cursor.fetchall()
        results = []
        for r in rows:
            res = dict(r)
            res["skills_score"] = json.loads(res["skills_score"]) if res["skills_score"] else {}
            results.append(res)
        return results
    except Exception as e:
        print(f"Error fetching interview history: {e}")
        return []
    finally:
        conn.close()

def get_interview_result_by_session(session_id):
    """
    Retrieves the summary metrics of a specific session.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM interview_results WHERE session_id = ?;",
            (session_id,)
        )
        row = cursor.fetchone()
        if row:
            res = dict(row)
            res["skills_score"] = json.loads(res["skills_score"]) if res["skills_score"] else {}
            return res
        return None
    except Exception as e:
        print(f"Error fetching session result: {e}")
        return None
    finally:
        conn.close()


# --- REPORTS QUERIES ---

def save_report(user_id, session_id, pdf_path):
    """
    Saves report PDF path reference.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reports (user_id, session_id, pdf_path) VALUES (?, ?, ?);",
            (user_id, session_id, pdf_path)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error saving report: {e}")
        return None
    finally:
        conn.close()

def get_user_reports(user_id):
    """
    Gets list of generated PDF reports for a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.*, ir.overall_score 
            FROM reports r
            JOIN interview_results ir ON r.session_id = ir.session_id
            WHERE r.user_id = ? 
            ORDER BY r.created_at DESC;
            """,
            (user_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching user reports: {e}")
        return []
    finally:
        conn.close()
