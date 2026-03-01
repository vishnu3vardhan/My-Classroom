import streamlit as st
from services.user_service import add_user


def render():

    st.subheader("🎓 Join the Classroom")
    st.write(
        "Add yourself to the directory so everyone can quickly access your LinkedIn profile."
    )

    st.divider()

    # centered form layout
    left, center, right = st.columns([1, 2, 1])

    with center:

        name = st.text_input("Full Name", placeholder="Enter your name")

        username = st.text_input(
            "LinkedIn Username",
            placeholder="e.g. john-doe"
        )

        st.caption(
            "If your profile is linkedin.com/in/john-doe, just enter **john-doe**."
        )

        st.write("")

        submitted = st.button(
            "Add Me to Directory",
            use_container_width=True
        )

        if submitted:
            success, message = add_user(name, username)

            if success:
                st.success("You are now part of MyConnections 🎉")
                st.balloons()
            else:
                st.error(message)