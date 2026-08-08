"""
EngageAI — Professional Login Page
"""

import streamlit as st

from utils import api_client
from utils.theme import inject_custom_css


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Login | EngageAI",
    page_icon="🔑",
    layout="centered",
)


# ============================================================
# GLOBAL THEME
# ============================================================

inject_custom_css()


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# HEADER
# ============================================================

st.markdown("## 🔑 EngageAI")

st.caption(
    "Intelligent business communication"
)

st.title("Welcome back")

st.write(
    "Sign in to access your EngageAI business portal."
)


# ============================================================
# FLASH MESSAGE
# ============================================================

_flash = st.session_state.pop(
    "flash_message",
    None,
)

if _flash:
    st.warning(
        f"🔒 {_flash}"
    )


# ============================================================
# LOGIN FORM
# ============================================================

with st.form("login_form"):

    email = st.text_input(
        "Work email",
        placeholder="you@company.com",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
    )

    st.write("")

    submitted = st.form_submit_button(
        "Log in →",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# LOGIN LOGIC
# ============================================================

if submitted:

    if not email.strip() or not password:

        st.error(
            "Email aur password dono zaroori hain."
        )

    else:

        try:

            data = api_client.login(
                email.strip(),
                password,
            )

            # ------------------------------------------------
            # Save authentication state
            # ------------------------------------------------

            st.session_state.token = data["token"]

            st.session_state.user = data["user"]

            # ------------------------------------------------
            # Check onboarding status
            # ------------------------------------------------

            org = api_client.get_organization_profile()

            st.session_state.onboarding_completed = bool(
                org.get("onboarding_completed")
            )

            # ------------------------------------------------
            # Re-run app
            #
            # app.py will decide whether the user should see
            # onboarding or dashboard.
            # ------------------------------------------------

            st.rerun()

        except Exception as e:

            st.error(
                f"Login fail ho gaya — credentials check karein. ({e})"
            )


# ============================================================
# SIGNUP
# ============================================================

st.divider()

st.caption(
    "Don't have an EngageAI account yet?"
)

if st.button(
    "Create an account",
    use_container_width=True,
):

    st.switch_page(
        "portal/2_signup.py"
    )