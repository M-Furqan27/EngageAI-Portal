import streamlit as st
import requests

from utils import api_client
from utils.sidebar import render_account_sidebar
from utils.theme import inject_custom_css
from utils.auth import require_login


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Profile | EngageAI",
    page_icon="👤",
    layout="wide",
)


# ============================================================
# GLOBAL THEME
# ============================================================

inject_custom_css()


# ============================================================
# AUTH
# ============================================================

require_login()

render_account_sidebar()


# ============================================================
# SESSION STATE
# ============================================================

if "profile_edit_mode" not in st.session_state:
    st.session_state.profile_edit_mode = False


# ============================================================
# CONSTANTS
# ============================================================

BUSINESS_TYPES = [
    "Retail",
    "Healthcare",
    "Education",
    "Services",
    "Other",
]

COUNTRIES = [
    "Pakistan",
    "India",
    "Bangladesh",
    "United Arab Emirates",
    "Saudi Arabia",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "France",
    "China",
    "Japan",
    "Turkey",
    "Qatar",
    "Kuwait",
    "Oman",
    "Bahrain",
    "Malaysia",
    "Indonesia",
    "Sri Lanka",
    "Nepal",
    "Afghanistan",
    "Egypt",
    "South Africa",
    "Nigeria",
    "Other",
]


# ============================================================
# API CONFIG
# ============================================================

API_BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "https://engageai-portal.onrender.com",
)

REQUEST_TIMEOUT = 120


# ============================================================
# LOAD ORGANIZATION
# ============================================================

try:

    org = api_client.get_organization_profile()

