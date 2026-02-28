# database/mongo.py

from pymongo import MongoClient
from config.settings import MONGO_URI, DB_NAME

try:
    import streamlit as st
    _USE_CACHE = True
except Exception:
    _USE_CACHE = False


def _create_connection():
    """Create Mongo client and return DB."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]


# Use Streamlit caching on Cloud
if _USE_CACHE:

    @st.cache_resource(show_spinner=False)
    def get_db():
        return _create_connection()

else:
    # fallback for local runs without Streamlit context
    _db = None

    def get_db():
        global _db
        if _db is None:
            _db = _create_connection()
        return _db