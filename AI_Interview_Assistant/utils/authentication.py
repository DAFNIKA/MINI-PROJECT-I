# utils/authentication.py
"""
Authentication Utilities.
Handles password hashing using bcrypt and session state management in Streamlit.
"""

import bcrypt
import streamlit as st
from database.queries import get_user_by_username, create_user

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a stored bcrypt hash.
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def init_session():
    """
    Initializes Streamlit session state variables for user session management.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "full_name" not in st.session_state:
        st.session_state.full_name = None

def login_user(user):
    """
    Sets session state variables on successful login.
    'user' can be a SQLite Row object or a dict.
    """
    st.session_state.logged_in = True
    st.session_state.user_id = user["id"]
    st.session_state.username = user["username"]
    st.session_state.full_name = user["full_name"]

def logout_user():
    """
    Clears session state variables on logout.
    """
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.full_name = None
    # Rerun to refresh pages and sidebar navigation
    st.rerun()

def authenticate(username, password):
    """
    Authenticates a user by username and password.
    Returns the user dictionary if successful, else None.
    """
    user_row = get_user_by_username(username)
    if user_row:
        user_dict = dict(user_row)
        if check_password(password, user_dict["password_hash"]):
            return user_dict
    return None

def register(username, password, email, full_name):
    """
    Registers a new user after hashing the password.
    Returns (True, user_id) on success, or (False, error_message) on failure.
    """
    if get_user_by_username(username):
        return False, "Username already exists."
        
    hashed = hash_password(password)
    user_id = create_user(username, hashed, email, full_name)
    if user_id:
        return True, user_id
    else:
        return False, "Database insertion failed."
