# config/settings.py

import os

# --- Mongo URI loading (optimized for Streamlit Cloud) ---
def _get_mongo_uri():
    # Try Streamlit secrets first (fast on Cloud)
    try:
        import streamlit as st
        if "MONGO_URI" in st.secrets:
            return st.secrets["MONGO_URI"]
    except Exception:
        pass

    # Fallback for local dev
    return os.getenv("MONGO_URI", "mongodb://localhost:27017")


MONGO_URI = _get_mongo_uri()

# --- App config ---
ADMIN_PASSWORD = "OnlyMyConnectionsMatterHere"
LINKEDIN_BASE_URL = "https://www.linkedin.com/in/"

# --- DB config ---
DB_NAME = "classroom_db"
USER_COLLECTION = "users"