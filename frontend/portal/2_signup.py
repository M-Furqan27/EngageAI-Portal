"""
frontend/portal/2_signup.py

EngageAI — Professional Signup Page

Signup creates:
- Organization shell
- Owner account

Remaining organization details are completed
during the onboarding process after login.
"""

import streamlit as st

from utils import api_client
from utils.theme import inject_custom_css


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Create Account | EngageAI",
    page_icon="✨",
    layout="centered",
)


# ============================================================
# GLOBAL THEME
# ============================================================

inject_custom_css()


# ============================================================
# COUNTRY CODES
# ============================================================

COUNTRY_CODES = [
    ("+92", "Pakistan"),
    ("+91", "India"),
    ("+880", "Bangladesh"),
    ("+971", "United Arab Emirates"),
    ("+966", "Saudi Arabia"),
    ("+1", "United States/Canada"),
    ("+44", "United Kingdom"),
    ("+61", "Australia"),
    ("+49", "Germany"),
    ("+33", "France"),
    ("+86", "China"),
    ("+81", "Japan"),
    ("+90", "Turkey"),
    ("+974", "Qatar"),
    ("+965", "Kuwait"),
    ("+968", "Oman"),
    ("+973", "Bahrain"),
    ("+60", "Malaysia"),
    ("+62", "Indonesia"),
    ("+94", "Sri Lanka"),
    ("+977", "Nepal"),
    ("+93", "Afghanistan"),
    ("+20", "Egypt"),
    ("+27", "South Africa"),
    ("+234", "Nigeria"),
]

CODE_LABELS = [
    f"{code}  {country}"
    for code, country in COUNTRY_CODES
]


# ============================================================
# SIGNUP-SPECIFIC STYLING
# ============================================================

