# ui/add_user.py

import streamlit as st
from services.user_service import add_user


def render():

    st.markdown("### 🎓 Join the Classroom")

    st.write(
        "Add yourself to the directory so everyone can quickly access your LinkedIn profile."
    )

    # spacing
    st.write("")

    # centered form
    left, center, right = st.columns([1, 2, 1])

    with center:
        with st.container(border=True):

            st.markdown("#### 👤 Your Details")

            name = st.text_input("Full Name")
            username = st.text_input("LinkedIn Username")

            st.caption("Example: if your profile is linkedin.com/in/john-doe → enter john-doe")

            submitted = st.button("➕ Add Me to Directory", use_container_width=True)

            if submitted:
                success, message = add_user(name, username)

                if success:
                    st.success("🎉 You are now part of MyConnections!")
                    st.balloons()
                else:
                    st.error(message)