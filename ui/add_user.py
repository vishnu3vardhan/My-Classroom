"""
Join the Classroom Module
Handles user registration form for adding students to the directory.
"""

import streamlit as st
from services.user_service import add_user
import re
from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_linkedin_username(username: str) -> Tuple[bool, str]:
    """
    Validate LinkedIn username format.
    
    Args:
        username: LinkedIn username to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username or not username.strip():
        return False, "LinkedIn username is required"
    
    username = username.strip()
    
    if not re.match(r'^[a-zA-Z0-9-]+$', username):
        return False, "Username can only contain letters, numbers, and hyphens"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 100:
        return False, "Username exceeds maximum length (100 characters)"
    
    return True, ""

def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate full name format.
    
    Args:
        name: Full name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Full name is required"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    if len(name) > 100:
        return False, "Name exceeds maximum length (100 characters)"
    
    if not re.match(r'^[a-zA-Z\s\.\-\'\_]+$', name):
        return False, "Name contains invalid characters"
    
    return True, ""

def render_registration_form() -> None:
    """
    Render the registration form with validation.
    """
    left, center, right = st.columns([1, 2, 1])
    
    with center:
        with st.form(key="registration_form", clear_on_submit=True):
            
            st.markdown("##### Personal Information")
            
            name = st.text_input(
                "Full Name *",
                placeholder="e.g., John Doe",
                help="Enter your full legal name or preferred name"
            )
            
            st.markdown("##### LinkedIn Profile")
            
            username = st.text_input(
                "LinkedIn Username *",
                placeholder="e.g., john-doe",
                help="The unique identifier from your LinkedIn profile URL"
            )
            
            st.caption(
                "Format: If your profile is linkedin.com/in/john-doe, enter **john-doe**"
            )
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button(
                    "Submit Registration",
                    use_container_width=True,
                    type="primary"
                )
            
            if submitted:
                process_registration(name, username)

def process_registration(name: str, username: str) -> None:
    """
    Process and validate registration submission.
    
    Args:
        name: User's full name
        username: LinkedIn username
    """
    # Validate inputs
    name_valid, name_error = validate_name(name)
    if not name_valid:
        st.error(f"Validation Error: {name_error}")
        return
    
    username_valid, username_error = validate_linkedin_username(username)
    if not username_valid:
        st.error(f"Validation Error: {username_error}")
        return
    
    # Clean inputs
    name_clean = name.strip()
    username_clean = username.strip()
    
    # Show processing indicator
    with st.status("Processing registration...", expanded=False) as status:
        try:
            st.write("✓ Validating information...")
            success, message = add_user(name_clean, username_clean)
            
            if success:
                status.update(
                    label="Registration Complete", 
                    state="complete"
                )
                st.success("Successfully added to the directory")
                
                # Show confirmation details
                with st.container():
                    st.markdown("**Registration Details:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Name:** {name_clean}")
                    with col2:
                        profile_url = f"https://linkedin.com/in/{username_clean}"
                        st.markdown(f"**LinkedIn:** [{username_clean}]({profile_url})")
            else:
                status.update(
                    label="Registration Failed", 
                    state="error"
                )
                st.error(f"Registration Error: {message}")
                
                # Provide specific guidance based on error
                if "already exists" in message.lower():
                    st.info(
                        "This LinkedIn profile is already registered. "
                        "Please verify your username or contact support if you believe this is an error."
                    )
                elif "invalid" in message.lower():
                    st.info("Please verify your LinkedIn username and try again.")
                    
        except Exception as e:
            status.update(label="System Error", state="error")
            logger.error(f"Registration error: {str(e)}")
            st.error("An unexpected error occurred. Please try again later.")

def render_information_section() -> None:
    """
    Render information section about directory benefits.
    """
    with st.expander("About the Directory", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Directory Benefits**
            - Professional networking with peers
            - Centralized access to student profiles
            - Collaboration opportunities
            - Mentorship connections
            """)
        
        with col2:
            st.markdown("""
            **Data Usage**
            - Information visible only to classroom members
            - Used for academic and professional networking
            - Not shared with third parties
            - You can request removal at any time
            """)

def render_guidelines_section() -> None:
    """
    Render guidelines and requirements section.
    """
    with st.expander("Guidelines & Requirements", expanded=False):
        st.markdown("""
        **Registration Guidelines:**
        
        1. **Name:** Use your full legal name or preferred professional name
        2. **LinkedIn Username:** Must be your actual LinkedIn profile identifier
        3. **Accuracy:** Ensure all information is accurate and up-to-date
        4. **Professional Conduct:** Directory is for professional networking purposes only
        
        **Note:** Duplicate registrations or inappropriate content may be removed by administrators.
        """)

def render() -> None:
    """
    Main render function for the Join Classroom page.
    """
    # Header section
    st.subheader("Directory Registration")
    
    st.markdown("""
    Complete the form below to add your profile to the classroom directory. 
    This allows classmates and instructors to connect with you professionally.
    """)
    
    st.divider()
    
    # Registration form
    render_registration_form()
    
    st.divider()
    
    # Information sections in columns for compact layout
    col1, col2 = st.columns(2)
    
    with col1:
        render_information_section()
    
    with col2:
        render_guidelines_section()
    
    # Footer with timestamp
    st.divider()
    from datetime import datetime
    st.caption(f"© {datetime.now().year} Classroom Directory System")

# Optional: Allow standalone execution
if __name__ == "__main__":
    render()