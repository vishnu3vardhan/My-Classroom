

import streamlit as st
from utils.auth import login_form

# import pages
from ui import add_user, dashboard, analytics

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="MyConnections",
    page_icon="🔗",
    layout="wide"
)

# ---------- HEADER ----------
st.title("🔗 MyConnections")
st.caption("Connect with your classmates instantly through their LinkedIn profiles.")

st.divider()

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
login_form()

page = st.sidebar.radio(
    "Go to",
    [
        "Add Yourself",
        "Classroom Directory",
        "Analytics"
    ],
)

# ---------- ROUTING ----------
if page == "Add Yourself":
    add_user.render()

elif page == "Classroom Directory":
    dashboard.render()

elif page == "Analytics":
    analytics.render()

# ---------- FOOTER ----------
st.divider()
st.markdown(
    "Made by [VishnuVarDhan](https://www.instagram.com/v_v_d_28)",
)