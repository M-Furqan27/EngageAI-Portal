"""
frontend/portal/2_signup.py

REPLACE the existing file. Ab do-step wizard nahi — ek hi simple form:
sirf Organization NAME (poori profile nahi) + Owner account.
Baaki organization details (business type, website, phone, country, ...)
pehli baar login karne pe onboarding wizard mein bharni hain.
"""

import streamlit as st
from utils import api_client

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


def phone_input(label_prefix: str, key_prefix: str):
    c1, c2 = st.columns([1.3, 2])
    code_label = c1.selectbox(f"{label_prefix} code *", CODE_LABELS, key=f"{key_prefix}_code")
    number = c2.text_input(f"{label_prefix} number *", key=f"{key_prefix}_number")
    code = code_label.split(" ")[0]
    combined = f"{code} {number}".strip() if number else ""
    return combined, number


st.title("🆕 Create your account")
st.caption("Bas apna organization ka naam aur apna account bana lo — baaki details pehli login ke baad complete karoge.")

with st.form("signup_form"):
    organization_name = st.text_input("Organization name *", placeholder="e.g. Sindh Furniture Co.")

    st.divider()
    st.subheader("Your account (Owner)")

    col1, col2 = st.columns(2)
    first_name = col1.text_input("First name *")
    last_name = col2.text_input("Last name *")
    email = st.text_input("Your login email *")

    phone, phone_number = phone_input("Your phone", "owner_phone")

    password = st.text_input("Password *", type="password")
    confirm_password = st.text_input("Confirm password *", type="password")

    submitted = st.form_submit_button("Create account →", type="primary", use_container_width=True)

if submitted:
    required = [organization_name, first_name, last_name, email, phone_number, password]
    if not all(required):
        st.error("Sab required (*) fields bharna zaroori hai.")
    elif password != confirm_password:
        st.error("Password match nahi kar raha.")
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
            data = api_client.register_organization_and_owner(payload)
            st.session_state.token = data["token"]
            st.session_state.user = data["user"]
            st.success(f"'{organization_name}' create ho gayi! Ab login karke apni profile complete karein.")
            st.switch_page("portal/1_login.py")
        except Exception as e:
            st.error(f"Signup fail ho gaya. ({e})")

st.divider()
if st.button("Already have an account? Log in"):
    st.switch_page("portal/1_login.py")