"""
frontend/portal/4_profile.py
"""

import time
import re
import streamlit as st
from utils import api_client
from utils.sidebar import render_account_sidebar
from utils.theme import inject_custom_css
from utils.auth import require_login

st.set_page_config(page_title="Profile", page_icon="🏢", layout="wide")
inject_custom_css()

require_login()
render_account_sidebar()

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

if "profile_edit_mode" not in st.session_state:
    st.session_state.profile_edit_mode = False

try:
    org = api_client.get_organization_profile()
except Exception as e:
    st.error(f"We couldn't load your profile. ({e})")
    st.stop()

# =========================
# HEADER — Edit button chota, right-aligned
# =========================
header_col, button_col = st.columns([6, 1])
with header_col:
    st.title("🏢 Profile")
    st.caption("Manage your organization setup.")
with button_col:
    st.write("")  # vertical spacing align karne ke liye
    if not st.session_state.profile_edit_mode:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.profile_edit_mode = True
            st.rerun()
    else:
        if st.button("✖ Cancel", use_container_width=True):
            st.session_state.profile_edit_mode = False
            st.rerun()

if st.session_state.profile_edit_mode:
    st.info("Edit mode is enabled. You can now update your organization, representatives, and knowledge base.")

# =========================
# ORGANIZATION SECTION
# =========================
st.divider()
st.subheader("🏢 Organization")

BUSINESS_TYPES = ["Retail", "Healthcare", "Education", "Services", "Other"]
COUNTRIES = [
    "Pakistan", "India", "Bangladesh", "United Arab Emirates", "Saudi Arabia",
    "United States", "United Kingdom", "Canada", "Australia", "Germany",
    "France", "China", "Japan", "Turkey", "Qatar", "Kuwait", "Oman",
    "Bahrain", "Malaysia", "Indonesia", "Sri Lanka", "Nepal", "Afghanistan",
    "Egypt", "South Africa", "Nigeria", "Other",
]

if not st.session_state.profile_edit_mode:
    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🏷️ Business Type**")
            st.markdown(f"<span style='color:#9AA3AE'>{org.get('business_type', '—')}</span>", unsafe_allow_html=True)
            st.markdown("&nbsp;", unsafe_allow_html=True)

            st.markdown("**🌐 Website**")
            website_val = org.get('website') or '—'
            st.markdown(f"<span style='color:#9AA3AE'>{website_val}</span>", unsafe_allow_html=True)
            st.markdown("&nbsp;", unsafe_allow_html=True)

            st.markdown("**📧 Business Email**")
            st.markdown(f"<span style='color:#9AA3AE'>{org.get('business_email') or '—'}</span>", unsafe_allow_html=True)

        with col2:
            st.markdown("**📞 Business Phone**")
            st.markdown(f"<span style='color:#9AA3AE'>{org.get('business_phone') or '—'}</span>", unsafe_allow_html=True)
            st.markdown("&nbsp;", unsafe_allow_html=True)

            st.markdown("**🌍 Country**")
            st.markdown(f"<span style='color:#9AA3AE'>{org.get('country') or '—'}</span>", unsafe_allow_html=True)
            st.markdown("&nbsp;", unsafe_allow_html=True)

            st.markdown("**📍 Address**")
            st.markdown(f"<span style='color:#9AA3AE'>{org.get('address') or '—'}</span>", unsafe_allow_html=True)

        st.divider()
        st.markdown("**📝 Description**")
        st.markdown(f"<span style='color:#9AA3AE'>{org.get('description') or '—'}</span>", unsafe_allow_html=True)

