"""
frontend/portal/0_onboarding.py

Onboarding wizard — 3 steps (Organization → Representatives → Knowledge Base).
Har step complete hone par, agla step khud-ba-khud khulta hai.
"""

import time
import streamlit as st
from utils import api_client
from utils.theme import inject_custom_css
from utils.auth import require_login
from utils.validators import (
    is_valid_email,
    is_required,
    validate_phone,
    validate_min_length,
    normalize_website,
    is_valid_website,
)

inject_custom_css()

st.set_page_config(page_title="EngageAI Portal", page_icon="👥", layout="wide")

require_login()

try:
    org = api_client.get_organization_profile()
    if org.get("onboarding_completed"):
        st.switch_page("portal/3_dashboard.py")
except Exception as e:
    st.error(f"We couldn't load your organization details. ({e})")
    st.stop()

if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 1

st.title("👋 Welcome! Let's set up your business.")
st.caption(f"Step {st.session_state.onboarding_step} of 3")
st.progress(st.session_state.onboarding_step / 3)

BUSINESS_TYPES = ["Retail", "Healthcare", "Education", "Services", "Other"]
COUNTRIES = [
    "Pakistan", "India", "Bangladesh", "United Arab Emirates", "Saudi Arabia",
    "United States", "United Kingdom", "Canada", "Australia", "Germany",
    "France", "China", "Japan", "Turkey", "Qatar", "Kuwait", "Oman",
    "Bahrain", "Malaysia", "Indonesia", "Sri Lanka", "Nepal", "Afghanistan",
    "Egypt", "South Africa", "Nigeria", "Other",
]

# ============================================================
# STEP 1 — ORGANIZATION
# ============================================================
if st.session_state.onboarding_step == 1:
    st.subheader("🏢 Step 1: Complete your business profile")

    with st.form("onboarding_org_form"):
        current_business = org.get("business_type", "Other")
        business_type = st.selectbox(
            "Business type *", BUSINESS_TYPES,
            index=BUSINESS_TYPES.index(current_business) if current_business in BUSINESS_TYPES else 0,
        )
        website = st.text_input("Website *", value=org.get("website") or "", placeholder="https://yourbusiness.com")
        business_email = st.text_input("Business email *", value=org.get("business_email") or "")
        business_phone = st.text_input("Business phone *", value=org.get("business_phone") or "")

        current_country = org.get("country", "Pakistan")
        country = st.selectbox(
            "Country *", COUNTRIES,
            index=COUNTRIES.index(current_country) if current_country in COUNTRIES else 0,
        )
        address = st.text_area("Address", value=org.get("address") or "")
        description = st.text_area("Description", value=org.get("description") or "")

        save_org = st.form_submit_button("Save & Continue →", type="primary", use_container_width=True)

    if save_org:
        errors = []
        if not is_required(website):
            errors.append("Website is required.")
        elif not is_valid_website(normalize_website(website)):
            errors.append("Please enter a valid website (e.g. www.yourbusiness.com).")

        if not is_required(business_email):
            errors.append("Business email is required.")
        elif not is_valid_email(business_email):
            errors.append("Please enter a valid business email address.")

        phone_ok, phone_msg = validate_phone(business_phone, country)
        if not phone_ok:
            errors.append(phone_msg)

        if errors:
            for err in errors:
                st.error(err)
        else:
            payload = {
                "business_type": business_type,
                "website": normalize_website(website),
                "business_email": business_email.strip().lower(),
                "business_phone": business_phone.strip(),
                "country": country,
                "address": address.strip(),
                "description": description.strip(),
            }
            try:
                api_client.update_organization_profile(payload)
                st.success("✅ Organization details saved. Moving to the next step...")
                time.sleep(1.2)
                st.session_state.onboarding_step = 2
                st.rerun()
            except Exception as e:
                st.error(f"We couldn't save your organization details. ({e})")

