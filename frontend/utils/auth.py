"""
frontend/utils/auth.py
"""

import streamlit as st


def require_login(message: str = "Please log in to continue."):
    if "token" not in st.session_state or st.session_state.token is None:
        st.session_state.flash_message = message
        st.switch_page("portal/1_login.py")
        st.stop()