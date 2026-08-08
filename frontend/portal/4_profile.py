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

inject_custom_css()

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
# HELPER FUNCTIONS
# ============================================================

def display_value(value, fallback="Not provided"):
    """
    Safely display profile values.
    """
    if value is None:
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return value


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


def check_calendar_status(representative_id):

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


# ============================================================
# PAGE HEADER
# ============================================================

st.title("👤 Profile")

st.caption(
    "Manage your organization, representatives, and AI knowledge."
)


# ============================================================
# EDIT BUTTON
# ============================================================

if not st.session_state.profile_edit_mode:

    header_col1, header_col2 = st.columns(
        [5, 1.4]
    )

    with header_col1:

        st.write(
            "Your business profile and workspace information."
        )

    with header_col2:

        if st.button(
            "✏️ Edit Profile",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.profile_edit_mode = True

            st.rerun()

else:

    header_col1, header_col2 = st.columns(
        [5, 1.4]
    )

    with header_col1:

        st.info(
            "Edit mode is active. You can update your business "
            "information and manage representatives and knowledge sources."
        )

    with header_col2:

        if st.button(
            "✕ Cancel",
            use_container_width=True,
        ):

            st.session_state.profile_edit_mode = False

            st.rerun()


# ============================================================
# ORGANIZATION
# ============================================================

st.divider()

st.subheader("🏢 Organization")

st.caption(
    "Your business information used across EngageAI."
)


# ============================================================
# VIEW MODE
# ============================================================

if not st.session_state.profile_edit_mode:

    # --------------------------------------------------------
    # MAIN ORGANIZATION CARD
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            f"### {display_value(org.get('organization_name'))}"
        )

        st.caption(
            display_value(
                org.get("business_type")
            )
        )

        st.divider()

        col1, col2 = st.columns([5, 1.4])

        with col1:
            st.write("**Knowledge Sources**")

        with col2:

            button_text = (
                "✕ Close"
                if st.session_state.show_knowledge_upload
                else "＋ Add Source"
            )

            if st.button(
                button_text,
                use_container_width=True,
            ):
                st.session_state.show_knowledge_upload = (
                    not st.session_state.show_knowledge_upload
                )
                st.rerun()
        with col2:

            st.write("📞 **Business phone**")

            st.write(
                display_value(
                    org.get("business_phone")
                )
            )

            st.write("🌍 **Country**")

            st.write(
                display_value(
                    org.get("country")
                )
            )

        st.write("📍 **Address**")

        st.write(
            display_value(
                org.get("address")
            )
        )

        st.write("📝 **Business description**")

        st.write(
            display_value(
                org.get("description")
            )
        )


# ============================================================
# EDIT MODE
# ============================================================

else:

    with st.form(
        "profile_organization_form"
    ):

        st.write(
            "**Organization information**"
        )

        organization_name = st.text_input(
            "Organization name",
            value=org.get(
                "organization_name",
                "",
            ),
            disabled=True,
            help=(
                "Organization name is managed during "
                "initial setup."
            ),
        )

        current_business_type = org.get(
            "business_type",
            "Other",
        )

        business_type = st.selectbox(
            "Business type *",
            BUSINESS_TYPES,
            index=(
                BUSINESS_TYPES.index(
                    current_business_type
                )
                if current_business_type in BUSINESS_TYPES
                else 0
            ),
        )

        col1, col2 = st.columns(2)

        with col1:

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

        with col2:

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
        )

        description = st.text_area(
            "Business description",
            value=org.get(
                "description",
                "",
            ),
            height=140,
        )

        save_org = st.form_submit_button(
            "💾 Save Organization",
            type="primary",
            use_container_width=True,
        )


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

st.subheader("👥 Representatives")

st.caption(
    "People who represent your business and handle services."
)


representatives = fetch_representatives()


# ============================================================
# REPRESENTATIVES — VIEW
# ============================================================

