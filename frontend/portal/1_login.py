"""
frontend/portal/1_login.py
"""

import time
import streamlit as st
from utils import api_client
from utils.theme import inject_custom_css
from utils.validators import is_valid_email, is_required

inject_custom_css()

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.user = None

st.title("🔑 Log in")

_flash = st.session_state.pop("flash_message", None)
if _flash:
    st.warning(f"🔒 {_flash}")

st.caption("Log in to access your organization's dashboard.")

with st.form("login_form"):
    email = st.text_input("Work email *", placeholder="you@company.com")
    password = st.text_input("Password *", type="password")
    submitted = st.form_submit_button("Log in →", type="primary")

if submitted:
    errors = []

    if not is_required(email):
        errors.append("Please enter your email address.")
    elif not is_valid_email(email):
        errors.append("Please enter a valid email address (e.g. you@company.com).")

    if not is_required(password):
        errors.append("Please enter your password.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        try:
            data = api_client.login(email.strip().lower(), password)
            st.session_state.token = data["token"]
            st.session_state.user = data["user"]

            org = api_client.get_organization_profile()
            st.session_state.onboarding_completed = bool(org.get("onboarding_completed"))

            st.success(f"✅ Login successful. Welcome back, {data['user']['first_name']}!")
            time.sleep(1.2)
            st.rerun()
        except Exception as e:
            st.error(f"Login failed. Please check your email and password and try again. ({e})")

st.divider()
st.write("New here?")
if st.button("Create an account"):
    st.switch_page("portal/2_signup.py")