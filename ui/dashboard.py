"""
Classroom Directory Module
Displays and manages the list of students with search and export capabilities.
"""

import streamlit as st
import pandas as pd
from database.user_repo import get_all_users
from utils.auth import is_admin
from typing import Optional, Dict, Any
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
        st.error("❌ Unable to load directory data. Please try again later.")
        return fallback

def render_directory_stats(df: pd.DataFrame) -> None:
    """
    Render directory statistics cards.
    
    Args:
        df: DataFrame containing user data
    """
    total = len(df)
    
    # Calculate additional stats if columns exist
    has_linkedin = len(df[df['linkedin_url'].notna() & (df['linkedin_url'] != '')]) if 'linkedin_url' in df.columns else total
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            label="📊 Total Students", 
            value=f"{total:,}",
            delta=None,
            help="Total number of students in the directory"
        )
    
    with c2:
        st.metric(
            label="✅ Directory Status", 
            value="🟢 Live",
            delta=None,
            help="Current directory status"
        )
    
    with c3:
        st.metric(
            label="🔗 Profiles Available", 
            value=f"{has_linkedin:,}",
            delta=f"{((has_linkedin/total)*100):.0f}%" if total > 0 else "0%",
            help="Number of students with LinkedIn profiles"
        )
    
    with c4:
        # Calculate completion rate
        completion_rate = (has_linkedin / total * 100) if total > 0 else 0
        st.metric(
            label="📈 Completion Rate", 
            value=f"{completion_rate:.1f}%",
            delta=None,
            help="Percentage of students with complete profiles"
        )

