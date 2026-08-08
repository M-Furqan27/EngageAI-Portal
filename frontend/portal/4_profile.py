# import streamlit as st
# from utils import api_client

# if "token" not in st.session_state or st.session_state.token is None:
#     st.warning("Pehle login karein.")
#     st.stop()

# st.title("🏢 Profile")

# tab1, tab2 = st.tabs(["🏢 Organization", "👤 My Account"])

# # ============================================================
# # TAB 1 — Organization profile
# # ============================================================
# with tab1:
#     try:
#         org = api_client.get_organization_profile()
#     except Exception as e:
#         st.error(f"Organization profile load nahi ho saka. ({e})")
#         org = None

#     if org:
#         with st.form("org_profile_form"):
#             organization_name = st.text_input("Organization name", value=org.get("organization_name", ""))
#             business_type = st.selectbox(
#                 "Business type",
#                 ["Retail", "Healthcare", "Education", "Services", "Other"],
#                 index=["Retail", "Healthcare", "Education", "Services", "Other"].index(org["business_type"])
#                 if org.get("business_type") in ["Retail", "Healthcare", "Education", "Services", "Other"] else 0,
#             )
#             website = st.text_input("Website", value=org.get("website", ""))
#             business_email = st.text_input("Business email", value=org.get("business_email", ""))
#             business_phone = st.text_input("Business phone", value=org.get("business_phone", ""))
#             country = st.text_input("Country", value=org.get("country", ""))
#             address = st.text_area("Address", value=org.get("address") or "")
#             description = st.text_area("Description", value=org.get("description") or "")

#             org_save = st.form_submit_button("Save Organization →", type="primary")

#         if org_save:
#             payload = {
#                 "organization_name": organization_name,
#                 "business_type": business_type,
#                 "website": website,
#                 "business_email": business_email,
#                 "business_phone": business_phone,
#                 "country": country,
#                 "address": address,
#                 "description": description,
#             }
#             try:
#                 api_client.update_organization_profile(payload)
#                 st.success("Organization profile update ho gayi!")
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"Update fail ho gaya. ({e})")

# # ============================================================
# # TAB 2 — My account (logged-in user)
# # ============================================================
# with tab2:
#     try:
#         me = api_client.get_my_user_profile()
#     except Exception as e:
#         st.error(f"Profile load nahi ho saka. ({e})")
#         me = None

#     if me:
#         st.caption(f"Role: **{me['role']}** · Status: **{me['status']}**")

#         with st.form("user_profile_form"):
#             first_name = st.text_input("First name", value=me.get("first_name", ""))
#             last_name = st.text_input("Last name", value=me.get("last_name", ""))
#             phone = st.text_input("Phone", value=me.get("phone", ""))
#             st.text_input("Email (change nahi ho sakta)", value=me.get("email", ""), disabled=True)

#             user_save = st.form_submit_button("Save My Profile →", type="primary")

#         if user_save:
#             payload = {"first_name": first_name, "last_name": last_name, "phone": phone}
#             try:
#                 updated = api_client.update_my_user_profile(payload)
#                 st.session_state.user = updated
#                 st.success("Profile update ho gayi!")
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"Update fail ho gaya. ({e})")



# frontend/portal/4_profile.py

import streamlit as st
import requests
from utils import api_client
from utils.sidebar import render_account_sidebar


st.set_page_config(
    page_title="Profile",
    page_icon="🏢",
    layout="wide"
)


# =========================
# AUTH CHECK
# =========================

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()

render_account_sidebar()



# =========================
# PROFILE MODE
# =========================

if "profile_edit_mode" not in st.session_state:

    st.session_state.profile_edit_mode = False



# =========================
# LOAD ORGANIZATION
# =========================

try:

    org = api_client.get_organization_profile()


except Exception as e:

    st.error(
        f"Profile load nahi ho saka ({e})"
    )

    st.stop()



# =========================
# HEADER
# =========================

st.title("🏢 Profile")

st.caption(
    "Manage your organization setup."
)



# =========================
# BUTTON CONTROL
# =========================

if not st.session_state.profile_edit_mode:


    if st.button(
        "✏️ Edit Profile",
        type="primary",
        use_container_width=True
    ):

        st.session_state.profile_edit_mode = True

        st.rerun()