# ============================================================
# STEP 2 — REPRESENTATIVES
# ============================================================
elif st.session_state.onboarding_step == 2:
    st.subheader("🧑‍💼 Step 2: Add a company representative")
    st.caption("Add at least one representative who will handle customer meetings. You can add more later from your Profile page.")

    with st.form("onboarding_add_rep_form"):
        representative_name = st.text_input("Representative name *", placeholder="e.g. Ali Khan")
        service = st.text_input("Service / Department *", placeholder="e.g. Sales")
        service_description = st.text_area("Service description *", placeholder="Briefly describe what this representative handles...")
        company_email = st.text_input("Representative's email *", placeholder="representative@company.com")

        add_rep = st.form_submit_button("Add & Continue →", type="primary", use_container_width=True)

    if add_rep:
        errors = []
        if not is_required(representative_name):
            errors.append("Representative name is required.")
        else:
            ok, msg = validate_min_length(representative_name, 2, "Representative name")
            if not ok:
                errors.append(msg)

        if not is_required(service):
            errors.append("Service is required.")

        if not is_required(service_description):
            errors.append("Service description is required.")
        else:
            ok, msg = validate_min_length(service_description, 10, "Service description")
            if not ok:
                errors.append(msg)

        if not is_required(company_email):
            errors.append("Representative's email is required.")
        elif not is_valid_email(company_email):
            errors.append("Please enter a valid email address.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            payload = {
                "representative_name": representative_name.strip(),
                "service": service.strip(),
                "service_description": service_description.strip(),
                "company_email": company_email.strip().lower(),
            }
            try:
                api_client.create_representative(payload)
                st.success("✅ Representative added successfully. Moving to the next step...")
                time.sleep(1.2)
                st.session_state.onboarding_step = 3
                st.rerun()
            except Exception as e:
                st.error(f"We couldn't add this representative. ({e})")

    st.divider()
    if st.button("← Back"):
        st.session_state.onboarding_step = 1
        st.rerun()

# ============================================================
# STEP 3 — KNOWLEDGE BASE
# ============================================================
elif st.session_state.onboarding_step == 3:
    st.subheader("📚 Step 3: Teach your AI about your business")

    kb_type = st.radio("Source type", ["Text", "PDF", "URL"], horizontal=True)

    if kb_type == "Text":
        text_content = st.text_area("Paste content")
        if st.button("Upload Text →", type="primary"):
            if not is_required(text_content):
                st.error("Please enter some text before uploading.")
            else:
                ok, msg = validate_min_length(text_content, 20, "Text content")
                if not ok:
                    st.error(msg)
                else:
                    try:
                        api_client.upload_knowledge_text(text_content.strip())
                        st.success("✅ Text uploaded successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Upload failed. ({e})")

    elif kb_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if st.button("Upload PDF →", type="primary"):
            if not pdf_file:
                st.error("Please select a PDF file before uploading.")
            else:
                try:
                    api_client.upload_knowledge_pdf(pdf_file)
                    st.success("✅ PDF uploaded successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload failed. ({e})")

    elif kb_type == "URL":
        url = st.text_input("Website URL", placeholder="https://yourbusiness.com/faq")
        if st.button("Upload URL →", type="primary"):
            normalized_url = normalize_website(url)
            if not is_required(url):
                st.error("Please enter a website URL before uploading.")
            elif not is_valid_website(normalized_url):
                st.error("Please enter a valid URL (e.g. https://yourbusiness.com/faq).")
            else:
                try:
                    api_client.upload_knowledge_url(normalized_url)
                    st.success("✅ URL added successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload failed. ({e})")

    st.divider()

    try:
        docs = api_client.list_knowledge()
    except Exception as e:
        docs = []
        st.error(f"We couldn't load your knowledge sources. ({e})")

    if docs:
        st.caption(f"{len(docs)} source(s) added:")
        for doc in docs:
            with st.container(border=True):
                source_type = doc.get("source_type", "Unknown") if isinstance(doc, dict) else "File"
                status = doc.get("processing_status", "Completed") if isinstance(doc, dict) else "Completed"
                source_name = doc.get("source_name", doc.get("source_path", "")) if isinstance(doc, dict) else doc
                st.markdown(f"**{source_type}** — {status}")
                if source_name:
                    st.caption(source_name)
    else:
        st.info("No knowledge sources added yet.")

    st.divider()
    if st.button("← Back"):
        st.session_state.onboarding_step = 2
        st.rerun()

# ============================================================
# FINISH SETUP (Step 3 pe hi available)
# ============================================================
if st.session_state.onboarding_step == 3:
    st.divider()
    if st.button("✅ Finish Setup & Go to Dashboard →", type="primary", use_container_width=True):
        try:
            api_client.complete_onboarding()
            st.session_state.onboarding_completed = True
            st.success("✅ Setup complete! Redirecting to your dashboard...")
            time.sleep(1.2)
            st.rerun()
        except Exception as e:
            st.error(f"We couldn't complete your setup. ({e})")