if not st.session_state.profile_edit_mode:

    if not representatives:

        st.info(
            "No representatives have been added yet."
        )

    else:

        st.caption(
            f"{len(representatives)} representative(s)"
        )

        # Two-column cards
        for start in range(
            0,
            len(representatives),
            2,
        ):

            row = representatives[
                start:start + 2
            ]

            columns = st.columns(
                len(row)
            )

            for column, representative in zip(
                columns,
                row,
            ):

                with column:

                    representative_id = representative.get(
                        "representative_id"
                    )

                    name = display_value(
                        representative.get(
                            "representative_name"
                        )
                    )

                    service = display_value(
                        representative.get(
                            "service"
                        )
                    )

                    email = display_value(
                        representative.get(
                            "company_email"
                        )
                    )

                    invitation = display_value(
                        representative.get(
                            "invitation_status",
                            "Pending",
                        )
                    )

                    calendar = check_calendar_status(
                        representative_id
                    )

                    calendar_status = calendar.get(
                        "connection_status",
                        "Unknown",
                    )

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### 👤 {name}"
                        )

                        st.caption(
                            service
                        )

                        st.write(
                            f"📧 {email}"
                        )

                        st.divider()

                        if str(invitation).lower() in [
                            "accepted",
                            "active",
                            "approved",
                        ]:

                            st.success(
                                f"Invitation · {invitation}"
                            )

                        else:

                            st.warning(
                                f"Invitation · {invitation}"
                            )

                        if calendar_status == "Connected":

                            st.success(
                                "🟢 Calendar connected"
                            )

                        elif calendar_status == "Unknown":

                            st.warning(
                                "⚪ Calendar status unknown"
                            )

                        else:

                            st.warning(
                                "🟡 Calendar not connected"
                            )

                        st.caption(
                            display_value(
                                representative.get(
                                    "service_description"
                                )
                            )
                        )


# ============================================================
# REPRESENTATIVES — EDIT MODE
# ============================================================

else:

    if representatives:

        for representative in representatives:

            representative_id = representative.get(
                "representative_id"
            )

            name = display_value(
                representative.get(
                    "representative_name"
                )
            )

            service = display_value(
                representative.get(
                    "service"
                )
            )

            email = display_value(
                representative.get(
                    "company_email"
                )
            )

            invitation = display_value(
                representative.get(
                    "invitation_status",
                    "Pending",
                )
            )

            calendar = check_calendar_status(
                representative_id
            )

            calendar_status = calendar.get(
                "connection_status",
                "Unknown",
            )

            with st.expander(
                f"👤 {name} · {service}",
                expanded=True,
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Company email:** {email}"
                    )

                    st.write(
                        "**Service description:**"
                    )

                    st.write(
                        display_value(
                            representative.get(
                                "service_description"
                            )
                        )
                    )

                with col2:

                    st.write(
                        f"**Invitation:** {invitation}"
                    )

                    st.write(
                        f"**Calendar:** {calendar_status}"
                    )

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
                            "Representative deleted."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Delete failed. ({e})"
                        )

    else:

        st.info(
            "No representatives added yet."
        )


# ============================================================
# ADD REPRESENTATIVE — EDIT MODE
# ============================================================

if st.session_state.profile_edit_mode:

    st.divider()

    st.subheader(
        "➕ Add Representative"
    )

    with st.expander(
        "Add a new representative",
        expanded=False,
    ):

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

            company_email = st.text_input(
                "Company email *",
                placeholder="representative@company.com",
            )

            service_description = st.text_area(
                "Service description",
                placeholder=(
                    "Describe the service handled by this representative."
                ),
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
                    "representative_name":
                        representative_name,
                    "service":
                        service,
                    "service_description":
                        service_description,
                    "company_email":
                        company_email,
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
                        f"Add representative failed. ({e})"
                    )


# ============================================================
# KNOWLEDGE BASE
# ============================================================

st.divider()

st.subheader("📚 Knowledge Base")

st.caption(
    "Business information used by your AI assistant."
)


# ============================================================
# LOAD KNOWLEDGE
# ============================================================

try:

    documents = api_client.list_knowledge()

except Exception as e:

    documents = []

    st.error(
        f"Knowledge sources load nahi ho sake. ({e})"
    )


# ============================================================
# KNOWLEDGE — VIEW MODE
# ============================================================

