# database/database.py
"""
Database Connection and Initialization Manager.
Creates SQLite tables and seeds them with baseline interview questions.
"""

import os
import sqlite3
from database.models import CREATE_TABLES_SQL
from database.seed_data import QUESTIONS

DB_NAME = "database.db"

def get_db_path():
    """
    Returns the absolute path to the database file.
    Resolves relative to the directory containing this script.
    """
    # The database file should sit in the AI_Interview_Assistant root folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, DB_NAME)

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Configures row factory to return dictionary-like row objects.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """
    Initializes the database.
    Creates tables if they don't exist and seeds initial questions.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create all tables
        for table_name, create_sql in CREATE_TABLES_SQL.items():
            cursor.execute(create_sql)
        conn.commit()
        
        # Check if interview_questions contains seed data
        cursor.execute("SELECT COUNT(*) FROM interview_questions WHERE user_id IS NULL;")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Seeding database with default interview questions...")
            for q in QUESTIONS:
                cursor.execute(
                    """
                    INSERT INTO interview_questions (
                        user_id, question_text, ideal_answer, category, difficulty, skill_reference
                    ) VALUES (NULL, ?, ?, ?, ?, ?);
                    """,
                    (
                        q["question_text"],
                        q["ideal_answer"],
                        q["category"],
                        q["difficulty"],
                        q["skill_reference"]
                    )
                )
            conn.commit()
            print("Successfully seeded questions database.")
            
    except Exception as e:
        conn.rollback()
        print(f"Error during database initialization: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