except Exception as e:

    st.error(
        f"Organization profile load nahi ho saka. ({e})"
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("👤 Profile")

st.caption(
    "Manage your organization, representatives, and AI knowledge."
)


# ============================================================
# PROFILE CONTROLS
# ============================================================

if not st.session_state.profile_edit_mode:

    col1, col2, col3 = st.columns([5, 1.5, 1.5])

    with col1:

        st.markdown(
            "### Organization Profile"
        )

        st.caption(
            "View your current business configuration."
        )

    with col3:

        if st.button(
            "✏️ Edit Profile",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.profile_edit_mode = True

            st.rerun()

else:

    col1, col2, col3 = st.columns([5, 1.5, 1.5])

    with col1:

        st.markdown(
            "### Edit Profile"
        )

        st.caption(
            "Update your organization information and manage resources."
        )

    with col3:

        if st.button(
            "Cancel",
            use_container_width=True,
        ):

            st.session_state.profile_edit_mode = False

            st.rerun()


# ============================================================
# ORGANIZATION PROFILE
# ============================================================

st.divider()

st.subheader("🏢 Organization")

st.caption(
    "Your business information used across the EngageAI portal."
)


if not st.session_state.profile_edit_mode:

    # --------------------------------------------------------
    # VIEW MODE
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Organization",
            org.get(
                "organization_name",
                "-"
            ),
        )

        st.write("**Business type**")

        st.write(
            org.get(
                "business_type",
                "-"
            )
        )

        st.write("**Website**")

        website = org.get(
            "website",
            "",
        )

        if website:
            st.write(website)
        else:
            st.caption("Not provided")

        st.write("**Business email**")

        business_email = org.get(
            "business_email",
            "",
        )

        if business_email:
            st.write(business_email)
        else:
            st.caption("Not provided")

    with col2:

        st.write("**Business phone**")

        business_phone = org.get(
            "business_phone",
            "",
        )

        if business_phone:
            st.write(business_phone)
        else:
            st.caption("Not provided")

        st.write("**Country**")

        st.write(
            org.get(
                "country",
                "-"
            )
        )

        st.write("**Address**")

        address = org.get(
            "address",
            "",
        )

        if address:
            st.write(address)
        else:
            st.caption("Not provided")

    st.write("**Business description**")

    description = org.get(
        "description",
        "",
    )

    if description:
        st.write(description)
    else:
        st.caption(
            "No business description added yet."
        )


else:

    # --------------------------------------------------------
    # EDIT MODE
    # --------------------------------------------------------

    with st.form(
        "profile_organization_form"
    ):

        organization_name = st.text_input(
            "Organization name",
            value=org.get(
                "organization_name",
                "",
            ),
            disabled=True,
            help="Organization name is managed during onboarding.",
        )

        business_type_current = org.get(
            "business_type",
            "Other",
        )

        business_type = st.selectbox(
            "Business type *",
            BUSINESS_TYPES,
            index=(
                BUSINESS_TYPES.index(
                    business_type_current
                )
                if business_type_current in BUSINESS_TYPES
                else 0
            ),
        )

        website = st.text_input(
            "Website",
            value=org.get(
                "website",
                "",
            ),
            placeholder="https://example.com",
        )

        business_email = st.text_input(
            "Business email",
            value=org.get(
                "business_email",
                "",
            ),
            placeholder="contact@company.com",
        )

        business_phone = st.text_input(
            "Business phone",
            value=org.get(
                "business_phone",
                "",
            ),
            placeholder="+92 300 1234567",
        )

        current_country = org.get(
            "country",
            "Pakistan",
        )

        country = st.selectbox(
            "Country *",
            COUNTRIES,
            index=(
                COUNTRIES.index(
                    current_country
                )
                if current_country in COUNTRIES
                else 0
            ),
        )

        address = st.text_area(
            "Address",
            value=org.get(
                "address",
                "",
            ),
            placeholder="Business address",
        )

        description = st.text_area(
            "Business description",
            value=org.get(
                "description",
                "",
            ),
            placeholder="Tell customers about your business...",
        )

        st.write("")

        save_org = st.form_submit_button(
            "Save Organization",
            type="primary",
            use_container_width=True,
        )


    # --------------------------------------------------------
    # SAVE ORGANIZATION
    # --------------------------------------------------------

    if save_org:

        payload = {
            "business_type": business_type,
            "website": website,
            "business_email": business_email,
            "business_phone": business_phone,
            "country": country,
            "address": address,
            "description": description,
        }

        try:

            api_client.update_organization_profile(
                payload
            )

            st.success(
                "Organization profile updated successfully!"
            )

            st.session_state.profile_edit_mode = False

            st.rerun()

        except Exception as e:

            st.error(
                f"Organization update failed. ({e})"
            )


# ============================================================
# REPRESENTATIVES
# ============================================================

st.divider()

st.subheader("🧑‍💼 Representatives")

st.caption(
    "Manage the people who represent your business and their calendar connections."
)


# ============================================================
# FETCH REPRESENTATIVES
# ============================================================

def fetch_representatives():

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(
            f"Representatives load nahi ho sake. ({e})"
        )

        return []


# ============================================================
# CALENDAR STATUS
# ============================================================

def check_calendar_status(
    representative_id,
):

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives/"
            f"{representative_id}/calendar/check",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return {
            "connection_status": "Unknown"
        }


representatives = fetch_representatives()


# ============================================================
# REPRESENTATIVE LIST
# ============================================================

if not representatives:

    st.info(
        "No representatives have been added yet."
    )

else:

    for representative in representatives:

        representative_id = representative.get(
            "representative_id"
        )

        representative_name = representative.get(
            "representative_name",
            "-",
        )

        service = representative.get(
            "service",
            "-",
        )

        company_email = representative.get(
            "company_email",
            "-",
        )

        service_description = representative.get(
            "service_description",
            "-",
        )

        invitation_status = representative.get(
            "invitation_status",
            "Pending",
        )

        calendar_status = check_calendar_status(
            representative_id
        )

        connection_status = calendar_status.get(
            "connection_status",
            "Unknown",
        )

        # ----------------------------------------------------
        # CARD
        # ----------------------------------------------------

        with st.container(
            border=True
        ):

            st.markdown(
                f"### 👤 {representative_name}"
            )

            st.caption(
                service
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Company email**"
                )

                st.write(
                    company_email
                )

                st.write(
                    "**Service description**"
                )

                st.write(
                    service_description
                )

            with col2:

                st.write(
                    "**Invitation**"
                )

                if str(invitation_status).lower() in [
                    "accepted",
                    "active",
                    "approved",
                ]:

                    st.success(
                        str(invitation_status)
                    )

                else:

                    st.warning(
                        str(invitation_status)
                    )

                st.write(
                    "**Calendar**"
                )

                if connection_status == "Connected":

                    st.success(
                        "Connected"
                    )

                elif connection_status == "Unknown":

                    st.warning(
                        "Unknown"
                    )

                else:

                    st.warning(
                        "Not Connected"
                    )

            # ------------------------------------------------
            # DELETE
            # ------------------------------------------------

            if st.session_state.profile_edit_mode:

                st.divider()

                if st.button(
                    "🗑️ Delete Representative",
                    key=f"profile_delete_{representative_id}",
                ):

                    try:

                        api_client.delete_representative(
                            representative_id
                        )

                        st.success(
                            "Representative deleted successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Delete failed. ({e})"
                        )


# ============================================================
# ADD REPRESENTATIVE
# ============================================================

if st.session_state.profile_edit_mode:

    st.divider()

    st.subheader(
        "➕ Add Representative"
    )

    st.caption(
        "Add a new person who can represent your business."
    )

    with st.form(
        "profile_add_rep_form"
    ):

        representative_name = st.text_input(
            "Representative name *",
            placeholder="e.g. Ahmed Khan",
        )

        service = st.text_input(
            "Service *",
            placeholder="e.g. Sales",
        )

        service_description = st.text_area(
            "Service description",
            placeholder="Describe the service handled by this representative.",
        )

        company_email = st.text_input(
            "Company email *",
            placeholder="representative@company.com",
        )

        add_rep = st.form_submit_button(
            "Add Representative",
            type="primary",
            use_container_width=True,
        )

    if add_rep:

        if not representative_name.strip():

            st.error(
                "Representative name is required."
            )

        elif not service.strip():

            st.error(
                "Service is required."
            )

        elif not company_email.strip():

            st.error(
                "Company email is required."
            )

        else:

            payload = {
                "organization_id": org.get(
                    "organization_id"
                ),
                "representative_name": representative_name,
                "service": service,
                "service_description": service_description,
                "company_email": company_email,
            }

            try:

                api_client.create_representative(
                    payload
                )

                st.success(
                    "Representative added successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Representative add failed. ({e})"
                )


# ============================================================
# KNOWLEDGE BASE
# ============================================================

st.divider()

st.subheader("📚 Knowledge Base")

st.caption(
    "Teach EngageAI about your business using text, documents, and URLs."
)


# ============================================================
# UPLOAD — EDIT MODE ONLY
# ============================================================

if st.session_state.profile_edit_mode:

    source_type = st.radio(
        "Source type",
        [
            "Text",
            "PDF",
            "URL",
        ],
        horizontal=True,
    )

    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    if source_type == "Text":

        text_content = st.text_area(
            "Content",
            placeholder=(
                "Paste information about your business, "
                "services, pricing, policies, FAQs, etc."
            ),
            height=180,
        )

        if st.button(
            "Upload Text",
            type="primary",
        ):

            if not text_content.strip():

                st.warning(
                    "Please enter some content first."
                )

            else:

                try:

                    api_client.upload_knowledge_text(
                        text_content
                    )

                    st.success(
                        "Text uploaded successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Text upload failed. ({e})"
                    )

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    elif source_type == "PDF":

        pdf_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
        )

        if st.button(
            "Upload PDF",
            type="primary",
        ):

            if pdf_file is None:

                st.warning(
                    "Please select a PDF first."
                )

            else:

                try:

                    api_client.upload_knowledge_pdf(
                        pdf_file
                    )

                    st.success(
                        "PDF uploaded successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"PDF upload failed. ({e})"
                    )

    # --------------------------------------------------------
    # URL
    # --------------------------------------------------------

    elif source_type == "URL":

        url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
        )

        if st.button(
            "Upload URL",
            type="primary",
        ):

            if not url.strip():

                st.warning(
                    "Please enter a website URL."
                )

            else:

                try:

                    api_client.upload_knowledge_url(
                        url
                    )

                    st.success(
                        "URL uploaded successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"URL upload failed. ({e})"
                    )


