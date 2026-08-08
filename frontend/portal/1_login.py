"""
frontend/portal/1_login.py

REPLACE the existing file. Login ke baad organization profile check karta
hai — agar onboarding abhi complete nahi hui to wizard dikhata hai,
warna seedha normal dashboard.
"""

import streamlit as st
from utils import api_client

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.user = None

st.title("🔑 Log in")
st.caption("Apne organization ke dashboard mein login karein.")

with st.form("login_form"):
    email = st.text_input("Work email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Log in →", type="primary")

if submitted:
    if not email or not password:
        st.error("Email aur password dono zaroori hain.")
    else:
        try:
            data = api_client.login(email, password)
            st.session_state.token = data["token"]
            st.session_state.user = data["user"]
            st.success(f"Welcome back, {data['user']['first_name']}!")

            # Onboarding complete hui ya nahi, check karo
            org = api_client.get_organization_profile()
            st.session_state.onboarding_completed = bool(org.get("onboarding_completed"))

            if st.session_state.onboarding_completed:
                st.switch_page("portal/3_dashboard.py")
            else:
                st.switch_page("portal/0_onboarding.py")
        except Exception as e:
            st.error(f"Login fail ho gaya — credentials check karein. ({e})")

st.divider()
st.write("Naye hain?")
if st.button("Create an account"):
    st.switch_page("portal/2_signup.py")