st.markdown(
    """
<style>

.signup-container {
    max-width: 680px;
    margin: 0 auto;
}

/* Brand */

.signup-brand {
    text-align: center;
    padding-top: 1rem;
    margin-bottom: 1.8rem;
}

.signup-logo {
    width: 52px;
    height: 52px;
    margin: 0 auto 0.8rem auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 15px;

    background: linear-gradient(
        135deg,
        #FF4B3E,
        #E63E33
    );

    color: white;
    font-size: 22px;
    font-weight: 800;

    box-shadow:
        0 10px 28px rgba(255, 75, 62, 0.25);
}

.signup-brand-name {
    color: #F5F7FA;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.signup-brand-subtitle {
    color: #737D8C;
    font-size: 0.78rem;
    margin-top: 0.2rem;
}


/* Header */

.signup-header {
    text-align: center;
    margin-bottom: 1.6rem;
}

.signup-title {
    color: #F5F7FA;
    font-size: 1.75rem;
    font-weight: 750;
    letter-spacing: -0.035em;
    margin-bottom: 0.35rem;
}

.signup-description {
    color: #858E9C;
    font-size: 0.88rem;
    line-height: 1.55;
    max-width: 540px;
    margin: 0 auto;
}


/* Section */

.signup-section-title {
    color: #F5F7FA;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 0.25rem;
    margin-bottom: 0.15rem;
}

.signup-section-description {
    color: #737D8C;
    font-size: 0.78rem;
    margin-bottom: 0.9rem;
}


/* Form card */

.signup-card {
    background:
        linear-gradient(
            145deg,
            rgba(22, 29, 39, 0.96),
            rgba(14, 19, 26, 0.96)
        );

    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;

    padding: 1.6rem;

    box-shadow:
        0 18px 45px rgba(0, 0, 0, 0.22);
}


/* Bottom */

.signup-login-text {
    text-align: center;
    color: #737D8C;
    font-size: 0.82rem;
    margin-top: 1.4rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PHONE INPUT
# ============================================================

def phone_input(label_prefix: str, key_prefix: str):

    col1, col2 = st.columns([1.15, 2])

    with col1:
        code_label = st.selectbox(
            f"{label_prefix} code *",
            CODE_LABELS,
            key=f"{key_prefix}_code",
        )

    with col2:
        number = st.text_input(
            f"{label_prefix} number *",
            placeholder="300 1234567",
            key=f"{key_prefix}_number",
        )

    code = code_label.split(" ")[0]

    combined = (
        f"{code} {number}".strip()
        if number
        else ""
    )

    return combined, number


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
<div class="signup-container">

    <div class="signup-brand">

        <div class="signup-logo">
            E
        </div>

        <div class="signup-brand-name">
            EngageAI
        </div>

        <div class="signup-brand-subtitle">
            Intelligent business communication
        </div>

    </div>

    <div class="signup-header">

        <div class="signup-title">
            Create your account
        </div>

        <div class="signup-description">
            Start your business workspace in a few simple steps.
            Your remaining organization details can be completed
            after your first login.
        </div>

    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIGNUP CARD
# ============================================================

st.markdown(
    '<div class="signup-card">',
    unsafe_allow_html=True,
)


# ============================================================
# SIGNUP FORM
# ============================================================

with st.form("signup_form"):

    # --------------------------------------------------------
    # ORGANIZATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="signup-section-title">'
        '🏢 Organization'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="signup-section-description">'
        'Start with the basic identity of your organization.'
        '</div>',
        unsafe_allow_html=True,
    )

    organization_name = st.text_input(
        "Organization name *",
        placeholder="e.g. Sindh Furniture Co.",
    )

    st.divider()

    # --------------------------------------------------------
    # OWNER ACCOUNT
    # --------------------------------------------------------

    st.markdown(
        '<div class="signup-section-title">'
        '👤 Owner account'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="signup-section-description">'
        'These credentials will be used to access your EngageAI portal.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First name *",
            placeholder="Khalil",
        )

    with col2:
        last_name = st.text_input(
            "Last name *",
            placeholder="Ali",
        )

    email = st.text_input(
        "Your login email *",
        placeholder="you@company.com",
    )

    phone, phone_number = phone_input(
        "Your phone",
        "owner_phone",
    )

    col1, col2 = st.columns(2)

    with col1:
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Create a password",
        )

    with col2:
        confirm_password = st.text_input(
            "Confirm password *",
            type="password",
            placeholder="Repeat your password",
        )

    st.markdown(
        "<div style='height:0.35rem'></div>",
        unsafe_allow_html=True,
    )

    submitted = st.form_submit_button(
        "Create account →",
        type="primary",
        use_container_width=True,
    )


# Close card
st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIGNUP LOGIC
# ============================================================

if submitted:

    required = [
        organization_name,
        first_name,
        last_name,
        email,
        phone_number,
        password,
    ]

    # --------------------------------------------------------
    # REQUIRED FIELDS
    # --------------------------------------------------------

    if not all(required):

        st.error(
            "Please complete all required (*) fields."
        )

    # --------------------------------------------------------
    # PASSWORD MATCH
    # --------------------------------------------------------

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    else:

        payload = {
            "organization_name": organization_name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "password": password,
        }

        try:

            api_client.register_organization_and_owner(
                payload
            )

            # ------------------------------------------------
            # IMPORTANT:
            # No auto-login.
            # User must login manually.
            # ------------------------------------------------

            st.success(
                f"'{organization_name}' has been created successfully!"
            )

            st.info(
                "Your account is ready. "
                "Please log in to continue your setup."
            )

            st.switch_page(
                "portal/1_login.py"
            )

        except Exception as e:

            st.error(
                f"Signup failed. ({e})"
            )


# ============================================================
# LOGIN LINK
# ============================================================

st.markdown(
    '<div class="signup-login-text">'
    'Already have an EngageAI account?'
    '</div>',
    unsafe_allow_html=True,
)


login_col = st.columns([1, 2, 1])[1]

with login_col:

    if st.button(
        "← Back to login",
        use_container_width=True,
    ):
        st.switch_page(
            "portal/1_login.py"
        )