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
# SIGNUP PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 980px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    div[data-testid="stForm"] {
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        background: rgba(18, 24, 32, 0.72);
        padding: 1.6rem;
    }

    div[data-baseweb="input"],
    div[data-baseweb="select"],
    textarea {
        border-radius: 9px !important;
    }

    button[kind="primaryFormSubmit"] {
        min-height: 46px;
        border-radius: 9px !important;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COUNTRY CODES
# ============================================================

COUNTRY_CODES = [
    ("+92", "Pakistan"),
    ("+91", "India"),
    ("+880", "Bangladesh"),
    ("+971", "United Arab Emirates"),
    ("+966", "Saudi Arabia"),
    ("+1", "United States / Canada"),
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
# BRAND
# ============================================================

st.markdown("## ✨ EngageAI")

st.caption(
    "Intelligent business communication"
)

st.write("")


# ============================================================
# HEADER
# ============================================================

st.title("Create your account")

st.caption(
    "Set up your business workspace in a few simple steps. "
    "You can complete the remaining business details "
    "after your first login."
)

st.divider()


# ============================================================
# SIGNUP FORM
# ============================================================

with st.form("signup_form"):

    # ========================================================
    # ORGANIZATION
    # ========================================================

    st.subheader("🏢 Your organization")

    st.caption(
        "Start with the basic identity of your organization."
    )

    organization_name = st.text_input(
        "Organization name *",
        placeholder="e.g. Sindh Furniture Co.",
    )


    # ========================================================
    # OWNER ACCOUNT
    # ========================================================

    st.divider()

    st.subheader("👤 Owner account")

    st.caption(
        "These credentials will be used to access your EngageAI portal."
    )


    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email = st.text_input(
        "Your login email *",
        placeholder="you@company.com",
    )


    # --------------------------------------------------------
    # PHONE
    # --------------------------------------------------------

    phone_col1, phone_col2 = st.columns(
        [1.15, 2]
    )

    with phone_col1:

        code_label = st.selectbox(
            "Country code *",
            CODE_LABELS,
            index=0,
        )

    with phone_col2:

        phone_number = st.text_input(
            "Phone number *",
            placeholder="300 1234567",
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


    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    st.write("")

    submitted = st.form_submit_button(
        "Create account →",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# SIGNUP LOGIC
# ============================================================

if submitted:

    # --------------------------------------------------------
    # PHONE
    # --------------------------------------------------------

    code = code_label.split(" ")[0]

    phone = (
        f"{code} {phone_number}".strip()
        if phone_number
        else ""
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not organization_name.strip():

        st.error(
            "Please enter your organization name."
        )

    elif not first_name.strip():

        st.error(
            "Please enter your first name."
        )

    elif not last_name.strip():

        st.error(
            "Please enter your last name."
        )

    elif not email.strip():

        st.error(
            "Please enter your email."
        )

    elif not phone_number.strip():

        st.error(
            "Please enter your phone number."
        )

    elif not password:

        st.error(
            "Please create a password."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    else:

        payload = {
            "organization_name": organization_name.strip(),
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": email.strip(),
            "phone": phone,
            "password": password,
        }

        try:

            api_client.register_organization_and_owner(
                payload
            )

            st.success(
                f"'{organization_name}' has been created successfully!"
            )

            st.info(
                "Your account is ready. Please log in "
                "to continue your setup."
            )

            st.switch_page(
                "portal/1_login.py"
            )

        except Exception as e:

            st.error(
                f"Signup failed. ({e})"
            )


# ============================================================
# LOGIN FOOTER
# ============================================================

st.divider()

st.caption(
    "Already have an EngageAI account?"
)

if st.button(
    "← Back to login",
    use_container_width=True,
):

    st.switch_page(
        "portal/1_login.py"
    )