else:

    col1, col2 = st.columns(2)


    with col1:

        st.info(
            "Edit mode enabled"
        )


    with col2:

        if st.button(
            "❌ Cancel Edit",
            use_container_width=True
        ):

            st.session_state.profile_edit_mode = False

            st.rerun()


# =========================
# ORGANIZATION SECTION
# =========================


st.divider()

st.subheader(
    "🏢 Organization"
)



BUSINESS_TYPES = [
    "Retail",
    "Healthcare",
    "Education",
    "Services",
    "Other"
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



if not st.session_state.profile_edit_mode:


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "**Business Type**"
        )

        st.write(
            org.get(
                "business_type",
                "-"
            )
        )


        st.write(
            "**Website**"
        )

        st.write(
            org.get(
                "website",
                "-"
            )
        )


        st.write(
            "**Business Email**"
        )

        st.write(
            org.get(
                "business_email",
                "-"
            )
        )


    with col2:


        st.write(
            "**Business Phone**"
        )

        st.write(
            org.get(
                "business_phone",
                "-"
            )
        )


        st.write(
            "**Country**"
        )

        st.write(
            org.get(
                "country",
                "-"
            )
        )


        st.write(
            "**Address**"
        )

        st.write(
            org.get(
                "address",
                "-"
            )
        )


    st.write(
        "**Description**"
    )

    st.write(
        org.get(
            "description",
            "-"
        )
    )



else:


    with st.form(
        "profile_organization_form"
    ):


        current_business = org.get(
            "business_type",
            "Other"
        )


        business_type = st.selectbox(
            "Business type *",
            BUSINESS_TYPES,
            index=(
                BUSINESS_TYPES.index(
                    current_business
                )
                if current_business in BUSINESS_TYPES
                else 0
            )
        )


        website = st.text_input(
            "Website *",
            value=org.get(
                "website",
                ""
            )
        )


        business_email = st.text_input(
            "Business email *",
            value=org.get(
                "business_email",
                ""
            )
        )


        business_phone = st.text_input(
            "Business phone *",
            value=org.get(
                "business_phone",
                ""
            )
        )


        current_country = org.get(
            "country",
            "Pakistan"
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
            )
        )


        address = st.text_area(
            "Address",
            value=org.get(
                "address",
                ""
            )
        )


        description = st.text_area(
            "Description",
            value=org.get(
                "description",
                ""
            )
        )


        save_org = st.form_submit_button(
            "Save Organization"
        )



    if save_org:


        payload = {

            "business_type": business_type,

            "website": website,

            "business_email": business_email,

            "business_phone": business_phone,

            "country": country,

            "address": address,

            "description": description

        }


        try:


            api_client.update_organization_profile(
                payload
            )


            st.success(
                "Organization updated!"
            )


            st.rerun()



        except Exception as e:


            st.error(
                f"Save failed ({e})"
            )
            
# =========================
# REPRESENTATIVES SECTION
# =========================


st.divider()

st.subheader(
    "🧑‍💼 Representative Management"
)

st.caption(
    "Add and manage company representatives."
)



API_BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "https://engageai-portal.onrender.com"
)


REQUEST_TIMEOUT = 120



def fetch_representatives():

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives",
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()


    except Exception as e:

        st.error(
            f"Representatives load nahi ho sake ({e})"
        )

        return []



def check_calendar_status(
    representative_id
):

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives/{representative_id}/calendar/check",
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()


    except Exception:


        return {
            "connection_status": "Unknown"
        }



representatives = fetch_representatives()



if not representatives:


    st.info(
        "No representatives added yet."
    )


