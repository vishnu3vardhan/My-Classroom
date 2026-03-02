"""
Analytics Dashboard for Classroom Insights
Displays user statistics, growth trends, and recent user profiles.
"""

import streamlit as st
import pandas as pd
from services.analytics_service import total_users, users_growth_by_day, latest_users
from typing import Dict, List, Optional, Any
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

def render_metric_cards(total_users_count: int) -> None:
    """
    Render the top metric cards.
    
    Args:
        total_users_count: Total number of users
    """
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric(
            label="Total Students", 
            value=f"{total_users_count:,}" if total_users_count else "0",  # Add thousands separator
            delta=None
        )
    
    with c2:
        st.metric(
            label="Directory Status", 
            value="✅ Active",  # Added emoji for visual status
            delta=None
        )
    
    with c3:
        st.metric(
            label="Active Profiles", 
            value=f"{total_users_count:,}" if total_users_count else "0",
            delta=None,
            help="Number of connected profiles"  # Added tooltip
        )

def render_growth_chart() -> None:
    """Render the user growth chart."""
    growth_data = safe_data_fetch(users_growth_by_day, fallback={})
    
    if growth_data and isinstance(growth_data, dict):
        try:
            # Create DataFrame with data validation
            df = pd.DataFrame({
                "Date": pd.to_datetime(list(growth_data.keys())),  # Convert to datetime
                "Users Added": [max(0, val) for val in growth_data.values()]  # Ensure non-negative
            })
            
            # Sort and set index
            df = df.sort_values("Date").set_index("Date")
            
            # Display chart with better formatting
            st.write("### 📈 Signups Over Time")
            
            # Display metrics summary
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total in period", f"{df['Users Added'].sum():,}")
                with col2:
                    st.metric("Daily Avg", f"{df['Users Added'].mean():.1f}")
                with col3:
                    st.metric("Peak Day", f"{df['Users Added'].max():,}")
                
                # Show the chart
                st.line_chart(
                    df, 
                    use_container_width=True,
                    height=400  # Fixed height for consistency
                )
            else:
                st.info("📊 No growth data available yet. Check back soon!")
            
        except Exception as e:
            logger.error(f"Error processing growth data: {str(e)}")
            st.error("Unable to display growth chart. Please check your data format.")
    else:
        st.info("📊 No growth data available yet. Check back soon!")

def render_recent_users() -> None:
    """Render the list of recently joined users."""
    st.write("### 👥 Recently Joined")
    
    recent_users = safe_data_fetch(latest_users, fallback=[])
    
    if not recent_users:
        st.info("✨ No users have joined yet. Be the first!")
        return
    
    # Add user count summary
    st.caption(f"Showing {len(recent_users)} most recent users")
    
    # Create expandable sections for better organization
    with st.expander("View Recent Users", expanded=True):
        for idx, user in enumerate(recent_users):
            # Validate user data structure
            if not isinstance(user, dict):
                logger.warning(f"Invalid user data format at index {idx}")
                continue
            
            name = user.get('name', 'Unknown User')
            linkedin_url = user.get('linkedin_url', '#')
            
            # Create columns with better proportion
            col1, col2, col3 = st.columns([3, 1, 0.5])
            
            with col1:
                # Add emoji based on name (or use consistent avatar)
                st.markdown(f"👤 **{name}**")
            
            with col2:
                if linkedin_url and linkedin_url != '#':
                    st.link_button(
                        "🔗 Profile", 
                        linkedin_url, 
                        use_container_width=True,
                        type="secondary"  # Added button styling
                    )
                else:
                    st.write("⏳ Pending")
            
            with col3:
                # Add join time indicator if available
                if 'joined_at' in user:
                    st.caption("🕐 New")
            
            # Add subtle divider
            if idx < len(recent_users) - 1:
                st.divider()

def render() -> None:
    """
    Main render function for the analytics dashboard.
    This is the primary entry point maintained from the original code.
    """
    # Page configuration
    st.subheader("📊 Classroom Insights")
    
    # Fetch total users with error handling
    total = safe_data_fetch(total_users, fallback=0)
    
    # Render components
    render_metric_cards(total)
    st.divider()
    render_growth_chart()
    st.divider()
    render_recent_users()
    
    # Add footer with last update time
    st.caption(f"🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Optional: Allow standalone execution
if __name__ == "__main__":
    render()