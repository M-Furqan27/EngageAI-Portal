import streamlit as st
from utils import api_client

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()

st.title("🏢 Profile")

tab1, tab2 = st.tabs(["🏢 Organization", "👤 My Account"])

# ============================================================
# TAB 1 — Organization profile
# ============================================================
with tab1:
    try:
        org = api_client.get_organization_profile()
    except Exception as e:
        st.error(f"Organization profile load nahi ho saka. ({e})")
        org = None

    if org:
        with st.form("org_profile_form"):
            organization_name = st.text_input("Organization name", value=org.get("organization_name", ""))
            business_type = st.selectbox(
                "Business type",
                ["Retail", "Healthcare", "Education", "Services", "Other"],
                index=["Retail", "Healthcare", "Education", "Services", "Other"].index(org["business_type"])
                if org.get("business_type") in ["Retail", "Healthcare", "Education", "Services", "Other"] else 0,
            )
            website = st.text_input("Website", value=org.get("website", ""))
            business_email = st.text_input("Business email", value=org.get("business_email", ""))
            business_phone = st.text_input("Business phone", value=org.get("business_phone", ""))
            country = st.text_input("Country", value=org.get("country", ""))
            address = st.text_area("Address", value=org.get("address") or "")
            description = st.text_area("Description", value=org.get("description") or "")

            org_save = st.form_submit_button("Save Organization →", type="primary")

        if org_save:
            payload = {
                "organization_name": organization_name,
                "business_type": business_type,
                "website": website,
                "business_email": business_email,
                "business_phone": business_phone,
                "country": country,
                "address": address,
                "description": description,
            }
            try:
                api_client.update_organization_profile(payload)
                st.success("Organization profile update ho gayi!")
                st.rerun()
            except Exception as e:
                st.error(f"Update fail ho gaya. ({e})")

# ============================================================
# TAB 2 — My account (logged-in user)
# ============================================================
with tab2:
    try:
        me = api_client.get_my_user_profile()
    except Exception as e:
        st.error(f"Profile load nahi ho saka. ({e})")
        me = None

    if me:
        st.caption(f"Role: **{me['role']}** · Status: **{me['status']}**")

        with st.form("user_profile_form"):
            first_name = st.text_input("First name", value=me.get("first_name", ""))
            last_name = st.text_input("Last name", value=me.get("last_name", ""))
            phone = st.text_input("Phone", value=me.get("phone", ""))
            st.text_input("Email (change nahi ho sakta)", value=me.get("email", ""), disabled=True)

            user_save = st.form_submit_button("Save My Profile →", type="primary")

        if user_save:
            payload = {"first_name": first_name, "last_name": last_name, "phone": phone}
            try:
                updated = api_client.update_my_user_profile(payload)
                st.session_state.user = updated
                st.success("Profile update ho gayi!")
                st.rerun()
            except Exception as e:
                st.error(f"Update fail ho gaya. ({e})")