else:
    with st.form("profile_organization_form"):
        current_business = org.get("business_type", "Other")
        business_type = st.selectbox(
            "Business type *", BUSINESS_TYPES,
            index=BUSINESS_TYPES.index(current_business) if current_business in BUSINESS_TYPES else 0,
        )
        website = st.text_input("Website *", value=org.get("website", ""))
        business_email = st.text_input("Business email *", value=org.get("business_email", ""))
        business_phone = st.text_input("Business phone *", value=org.get("business_phone", ""))

        current_country = org.get("country", "Pakistan")
        country = st.selectbox(
            "Country *", COUNTRIES,
            index=COUNTRIES.index(current_country) if current_country in COUNTRIES else 0,
        )
        address = st.text_area("Address", value=org.get("address", ""))
        description = st.text_area("Description", value=org.get("description", ""))

        save_org = st.form_submit_button("Save Organization", type="primary")

    if save_org:
        errors = []
        if not website.strip():
            errors.append("Website is required.")
        if not business_email.strip():
            errors.append("Business email is required.")
        elif not EMAIL_PATTERN.match(business_email.strip()):
            errors.append("Please enter a valid business email address.")
        if not business_phone.strip():
            errors.append("Business phone is required.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            payload = {
                "business_type": business_type,
                "website": website.strip(),
                "business_email": business_email.strip().lower(),
                "business_phone": business_phone.strip(),
                "country": country,
                "address": address.strip(),
                "description": description.strip(),
            }
            try:
                api_client.update_organization_profile(payload)
                st.success("✅ Organization details updated successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"We couldn't save your changes. ({e})")

# =========================
# REPRESENTATIVES SECTION
# =========================
st.divider()
st.subheader("🧑‍💼 Representative Management")
st.caption("Add and manage company representatives.")

if st.session_state.profile_edit_mode:
    with st.expander("➕ Add Representative", expanded=False):
        with st.form("profile_add_rep_form"):
            rep_name = st.text_input("Representative name *", placeholder="e.g. Ali Khan")
            rep_service = st.text_input("Service / Department *", placeholder="e.g. Sales")
            rep_desc = st.text_area("Service description *", placeholder="Briefly describe what this representative handles...")
            rep_email = st.text_input("Representative's email *", placeholder="representative@company.com")

            add_rep = st.form_submit_button("Add Representative", type="primary")

        if add_rep:
            errors = []
            if not rep_name.strip():
                errors.append("Representative name is required.")
            if not rep_service.strip():
                errors.append("Service is required.")
            if not rep_desc.strip():
                errors.append("Service description is required.")
            if not rep_email.strip():
                errors.append("Representative's email is required.")
            elif not EMAIL_PATTERN.match(rep_email.strip()):
                errors.append("Please enter a valid email address.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                payload = {
                    "representative_name": rep_name.strip(),
                    "service": rep_service.strip(),
                    "service_description": rep_desc.strip(),
                    "company_email": rep_email.strip().lower(),
                }
                try:
                    api_client.create_representative(payload)
                    st.success("✅ Representative added successfully.")
                    time.sleep(1.0)
                    st.rerun()
                except Exception as e:
                    st.error(f"We couldn't add this representative. ({e})")

try:
    representatives = api_client.list_representatives()
except Exception as e:
    representatives = []
    st.error(f"We couldn't load your representatives. ({e})")

if not representatives:
    st.info("No representatives added yet.")
else:
    for representative in representatives:
        representative_id = representative.get("representative_id")

        try:
            calendar_status = api_client.check_calendar_status(representative_id)
        except Exception:
            calendar_status = {"connection_status": "Unknown"}

        connection_status = calendar_status.get("connection_status", "Unknown")
        invitation_status = representative.get("invitation_status", "Pending")

        with st.container(border=True):
            top_col1, top_col2, top_col3 = st.columns([3, 2, 2])
            with top_col1:
                st.markdown(f"### 🧑‍💼 {representative.get('representative_name', '-')}")
                st.caption(f"📧 {representative.get('company_email', '-')}")
            with top_col2:
                st.markdown("**Service**")
                st.markdown(f"<span style='color:#9AA3AE'>{representative.get('service', '-')}</span>", unsafe_allow_html=True)
            with top_col3:
                badge_col1, badge_col2 = st.columns(2)
                with badge_col1:
                    st.markdown("**Invitation**")
                    if invitation_status == "Sent":
                        st.success("✉️ Sent")
                    elif invitation_status == "Accepted":
                        st.success("✅ Accepted")
                    elif invitation_status == "Email Failed":
                        st.error("⚠️ Failed")
                    else:
                        st.warning(f"⏳ {invitation_status}")
                with badge_col2:
                    st.markdown("**Calendar**")
                    if connection_status == "Connected":
                        st.success("🟢 Connected")
                    elif connection_status == "Revoked":
                        st.error("🔴 Revoked")
                    else:
                        st.warning("⚪ Not Connected")

            if representative.get("service_description"):
                st.markdown("**Description**")
                st.markdown(f"<span style='color:#9AA3AE'>{representative.get('service_description')}</span>", unsafe_allow_html=True)

            if st.session_state.profile_edit_mode:
                st.markdown("&nbsp;", unsafe_allow_html=True)
                if st.button("🗑️ Delete Representative", key=f"profile_delete_{representative_id}"):
                    try:
                        api_client.delete_representative(representative_id)
                        st.success(f"✅ '{representative.get('representative_name')}' has been removed successfully.")
                        time.sleep(1.2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"We couldn't remove this representative. ({e})")

# =========================
# KNOWLEDGE BASE SECTION
# =========================
st.divider()
st.subheader("📚 Knowledge Base")
st.caption("Teach your AI about your business.")

if st.session_state.profile_edit_mode:
    source_type = st.radio("Source type", ["Text", "PDF", "URL"], horizontal=True)

    if source_type == "Text":
        text_content = st.text_area("Paste content")
        if st.button("Upload Text", type="primary"):
            if not text_content.strip():
                st.error("Please enter some text before uploading.")
            else:
                try:
                    api_client.upload_knowledge_text(text_content.strip())
                    st.success("✅ Text uploaded successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload failed. ({e})")

    elif source_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if st.button("Upload PDF", type="primary"):
            if not pdf_file:
                st.error("Please select a PDF file before uploading.")
            else:
                try:
                    api_client.upload_knowledge_pdf(pdf_file)
                    st.success("✅ PDF uploaded successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload failed. ({e})")

    elif source_type == "URL":
        url = st.text_input("Website URL")
        if st.button("Upload URL", type="primary"):
            if not url.strip():
                st.error("Please enter a website URL before uploading.")
            elif not url.strip().startswith(("http://", "https://")):
                st.error("Please enter a valid URL starting with http:// or https://")
            else:
                try:
                    api_client.upload_knowledge_url(url.strip())
                    st.success("✅ URL added successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload failed. ({e})")

st.divider()
st.subheader("Knowledge Sources")

try:
    documents = api_client.list_knowledge()
except Exception as e:
    documents = []
    st.error(f"We couldn't load your knowledge sources. ({e})")

if documents:
    st.caption(f"{len(documents)} source(s) added")

    icon_map = {"Text": "📝", "PDF": "📄", "URL": "🔗"}

    for doc in documents:
        source_type = doc.get("source_type", "Unknown")
        status = doc.get("processing_status", "Completed")
        icon = icon_map.get(source_type, "📚")

        with st.container(border=True):
            col1, col2, col3 = st.columns([0.5, 4, 1])
            with col1:
                st.markdown(f"### {icon}")
            with col2:
                st.markdown(f"**{source_type} Source**")
                path_preview = doc.get("source_path", "")
                if len(path_preview) > 100:
                    path_preview = path_preview[:100] + "..."
                st.caption(path_preview)
            with col3:
                if status == "Completed":
                    st.success("✅ Completed")
                elif status == "Failed":
                    st.error("❌ Failed")
                elif status == "Processing":
                    st.warning("⏳ Processing")
                else:
                    st.info(status)

                if st.session_state.profile_edit_mode:
                    if st.button("Delete", key=f"delete_kb_{doc.get('knowledge_base_id')}"):
                        try:
                            api_client.delete_knowledge(doc.get("knowledge_base_id"))
                            st.success("✅ Knowledge source deleted successfully.")
                            time.sleep(1.2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"We couldn't delete this source. ({e})")
else:
    st.info("No knowledge sources added yet.")