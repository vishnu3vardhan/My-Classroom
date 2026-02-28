# utils/auth.py

import streamlit as st
from config.settings import ADMIN_PASSWORD


def login_form():
    """Render admin login form."""
    st.sidebar.subheader("Admin Login")

    password = st.sidebar.text_input("Enter admin password", type="password")

    if st.sidebar.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state["is_admin"] = True
            st.sidebar.success("Logged in as admin")
        else:
            st.sidebar.error("Incorrect password")


def is_admin():
    """Check admin status."""
    return st.session_state.get("is_admin", False)