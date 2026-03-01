import streamlit as st
import pandas as pd
from services.analytics_service import total_users, users_growth_by_day, latest_users


def render():
    st.subheader("📊 Classroom Insights")

    total = total_users()

    # ---------- TOP STATS ----------
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", total)
    c2.metric("Directory Status", "Active")
    c3.metric("Profiles Connected", total)

    st.divider()

    # ---------- GROWTH CHART ----------
    growth = users_growth_by_day()

    if growth:
        df = pd.DataFrame({
            "Date": list(growth.keys()),
            "Users Added": list(growth.values())
        })

        df = df.sort_values("Date").set_index("Date")

        st.write("Signups Over Time")
        st.line_chart(df, use_container_width=True)

    else:
        st.info("No growth data yet.")

    st.divider()

    # ---------- RECENT USERS ----------
    st.write("Recently Joined")

    latest = latest_users()

    if not latest:
        st.write("No users yet.")
        return

    for user in latest:
        col1, col2 = st.columns([4, 1])

        col1.write(f"**{user['name']}**")
        col2.link_button("Profile", user["linkedin_url"], use_container_width=True)

        st.divider()