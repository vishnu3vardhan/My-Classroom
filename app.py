# app.py

import streamlit as st
from utils.auth import login_form

# import pages
from ui import add_user, dashboard, analytics

st.set_page_config(
    page_title="MyConnections",
    page_icon="🔗",
    layout="wide"
)

# ---------- THEME / DESIGN SYSTEM (Modern, Minimal, Emoji-friendly) ----------
st.markdown(
    """
    <style>
    /* Import a clean, modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    :root{
        --bg: #f6f8fb;
        --panel: #ffffff;
        --muted: #6b7280;
        --primary: #3b82f6;       /* vivid blue for accents */
        --accent: #60a5fa;        /* lighter blue accent */
        --glass: rgba(255,255,255,0.65);
        --card-shadow: 0 6px 18px rgba(46,59,73,0.08);
        --radius: 12px;
    }

    /* page background and font */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        color: #0f172a;
    }

    /* main container max width (keeps layout minimal) */
    .main-container {
        max-width: 1100px;
        margin: 0 auto;
    }

    /* header */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin: 8px 0 4px 0;
        letter-spacing: -0.3px;
    }
    .subtitle {
        color: var(--muted);
        margin: 0 0 18px 0;
        font-weight: 400;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(250,250,252,0.95));
        border-right: 1px solid rgba(15,23,42,0.03);
        padding: 18px;
    }
    .stSidebar .css-1d391kg { padding-top: 6px; } /* small tweak to compact sidebar */

    /* card */
    .card {
        background: var(--panel);
        border-radius: var(--radius);
        box-shadow: var(--card-shadow);
        padding: 16px;
        margin-bottom: 14px;
        transition: transform .14s ease, box-shadow .14s ease;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 10px 24px rgba(46,59,73,0.09); }

    /* avatar circle (emoji friendly) */
    .avatar {
        width:56px;
        height:56px;
        border-radius:50%;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        font-weight:700;
        color:white;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        box-shadow: 0 4px 12px rgba(59,130,246,0.14);
        font-size:20px;
    }

    /* buttons */
    div.stButton > button, button.css-1q8dd3e { /* fallback for different streamlit versions */
        background: var(--primary);
        color: white;
        border: none;
        padding: 8px 14px;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 6px 18px rgba(59,130,246,0.16);
        transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
    }
    div.stButton > button:hover, button.css-1q8dd3e:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(59,130,246,0.18);
        opacity: 0.98;
    }

    /* link button style (links that look like buttons) */
    a.streamlit-link {
        display:inline-block;
        background: transparent;
        border: 1px solid rgba(15,23,42,0.06);
        padding: 8px 12px;
        border-radius: 10px;
        text-decoration: none;
        color: var(--primary);
        font-weight: 600;
    }
    a.streamlit-link:hover {
        background: rgba(59,130,246,0.06);
    }

    /* metrics (small visual polish) */
    .metric-container { display:flex; gap:16px; align-items:center; }
    .metric-pill {
        background: linear-gradient(90deg, rgba(99,102,241,0.08), rgba(96,165,250,0.04));
        padding: 10px 14px;
        border-radius: 12px;
        font-weight: 700;
        color: #0b1220;
    }

    /* subtle divider */
    .soft-divider { height:1px; background: rgba(11,17,32,0.04); margin:18px 0; border-radius:2px; }

    /* small screens responsiveness */
    @media (max-width: 800px) {
        .main-title { font-size: 30px; }
        .card { padding: 12px; }
        .avatar { width:46px; height:46px; font-size:18px; }
    }

    /* make the default markdown header spacing tighter */
    .css-18e3th9 { padding-top: 6px; } /* streamlit main block - best effort */
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔗 MyConnections</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Connect with your classmates instantly through their LinkedIn profiles.</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📌 Navigation")
login_form()

page = st.sidebar.radio(
    "Go to",
    [
        "Add Yourself",
        "Classroom Directory",
        "Analytics"
    ],
)

# ---------- ROUTING (pages use consistent classes like 'card' for visual harmony) ----------
if page == "Add Yourself":
    # Wrap page content in a card container where appropriate (pages themselves already create containers)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    add_user.render()
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Classroom Directory":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    dashboard.render()
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Analytics":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    analytics.render()
    st.markdown('</div>', unsafe_allow_html=True)

# close main container
st.markdown('</div>', unsafe_allow_html=True)