# services/analytics_service.py

from collections import Counter
from database.user_repo import get_all_users, get_user_count
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def total_users():
    """Return total number of registered users."""
    return get_user_count()


def users_growth_by_day(days: Optional[int] = None) -> Dict[str, int]:
    """
    Return dict of {date: count} for chart plotting.
    
    Args:
        days: Optional limit to last N days
    """
    users = get_all_users()

    dates = [
        u["created_at"].date()
        for u in users
        if "created_at" in u
    ]

    counts = Counter(dates)
    sorted_counts = dict(sorted(counts.items()))
    
    # Limit to last N days if specified
    if days and sorted_counts:
        cutoff_date = datetime.now().date() - timedelta(days=days)
        sorted_counts = {
            date: count 
            for date, count in sorted_counts.items() 
            if date >= cutoff_date
        }
    
    # Convert date objects to strings for JSON serialization
    return {str(date): count for date, count in sorted_counts.items()}


def latest_users(limit=5):
    """Return most recently added users."""
    users = get_all_users()
    return users[:limit]


def get_growth_summary() -> Dict:
    """
    Return summary statistics for growth.
    """
    users = get_all_users()
    
    if not users:
        return {}
    
    # Extract creation dates
    dates = [
        u["created_at"].date()
        for u in users
        if "created_at" in u
    ]
    
    if not dates:
        return {}
    
    # Calculate metrics
    from datetime import date
    today = date.today()
    
    # Users in last 7 days
    last_7_dates = [d for d in dates if d >= today - timedelta(days=7)]
    last_30_dates = [d for d in dates if d >= today - timedelta(days=30)]
    
    return {
        "total": len(users),
        "last_7_days": len(last_7_dates),
        "last_30_days": len(last_30_dates),
        "first_join": min(dates) if dates else None,
        "latest_join": max(dates) if dates else None,
    }