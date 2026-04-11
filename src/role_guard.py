"""
Role Guard Utilities
Provides quick role-checking functions for page-level access control.
"""

import streamlit as st


def is_admin():
    """Check if current session user is an admin."""
    return st.session_state.get('role') == 'admin'


def is_user():
    """Check if current session user is a regular user."""
    return st.session_state.get('role') == 'user'


def require_role(expected_role):
    """
    Block access if the session role doesn't match.
    Returns True if access granted, False otherwise.
    """
    if not st.session_state.get('logged_in'):
        st.warning("⚠️ Please login first.")
        return False
    if st.session_state.get('role') != expected_role:
        st.error(f"🚫 Access Denied — {expected_role.title()} privileges required")
        return False
    return True
