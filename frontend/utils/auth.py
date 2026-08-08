"""
frontend/utils/auth.py

require_login() — koi bhi protected page (Onboarding, Dashboard, Profile,
Admin) isay sabse pehle call karti hai. Agar user logged in nahi hai
(chahe direct link se kholi ho, kisi bhi tab mein) to ek simple alert
message ke sath seedha Login page par bhej deta hai.
"""

import streamlit as st


def require_login(message: str = "Pehle login karein."):
    if "token" not in st.session_state or st.session_state.token is None:
        st.session_state.flash_message = message
        st.switch_page("portal/1_login.py")
        st.stop()
