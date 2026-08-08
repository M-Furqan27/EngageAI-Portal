"""
frontend/utils/sidebar.py

Shared sidebar "account" widget — Dashboard aur Profile dono pages
isay call karte hain taake Logout button har jagah consistent rahe.
"""

import streamlit as st


def render_account_sidebar():
    user = st.session_state.get("user") or {}
    name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "Account"
    email = user.get("email", "")

    with st.sidebar:
        st.divider()
        with st.container(border=True):
            st.caption("Signed in as")
            st.markdown(f"**{name}**")
            if email:
                st.caption(email)

        if st.button("🚪 Log out", use_container_width=True, key="sidebar_logout_btn"):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.onboarding_completed = False
            st.rerun()
