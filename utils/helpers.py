# utils/helpers.py

from config.settings import LINKEDIN_BASE_URL


def build_linkedin_url(username: str) -> str:
    """Generate full LinkedIn profile URL from username."""
    username = username.strip().replace(" ", "")
    return f"{LINKEDIN_BASE_URL}{username}"


def normalize_username(username: str) -> str:
    """Clean username input."""
    return username.strip().lower()