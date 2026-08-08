import streamlit as st

from utils import api_client
from utils.theme import inject_custom_css

inject_custom_css()


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# LOGIN PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Remove unnecessary top spacing */
    .block-container {
        max-width: 1180px;
        padding-top: 3rem;
    }

    /* Login layout */
    .login-wrapper {
        max-width: 460px;
        margin: 3rem auto 0 auto;
    }

    /* Brand */
    .login-brand {
        text-align: center;
        margin-bottom: 2rem;
    }

    .brand-icon {
        width: 54px;
        height: 54px;
        margin: 0 auto 1rem auto;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 16px;

        background:
            linear-gradient(
                135deg,
                #FF4B3E,
                #E63E33
            );

        color: #FFFFFF;
        font-size: 23px;
        font-weight: 800;

        box-shadow:
            0 12px 30px rgba(255, 75, 62, 0.25);
    }

    .brand-name {
        color: #F5F7FA;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .brand-tagline {
        color: #737D8C;
        font-size: 0.82rem;
        margin-top: 0.25rem;
    }

    /* Login card */
    .login-card {
        background:
            linear-gradient(
                145deg,
                rgba(22, 29, 39, 0.98),
                rgba(14, 19, 26, 0.98)
            );

        border:
            1px solid rgba(255, 255, 255, 0.08);

        border-radius: 20px;

        padding: 2rem;

        box-shadow:
            0 20px 55px rgba(0, 0, 0, 0.30);
    }

    .login-heading {
        color: #F5F7FA;
        font-size: 1.55rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .login-description {
        color: #858E9C;
        font-size: 0.88rem;
        margin-bottom: 1.3rem;
    }

    /* Bottom signup */
    .signup-text {
        text-align: center;
        color: #737D8C;
        font-size: 0.84rem;
        margin-top: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FLASH MESSAGE
# ============================================================

_flash = st.session_state.pop("flash_message", None)


# ============================================================
# BRAND
# ============================================================

st.markdown(
    """
    <div class="login-wrapper">

        <div class="login-brand">

            <div class="brand-icon">
                E
            </div>

            <div class="brand-name">
                EngageAI
            </div>

            <div class="brand-tagline">
                Intelligent business communication
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FLASH MESSAGE
# ============================================================

if _flash:
    st.warning(f"🔒 {_flash}")


# ============================================================
# LOGIN CARD
# ============================================================

st.markdown(
    """
    <div class="login-wrapper">

        <div class="login-card">

            <div class="login-heading">
                Welcome back
            </div>

            <div class="login-description">
                Sign in to access your EngageAI business portal.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN FORM
# ============================================================

with st.container():

    st.markdown(
        '<div class="login-wrapper">',
        unsafe_allow_html=True,
    )

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

        st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "Log in →",
            type="primary",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# LOGIN LOGIC — ORIGINAL FLOW PRESERVED
# ============================================================

if submitted:

    if not email or not password:

        st.error(
            "Email aur password dono zaroori hain."
        )

    else:

        try:

            data = api_client.login(
                email,
                password,
            )

            st.session_state.token = data["token"]
            st.session_state.user = data["user"]

            st.success(
                f"Welcome back, {data['user']['first_name']}!"
            )

            # Check onboarding status
            org = api_client.get_organization_profile()

            st.session_state.onboarding_completed = bool(
                org.get("onboarding_completed")
            )

            # Re-run app so navigation updates
            st.rerun()

        except Exception as e:

            st.error(
                f"Login fail ho gaya — credentials check karein. ({e})"
            )


# ============================================================
# SIGNUP
# ============================================================

st.markdown(
    """
    <div class="login-wrapper">
        <div class="signup-text">
            Don't have an EngageAI account yet?
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


signup_col = st.columns([1, 2, 1])[1]

with signup_col:

    if st.button(
        "Create an account",
        use_container_width=True,
    ):
        st.switch_page(
            "portal/2_signup.py"
        )