# ============================================================
# EXISTING KNOWLEDGE SOURCES
# ============================================================

st.divider()

st.subheader(
    "Knowledge Sources"
)


try:

    documents = api_client.list_knowledge()

except Exception as e:

    documents = []

    st.error(
        f"Knowledge sources load nahi ho sake. ({e})"
    )


if documents:

    st.caption(
        f"{len(documents)} source(s) added"
    )

    for doc in documents:

        knowledge_id = doc.get(
            "knowledge_base_id"
        )

        source_type = doc.get(
            "source_type",
            "Unknown",
        )

        processing_status = doc.get(
            "processing_status",
            "Unknown",
        )

        source_path = doc.get(
            "source_path",
            "",
        )

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.write(
                    f"**{source_type}**"
                )

                if str(processing_status).lower() in [
                    "completed",
                    "processed",
                    "success",
                ]:

                    st.success(
                        str(processing_status)
                    )

                elif str(processing_status).lower() in [
                    "failed",
                    "error",
                ]:

                    st.error(
                        str(processing_status)
                    )

                else:

                    st.info(
                        str(processing_status)
                    )

                if source_path:

                    st.caption(
                        source_path
                    )

            with col2:

                if st.session_state.profile_edit_mode:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_kb_{knowledge_id}",
                    ):

                        try:

                            api_client.delete_knowledge(
                                knowledge_id
                            )

                            st.success(
                                "Knowledge source deleted."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Delete failed. ({e})"
                            )

else:

    st.info(
        "No knowledge sources added yet."
    )