def render_search_section(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render search input and filter DataFrame.
    
    Args:
        df: Original DataFrame
    
    Returns:
        Filtered DataFrame based on search
    """
    st.write("### 🔍 Find Classmates")
    
    # Create search columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input(
            "Search by name",
            placeholder="Enter student name...",
            label_visibility="collapsed"
        )
    
    with col2:
        # Add clear search button
        if st.button("🗑️ Clear", use_container_width=True):
            search_term = ""
            st.rerun()
    
    # Apply search filter
    filtered_df = df.copy()
    if search_term and 'name' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_term, case=False, na=False)
        ]
        
        # Show search results count
        if len(filtered_df) == 0:
            st.warning(f"🔍 No students found matching '{search_term}'")
        else:
            st.success(f"✅ Found {len(filtered_df)} student(s) matching '{search_term}'")
    
    return filtered_df, search_term

def render_directory_list(df: pd.DataFrame) -> None:
    """
    Render the list of students in the directory.
    
    Args:
        df: DataFrame containing user data to display
    """
    if df.empty:
        return
    
    st.write(f"### 👥 Student Directory ({len(df)} students)")
    
    # Add view options
    view_mode = st.radio(
        "View mode",
        ["List View", "Grid View"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if view_mode == "List View":
        render_list_view(df)
    else:
        render_grid_view(df)

def render_list_view(df: pd.DataFrame) -> None:
    """
    Render students in list view format.
    
    Args:
        df: DataFrame containing user data
    """
    for idx, row in df.iterrows():
        # Safely get data with defaults
        name = row.get('name', 'Unknown Student')
        linkedin_url = row.get('linkedin_url', '')
        
        # Create container with border for better visual separation
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 0.5])
            
            with col1:
                # Add student avatar/emoji based on name
                st.markdown(f"👨‍🎓 **{name}**")
                
                # Show additional info if available
                additional_info = []
                if 'email' in row and pd.notna(row['email']):
                    additional_info.append(f"📧 {row['email']}")
                if 'course' in row and pd.notna(row['course']):
                    additional_info.append(f"📚 {row['course']}")
                
                if additional_info:
                    st.caption(" | ".join(additional_info))
            
            with col2:
                if linkedin_url and isinstance(linkedin_url, str) and linkedin_url.strip():
                    st.link_button(
                        "🔗 Profile", 
                        linkedin_url, 
                        use_container_width=True,
                        type="secondary",
                        help=f"View {name}'s LinkedIn profile"
                    )
                else:
                    st.button(
                        "⏳ Pending", 
                        disabled=True, 
                        use_container_width=True,
                        help="LinkedIn profile not yet added"
                    )
            
            with col3:
                # Add index or join year if available
                if 'join_year' in row and pd.notna(row['join_year']):
                    st.caption(f"📅 {row['join_year']}")
            
            # Add divider between entries
            if idx < len(df) - 1:
                st.divider()

def render_grid_view(df: pd.DataFrame) -> None:
    """
    Render students in grid view format (3 columns).
    
    Args:
        df: DataFrame containing user data
    """
    # Create 3-column grid
    cols = st.columns(3)
    
    for idx, row in df.iterrows():
        with cols[idx % 3]:
            name = row.get('name', 'Unknown Student')
            linkedin_url = row.get('linkedin_url', '')
            
            # Create card-like container
            with st.container():
                st.markdown(f"**{name}**")
                
                if linkedin_url and isinstance(linkedin_url, str) and linkedin_url.strip():
                    st.link_button(
                        "🔗 Profile", 
                        linkedin_url, 
                        use_container_width=True,
                        type="secondary"
                    )
                else:
                    st.button(
                        "⏳ No Profile", 
                        disabled=True, 
                        use_container_width=True
                    )
                
                # Add email if available
                if 'email' in row and pd.notna(row['email']):
                    st.caption(f"📧 {row['email'][:15]}...")

def render_admin_export(df: pd.DataFrame) -> None:
    """
    Render admin export section with enhanced options.
    
    Args:
        df: Original DataFrame (unfiltered for admin)
    """
    if not is_admin():
        return
    
    st.divider()
    st.write("### 👑 Admin Controls")
    
    # Create tabs for different export options
    tab1, tab2, tab3 = st.tabs(["📥 Export Data", "📊 Statistics", "⚙️ Settings"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Export current view (filtered)
            if not df.empty:
                csv_filtered = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📁 Export Current View",
                    csv_filtered,
                    f"classroom_view_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    use_container_width=True,
                    help="Export the currently filtered student list"
                )
        
        with col2:
            # Export full dataset
            full_users = safe_data_fetch(get_all_users, fallback=[])
            if full_users:
                full_df = pd.DataFrame(full_users)
                csv_full = full_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📁 Export Full Directory",
                    csv_full,
                    f"full_classroom_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    use_container_width=True,
                    help="Export the complete unfiltered student directory"
                )
    
    with tab2:
        if not df.empty:
            # Show additional statistics
            st.write("**Directory Statistics**")
            
            # Calculate various stats
            total_students = len(df)
            students_with_linkedin = len(df[df['linkedin_url'].notna() & (df['linkedin_url'] != '')])
            
            stats_data = {
                "Metric": ["Total Students", "With LinkedIn", "Without LinkedIn", "Completion Rate"],
                "Count": [
                    total_students,
                    students_with_linkedin,
                    total_students - students_with_linkedin,
                    f"{(students_with_linkedin/total_students*100):.1f}%" if total_students > 0 else "0%"
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.write("**Directory Settings**")
        
        # Placeholder for future settings
        st.info("⚙️ Additional admin settings coming soon...")
        
        # Refresh option
        if st.button("🔄 Refresh Directory", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

def render() -> None:
    """
    Main render function for the classroom directory.
    This is the primary entry point maintained from the original code.
    """
    # Page header
    st.subheader("📚 Classroom Directory")
    
    # Add last update timestamp
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Fetch users with error handling
    users = safe_data_fetch(get_all_users, fallback=[])
    
    if not users:
        st.info("✨ No students have been added to the directory yet.")
        st.info("👋 Check back soon or contact an administrator to add students.")
        
        # Show sample placeholder for better UX
        with st.expander("📋 Directory Preview (Sample)"):
            st.write("The directory will display student information including:")
            st.write("• Student names")
            st.write("• LinkedIn profiles")
            st.write("• Additional details like email and courses")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(users)
    
    # Render statistics
    render_directory_stats(df)
    st.divider()
    
    # Search section
    filtered_df, search_term = render_search_section(df)
    st.divider()
    
    # Directory listing
    render_directory_list(filtered_df)
    
    # Admin export section (using original unfiltered data for admin functions)
    render_admin_export(df)
    
    # Footer with update info
    st.divider()
    st.caption(f"🕒 Directory last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Optional: Allow standalone execution
if __name__ == "__main__":
    render()