# services/analytics_service.py

from collections import Counter
from database.user_repo import get_all_users, get_user_count


def total_users():
    """Return total number of registered users."""
    return get_user_count()


def users_growth_by_day():
    """Return dict of {date: count} for chart plotting."""
    users = get_all_users()

    dates = [
        u["created_at"].date()
        for u in users
        if "created_at" in u
    ]

    counts = Counter(dates)
    return dict(sorted(counts.items()))


def latest_users(limit=5):
    """Return most recently added users."""
    users = get_all_users()
    return users[:limit]