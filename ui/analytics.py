# ui/analytics.py

import streamlit as st
import pandas as pd
from services.analytics_service import total_users, users_growth_by_day, latest_users


def render():
    st.markdown("### 📊 Classroom Insights")

    total = total_users()

    # ---------- TOP STATS ----------
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("👥 Total Students", total)
    with c2:
        st.metric("📈 Directory Growth", "Active")
    with c3:
        st.metric("🔗 Profiles Connected", total)

    st.divider()

    # ---------- GROWTH CHART ----------
    growth = users_growth_by_day()
    if growth:
        df = pd.DataFrame({
            "Date": list(growth.keys()),
            "Users Added": list(growth.values())
        })
        df = df.sort_values("Date")
        df = df.set_index("Date")
        st.markdown("#### 📈 Signups Over Time")
        st.line_chart(df, use_container_width=True)
    else:
        st.info("No growth data yet.")

    st.divider()

    # ---------- RECENT USERS ----------
    st.markdown("#### 🕒 Recently Joined")
    latest = latest_users()
    if not latest:
        st.write("No users yet.")
    else:
        cols = st.columns(2)
        for i, user in enumerate(latest):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="card" style="padding:10px; margin-bottom:10px;">
                        <strong>{user['name']}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ---------- FOOTER ----------
    st.markdown(
        """
        <div style="
            margin-top:40px;
            padding:12px;
            text-align:center;
            color: #6b7280;
            font-size:14px;
        ">
        Created by <a href="https://www.instagram.com/v_v_d_28" target="_blank" style="color:#3b82f6; text-decoration:none;">VishnuVarDhan</a>
        </div>
        """,
        unsafe_allow_html=True
    )