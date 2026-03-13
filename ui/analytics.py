"""
Analytics Dashboard for Classroom Insights
Displays user statistics, growth trends, and recent user profiles.
"""

import streamlit as st
import pandas as pd
from services.analytics_service import total_users, users_growth_by_day, latest_users
from typing import Dict
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_data_fetch(func, fallback=None):
    """
    Safely fetch data with error handling.
    
    Args:
        func: Function to execute
        fallback: Fallback value if function fails
    
    Returns:
        Fetched data or fallback value
    """
    try:
        return func()
    except Exception as e:
        logger.error(f"Error fetching data from {func.__name__}: {str(e)}")
        st.error(f"Unable to load data. Please try again later.")
        return fallback

def render_metric_cards(total_users_count: int, growth_data: Dict = None) -> None:
    """
    Render the top metric cards with delta indicators.
    
    Args:
        total_users_count: Total number of users
        growth_data: Growth data for calculating deltas
    """
    # Calculate week-over-week growth if data available
    wow_growth = None
    if growth_data and len(growth_data) >= 7:
        dates = sorted(growth_data.keys())
        last_7_days = sum(growth_data.get(d, 0) for d in dates[-7:])
        previous_7_days = sum(growth_data.get(d, 0) for d in dates[-14:-7]) if len(dates) >= 14 else 0
        
        if previous_7_days > 0:
            growth_pct = ((last_7_days - previous_7_days) / previous_7_days) * 100
            wow_growth = f"{growth_pct:+.1f}%"
        elif last_7_days > 0:
            wow_growth = "+100%"
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric(
            label="Total Students", 
            value=f"{total_users_count:,}" if total_users_count else "0",
            delta=wow_growth,
            help="Total registered students. Delta shows week-over-week growth."
        )
    
    with c2:
        st.metric(
            label="Directory Status", 
            value="Active",
            delta=None,
            help="Current directory status"
        )
    
    with c3:
        active_rate = "100%" if total_users_count > 0 else "0%"
        st.metric(
            label="Profiles Complete", 
            value=active_rate,
            delta=None,
            help="Percentage of students with complete profiles"
        )

def render_growth_summary(growth_data: Dict) -> None:
    """
    Render growth summary statistics in a clean card format.
    
    Args:
        growth_data: Dictionary of date -> count
    """
    st.subheader("Growth Summary")
    
    if not growth_data:
        st.info("Insufficient data for growth summary")
        return
    
    # Create DataFrame
    df = pd.DataFrame({
        "Date": pd.to_datetime(list(growth_data.keys())),
        "New Users": list(growth_data.values())
    }).sort_values("Date")
    
    if df.empty:
        st.info("No growth data available")
        return
    
    # Calculate statistics
    total_growth = df['New Users'].sum()
    avg_daily = df['New Users'].mean()
    max_daily = df['New Users'].max()
    min_daily = df['New Users'].min()
    
    # Create four columns for summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Growth",
            value=f"{total_growth:,}",
            help="Total new users in the selected period"
        )
    
    with col2:
        st.metric(
            label="Daily Avg",
            value=f"{avg_daily:.1f}",
            help="Average new users per day"
        )
    
    with col3:
        st.metric(
            label="Peak Day",
            value=f"{max_daily:,}",
            help="Highest number of new users in a single day"
        )
    
    with col4:
        st.metric(
            label="Lowest Day",
            value=f"{min_daily:,}",
            help="Lowest number of new users in a single day"
        )

def render_recent_users_table() -> None:
    """Render recent users in a clean table format."""
    st.subheader("Recent Joiners")
    
    recent_users = safe_data_fetch(lambda: latest_users(limit=10), fallback=[])
    
    if not recent_users:
        st.info("No recent joiners")
        return
    
    # Prepare data for table
    table_data = []
    for user in recent_users:
        created_at = user.get('created_at', '')
        if created_at:
            if isinstance(created_at, datetime):
                date_str = created_at.strftime('%Y-%m-%d')
            else:
                date_str = str(created_at)
        else:
            date_str = ""
        
        table_data.append({
            "Name": user.get('name', 'Unknown'),
            "Joined": date_str,
            "Profile": user.get('linkedin_url', ''),
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Name": st.column_config.TextColumn("Name", width=250),
                "Joined": st.column_config.DateColumn("Join Date", format="YYYY-MM-DD", width=150),
                "Profile": st.column_config.LinkColumn("LinkedIn Profile", width=200, display_text="View")
            }
        )
        
        st.caption(f"Showing {len(recent_users)} most recent registrations")

def render() -> None:
    """
    Main render function for the analytics dashboard.
    """
    # Page header
    st.title("Analytics Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch data
    total = safe_data_fetch(total_users, fallback=0)
    growth_data = safe_data_fetch(users_growth_by_day, fallback={})
    
    # Overview metrics
    with st.container(border=True):
        st.subheader("Overview")
        render_metric_cards(total, growth_data)
    
    st.divider()
    
    # Growth summary
    with st.container(border=True):
        render_growth_summary(growth_data)
    
    st.divider()
    
    # Recent users section
    with st.container(border=True):
        render_recent_users_table()

# Optional: Allow standalone execution
if __name__ == "__main__":
    render()