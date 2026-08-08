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
    f"{code}  {name}"
    for code, name in COUNTRY_CODES
]


# ============================================================
# SIGNUP PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    .signup-page {
        max-width: 620px;
        margin: 1.5rem auto 3rem auto;
    }

    /* Brand */

    .signup-brand {
        text-align: center;
        margin-bottom: 1.7rem;
    }

    .signup-brand-icon {
        width: 52px;
        height: 52px;
        margin: 0 auto 0.9rem auto;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 15px;

        background:
            linear-gradient(
                135deg,
                #FF4B3E,
                #E63E33
            );

        color: #FFFFFF;
        font-size: 22px;
        font-weight: 800;

        box-shadow:
            0 12px 30px rgba(255, 75, 62, 0.24);
    }

    .signup-brand-name {
        color: #F5F7FA;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .signup-brand-caption {
        color: #737D8C;
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    /* Header */

    .signup-header {
        text-align: center;
        margin-bottom: 1.4rem;
    }

    .signup-title {
        color: #F5F7FA;
        font-size: 1.65rem;
        font-weight: 750;
        letter-spacing: -0.035em;
    }

    .signup-description {
        color: #858E9C;
        font-size: 0.88rem;
        margin-top: 0.35rem;
        line-height: 1.55;
    }

    /* Form section */

    .form-section {
        color: #F5F7FA;
        font-size: 0.98rem;
        font-weight: 700;
        margin-top: 0.35rem;
        margin-bottom: 0.7rem;
    }

    .form-section-caption {
        color: #737D8C;
        font-size: 0.78rem;
        margin-bottom: 0.9rem;
    }

    /* Footer */

    .signup-footer {
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
# BRAND
# ============================================================

st.markdown(
    """
<div class="signup-page">

    <div class="signup-brand">

        <div class="signup-brand-icon">
            E
        </div>

        <div class="signup-brand-name">
            EngageAI
        </div>

        <div class="signup-brand-caption">
            Intelligent business communication
        </div>

    </div>

    <div class="signup-header">

        <div class="signup-title">
            Create your account
        </div>

        <div class="signup-description">
            Start your business workspace in a few simple steps.
            You can complete the rest of your business profile
            after your first login.
        </div>

    </div>

</div>
""",
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
        '<div class="form-section">🏢 Your organization</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="form-section-caption">'
        'Tell us the name of your organization.'
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
        '<div class="form-section">👤 Owner account</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="form-section-caption">'
        'These details will be used to access your EngageAI portal.'
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
        "Work email *",
        placeholder="you@company.com",
    )

    # --------------------------------------------------------
    # PHONE
    # --------------------------------------------------------

    st.markdown(
        '<div style="height:0.2rem"></div>',
        unsafe_allow_html=True,
    )

    phone_col1, phone_col2 = st.columns([1.25, 2])

    with phone_col1:

        code_label = st.selectbox(
            "Country code *",
            CODE_LABELS,
        )

    with phone_col2:

        phone_number = st.text_input(
            "Phone number *",
            placeholder="300 1234567",
        )

    code = code_label.split(" ")[0]

    phone = (
        f"{code} {phone_number}".strip()
        if phone_number
        else ""
    )

    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    password_col1, password_col2 = st.columns(2)

    with password_col1:

        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Create a password",
        )

    with password_col2:

        confirm_password = st.text_input(
            "Confirm password *",
            type="password",
            placeholder="Repeat your password",
        )

    st.markdown(
        '<div style="height:0.35rem"></div>',
        unsafe_allow_html=True,
    )

    submitted = st.form_submit_button(
        "Create account →",
        type="primary",
        use_container_width=True,
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

    if not all(required):

        st.error(
            "Please complete all required (*) fields."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

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

            data = api_client.register_organization_and_owner(
                payload
            )

            # Do NOT auto-login.
            # User should login manually after signup.

            st.success(
                f"'{organization_name}' has been created successfully!"
            )

            st.info(
                "Your account is ready. Please log in to "
                "complete your business setup."
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
    '<div class="signup-footer">'
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