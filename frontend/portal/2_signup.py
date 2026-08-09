"""
frontend/portal/2_signup.py
"""

import time
import streamlit as st
from utils import api_client
from utils.theme import inject_custom_css
from utils.validators import is_valid_email, is_required, validate_phone, validate_password, validate_min_length

inject_custom_css()

COUNTRY_CODES = [
    ("+92", "Pakistan"), ("+91", "India"), ("+880", "Bangladesh"),
    ("+971", "United Arab Emirates"), ("+966", "Saudi Arabia"),
    ("+1", "United States/Canada"), ("+44", "United Kingdom"),
    ("+61", "Australia"), ("+49", "Germany"), ("+33", "France"),
    ("+86", "China"), ("+81", "Japan"), ("+90", "Turkey"),
    ("+974", "Qatar"), ("+965", "Kuwait"), ("+968", "Oman"),
    ("+973", "Bahrain"), ("+60", "Malaysia"), ("+62", "Indonesia"),
    ("+94", "Sri Lanka"), ("+977", "Nepal"), ("+93", "Afghanistan"),
    ("+20", "Egypt"), ("+27", "South Africa"), ("+234", "Nigeria"),
]
CODE_LABELS = [f"{code}  {name}" for code, name in COUNTRY_CODES]
CODE_TO_COUNTRY = {code: name for code, name in COUNTRY_CODES}


def phone_input(label_prefix: str, key_prefix: str):
    c1, c2 = st.columns([1.3, 2])
    code_label = c1.selectbox(f"{label_prefix} code *", CODE_LABELS, key=f"{key_prefix}_code")
    number = c2.text_input(f"{label_prefix} number *", key=f"{key_prefix}_number")
    code = code_label.split(" ")[0]
    country = CODE_TO_COUNTRY.get(code)
    combined = f"{code} {number}".strip() if number else ""
    return combined, number, country


st.title("🆕 Create your account")
st.caption("Set up your organization and owner account. You'll complete the rest of your business profile after your first login.")

# Signup successfully hone ke baad yahan rukte hain (redirect turant nahi karte)
if st.session_state.get("signup_success"):
    st.success("✅ Your account has been created successfully. Please log in to continue.")
    if st.button("Continue to Login →", type="primary", use_container_width=True):
        st.session_state.signup_success = False
        st.switch_page("portal/1_login.py")
    st.stop()

with st.form("signup_form"):
    organization_name = st.text_input("Organization name *", placeholder="e.g. Sindh Furniture Co.")

    st.divider()
    st.subheader("Your account (Owner)")

    col1, col2 = st.columns(2)
    first_name = col1.text_input("First name *")
    last_name = col2.text_input("Last name *")
    email = st.text_input("Your login email *", placeholder="you@company.com")

    phone, phone_number, phone_country = phone_input("Your phone", "owner_phone")

    password = st.text_input("Password *", type="password", help="Minimum 8 characters, at least one letter and one number.")
    confirm_password = st.text_input("Confirm password *", type="password")

    submitted = st.form_submit_button("Create account →", type="primary", use_container_width=True)

if submitted:
    errors = []

    if not is_required(organization_name):
        errors.append("Organization name is required.")
    else:
        ok, msg = validate_min_length(organization_name, 2, "Organization name")
        if not ok:
            errors.append(msg)

    if not is_required(first_name):
        errors.append("First name is required.")

    if not is_required(last_name):
        errors.append("Last name is required.")

    if not is_required(email):
        errors.append("Email address is required.")
    elif not is_valid_email(email):
        errors.append("Please enter a valid email address (e.g. you@company.com).")

    phone_ok, phone_msg = validate_phone(phone_number, phone_country)
    if not phone_ok:
        errors.append(phone_msg)

    pw_ok, pw_msg = validate_password(password, min_len=8)
    if not pw_ok:
        errors.append(pw_msg)

    if password != confirm_password:
        errors.append("Password and confirmation do not match.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        payload = {
            "organization_name": organization_name.strip(),
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": email.strip().lower(),
            "phone": phone,
            "password": password,
        }
        try:
            api_client.register_organization_and_owner(payload)
            st.success("✅ Your account has been created successfully. Redirecting to login...")
            time.sleep(1.5)
            st.switch_page("portal/1_login.py")
        except Exception as e:
            st.error(f"We couldn't create your account. Please try again. ({e})")

st.divider()
if st.button("Already have an account? Log in"):
    st.switch_page("portal/1_login.py")