else:


    for representative in representatives:


        representative_id = representative.get(
            "representative_id"
        )


        calendar_status = check_calendar_status(
            representative_id
        )


        connection_status = calendar_status.get(
            "connection_status",
            "Unknown"
        )



        with st.container(
            border=True
        ):


            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                [
                    1.2,
                    1.2,
                    1.5,
                    2,
                    1.2,
                    1.2,
                    0.8
                ]
            )


            with col1:

                st.write(
                    "**Representative**"
                )

                st.write(
                    representative.get(
                        "representative_name",
                        "-"
                    )
                )



            with col2:

                st.write(
                    "**Service**"
                )

                st.write(
                    representative.get(
                        "service",
                        "-"
                    )
                )



            with col3:

                st.write(
                    "**Email**"
                )

                st.write(
                    representative.get(
                        "company_email",
                        "-"
                    )
                )



            with col4:

                st.write(
                    "**Description**"
                )

                st.write(
                    representative.get(
                        "service_description",
                        "-"
                    )
                )



            with col5:

                st.write(
                    "**Invitation**"
                )

                st.write(
                    representative.get(
                        "invitation_status",
                        "Pending"
                    )
                )



            with col6:

                st.write(
                    "**Calendar**"
                )


                if connection_status == "Connected":

                    st.success(
                        "Connected"
                    )

                else:

                    st.warning(
                        "Not Connected"
                    )



            with col7:


                if st.session_state.profile_edit_mode:


                    if st.button(
                        "Delete",
                        key=f"profile_delete_{representative_id}"
                    ):


                        api_client.delete_representative(
                            representative_id
                        )


                        st.success(
                            "Deleted successfully"
                        )


                        st.rerun()


# =========================
# ADD REPRESENTATIVE
# EDIT MODE ONLY
# =========================


if st.session_state.profile_edit_mode:


    st.divider()

    st.subheader(
        "Add Representative"
    )


    with st.form(
        "profile_add_rep_form"
    ):


        representative_name = st.text_input(
            "Representative Name"
        )


        service = st.text_input(
            "Service"
        )


        service_description = st.text_area(
            "Service Description"
        )


        company_email = st.text_input(
            "Company Email"
        )


        add_rep = st.form_submit_button(
            "Add Representative"
        )


    if add_rep:


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
        company_email

}


        try:


            api_client.create_representative(
                payload
            )


            st.success(
                "Representative added!"
            )


            st.rerun()


        except Exception as e:


            st.error(
                f"Add failed ({e})"
            )
            
# =========================
# KNOWLEDGE BASE SECTION
# =========================


st.divider()

st.subheader(
    "📚 Knowledge Base"
)


st.caption(
    "Teach your AI about your business."
)



# =========================
# UPLOAD
# EDIT MODE ONLY
# =========================

if st.session_state.profile_edit_mode:


    source_type = st.radio(
        "Source type",
        [
            "Text",
            "PDF",
            "URL"
        ],
        horizontal=True
    )


    if source_type == "Text":


        text_content = st.text_area(
            "Paste content"
        )


        if st.button(
            "Upload Text"
        ):

            try:

                api_client.upload_knowledge_text(
                    text_content
                )

                st.success(
                    "Text uploaded"
                )

                st.rerun()


            except Exception as e:

                st.error(
                    f"Upload failed ({e})"
                )



    elif source_type == "PDF":


        pdf_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )


        if st.button(
            "Upload PDF"
        ):

            if pdf_file:

                try:

                    api_client.upload_knowledge_pdf(
                        pdf_file
                    )

                    st.success(
                        "PDF uploaded"
                    )

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"Upload failed ({e})"
                    )



    elif source_type == "URL":


        url = st.text_input(
            "Website URL"
        )


        if st.button(
            "Upload URL"
        ):

            try:

                api_client.upload_knowledge_url(
                    url
                )

                st.success(
                    "URL uploaded"
                )

                st.rerun()


            except Exception as e:

                st.error(
                    f"Upload failed ({e})"
                )



# =========================
# EXISTING SOURCES
# =========================


st.divider()

st.subheader(
    "Knowledge Sources"
)


try:

    documents = api_client.list_knowledge()


except Exception as e:

    documents = []

    st.error(
        f"Knowledge load failed ({e})"
    )



if documents:


    st.caption(
        f"{len(documents)} source(s) added"
    )


    for doc in documents:


        with st.container(
            border=True
        ):


            col1, col2 = st.columns(
                [5,1]
            )


            with col1:


                st.write(
                    f"**{doc.get('source_type')}** — {doc.get('processing_status')}"
                )


                st.caption(
                    doc.get(
                        "source_path",
                        ""
                    )
                )



            with col2:


                if st.session_state.profile_edit_mode:


                    if st.button(
                        "Delete",
                        key=f"delete_kb_{doc.get('knowledge_base_id')}"
                    ):


                        api_client.delete_knowledge(
                            doc.get(
                                "knowledge_base_id"
                            )
                        )


                        st.success(
                            "Deleted"
                        )


                        st.rerun()


else:


    st.info(
        "No knowledge sources added."
    )                                                    