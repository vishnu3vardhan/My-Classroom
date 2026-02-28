# database/user_repo.py

from datetime import datetime
from database.mongo import get_db
from config.settings import USER_COLLECTION

try:
    import streamlit as st
    _USE_CACHE = True
except Exception:
    _USE_CACHE = False


def _get_collection():
    db = get_db()
    return db[USER_COLLECTION]


def insert_user(name: str, username: str, linkedin_url: str):
    """Insert a new user document."""
    collection = _get_collection()

    user = {
        "name": name,
        "username": username,
        "linkedin_url": linkedin_url,
        "created_at": datetime.utcnow()
    }

    result = collection.insert_one(user)

    # clear cached queries after insert
    if _USE_CACHE:
        get_all_users.clear()
        get_user_count.clear()

    return result


# ---- Cached queries for fast UI ----
if _USE_CACHE:

    @st.cache_data(show_spinner=False, ttl=60)
    def get_all_users():
        collection = _get_collection()
        return list(collection.find({}, {"_id": 0}).sort("created_at", -1))

    @st.cache_data(show_spinner=False, ttl=60)
    def get_user_count():
        collection = _get_collection()
        return collection.count_documents({})

else:

    def get_all_users():
        collection = _get_collection()
        return list(collection.find({}, {"_id": 0}).sort("created_at", -1))

    def get_user_count():
        collection = _get_collection()
        return collection.count_documents({})


def find_by_username(username: str):
    """Check if a LinkedIn username already exists."""
    collection = _get_collection()
    return collection.find_one({"username": username})