# ui/dashboard.py

import streamlit as st
import pandas as pd
from database.user_repo import get_all_users
from utils.auth import is_admin


def avatar(name: str) -> str:
    """Return initials for avatar circle."""
    parts = name.split()
    if len(parts) == 1:
        return parts[0][0].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def render():
    users = get_all_users()

    if not users:
        st.info("No students added yet.")
        return

    df = pd.DataFrame(users)

    # ---------- STATS ROW ----------
    total = len(df)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("👥 Total Students", total)
    with c2:
        st.metric("🟢 Active Directory", "Live")
    with c3:
        st.metric("🔗 Profiles Ready", total)

    st.divider()

    # ---------- SEARCH ----------
    search = st.text_input("🔎 Search classmates")
    if search:
        df = df[df["name"].str.contains(search, case=False)]

    # ---------- PROFILE CARDS ----------
    cols = st.columns(2)

    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 2]:
            with st.container():
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <div class="avatar">{avatar(row['name'])}</div>
                            <div>
                                <h3 style="margin:0">{row['name']}</h3>
                                <a class="streamlit-link" href="{row['linkedin_url']}" target="_blank">
                                    View LinkedIn Profile
                                </a>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ---------- ADMIN PANEL ----------
    if is_admin():
        st.divider()
        st.markdown("### 🔐 Admin Export")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download CSV",
            csv,
            "classroom_list.csv",
            "text/csv",
            use_container_width=True
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