if not st.session_state.profile_edit_mode:

    if not documents:

        st.info(
            "No knowledge sources have been added yet."
        )

    else:

        st.caption(
            f"{len(documents)} source(s) added"
        )

        for doc in documents:

            source_type = display_value(
                doc.get(
                    "source_type",
                    "Unknown",
                )
            )

            processing_status = display_value(
                doc.get(
                    "processing_status",
                    "Unknown",
                )
            )

            source_path = display_value(
                doc.get(
                    "source_path",
                    ""
                )
            )

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"### 📄 {source_type}"
                    )

                    if source_path != "Not provided":

                        st.caption(
                            source_path
                        )

                with col2:

                    if str(processing_status).lower() in [
                        "completed",
                        "processed",
                        "success",
                    ]:

                        st.success(
                            "✓ Completed"
                        )

                    elif str(processing_status).lower() in [
                        "failed",
                        "error",
                    ]:

                        st.error(
                            "✕ Failed"
                        )

                    else:

                        st.info(
                            processing_status
                        )

# ============================================================
# KNOWLEDGE — EDIT MODE
# ============================================================

else:

    st.caption(
        "Manage the information your AI assistant uses."
    )

    # --------------------------------------------------------
    # ADD SOURCE TOGGLE
    # --------------------------------------------------------

    if "show_knowledge_upload" not in st.session_state:
        st.session_state.show_knowledge_upload = False

    col1, col2 = st.columns([4, 1.2])

    with col1:
        st.write(
            "**Knowledge sources**"
        )

    with col2:

        button_text = (
            "✕ Close"
            if st.session_state.show_knowledge_upload
            else "＋ Add Source"
        )

        if st.button(
            button_text,
            use_container_width=True,
        ):

            st.session_state.show_knowledge_upload = (
                not st.session_state.show_knowledge_upload
            )

            st.rerun()


    # --------------------------------------------------------
    # UPLOAD PANEL — ONLY WHEN OPEN
    # --------------------------------------------------------

    if st.session_state.show_knowledge_upload:

        st.write("")

        with st.container(border=True):

            st.markdown(
                "#### Add Knowledge Source"
            )

            source_type = st.radio(
                "Source type",
                [
                    "Text",
                    "PDF",
                    "URL",
                ],
                horizontal=True,
            )

            # ------------------------------------------------
            # TEXT
            # ------------------------------------------------

            if source_type == "Text":

                text_content = st.text_area(
                    "Content",
                    placeholder=(
                        "Paste business information, FAQs, "
                        "services, pricing, policies, etc."
                    ),
                    height=130,
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

                            st.session_state.show_knowledge_upload = False

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Upload failed. ({e})"
                            )


            # ------------------------------------------------
            # PDF
            # ------------------------------------------------

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

                            st.session_state.show_knowledge_upload = False

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Upload failed. ({e})"
                            )


            # ------------------------------------------------
            # URL
            # ------------------------------------------------

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
                            "Please enter a URL first."
                        )

                    else:

                        try:

                            api_client.upload_knowledge_url(
                                url
                            )

                            st.success(
                                "URL uploaded successfully!"
                            )

                            st.session_state.show_knowledge_upload = False

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Upload failed. ({e})"
                            )


    # --------------------------------------------------------
    # EXISTING SOURCES
    # --------------------------------------------------------

    if documents:

        st.write("")
        st.write("**Existing sources**")

        for doc in documents:

            knowledge_id = doc.get(
                "knowledge_base_id"
            )

            source_type = display_value(
                doc.get(
                    "source_type"
                )
            )

            processing_status = display_value(
                doc.get(
                    "processing_status"
                )
            )

            source_path = display_value(
                doc.get(
                    "source_path"
                )
            )

            with st.container(
                border=True
            ):

                col1, col2, col3 = st.columns(
                    [3.5, 2, 1]
                )

                with col1:

                    st.write(
                        f"📄 **{source_type}**"
                    )

                    if source_path != "Not provided":

                        st.caption(
                            source_path
                        )

                with col2:

                    if str(processing_status).lower() in [
                        "completed",
                        "processed",
                        "success",
                    ]:

                        st.success(
                            "✓ Completed"
                        )

                    elif str(processing_status).lower() in [
                        "failed",
                        "error",
                    ]:

                        st.error(
                            "✕ Failed"
                        )

                    else:

                        st.info(
                            processing_status
                        )

                with col3:

                    if st.button(
                        "🗑️",
                        key=f"delete_kb_{knowledge_id}",
                        help="Delete this knowledge source",
                    ):

                        try:

                            api_client.delete_knowledge(
                                knowledge_id
                            )

                            st.success(
                                "Source deleted."
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