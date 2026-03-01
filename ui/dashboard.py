import streamlit as st
import pandas as pd
from database.user_repo import get_all_users
from utils.auth import is_admin


def render():
    st.subheader("📚 Classroom Directory")

    users = get_all_users()

    if not users:
        st.info("No students added yet.")
        return

    df = pd.DataFrame(users)

    # ---------- STATS ----------
    c1, c2, c3 = st.columns(3)
    total = len(df)

    c1.metric("Total Students", total)
    c2.metric("Directory Status", "Live")
    c3.metric("Profiles Available", total)

    st.divider()

    # ---------- SEARCH ----------
    search = st.text_input("Search classmates")

    if search:
        df = df[df["name"].str.contains(search, case=False)]

    # ---------- DIRECTORY LIST ----------
    for _, row in df.iterrows():
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"**{row['name']}**")

        with col2:
            st.link_button("Profile", row["linkedin_url"], use_container_width=True)

        st.divider()

    # ---------- ADMIN EXPORT ----------
    if is_admin():
        st.subheader("Admin Export")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "classroom_list.csv",
            "text/csv",
            use_container_width=True
        )