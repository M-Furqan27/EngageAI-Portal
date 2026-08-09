

"""
frontend/portal/0_onboarding.py

Onboarding page after first login.

Steps:
1. Organization
2. Representatives
3. Knowledge Base

Finish Setup marks onboarding completed and redirects dashboard.
"""

import streamlit as st
from utils import api_client
import requests
from utils.theme import inject_custom_css
from utils.auth import require_login

inject_custom_css()


st.set_page_config(
    page_title="EngageAI Portal",
    page_icon="👥",
    layout="wide",
)




# ---------------- AUTH CHECK ----------------

require_login()



# ---------------- CHECK ONBOARDING STATUS ----------------

try:
    org = api_client.get_organization_profile()

    if org.get("onboarding_completed"):
        st.switch_page("portal/3_dashboard.py")

except Exception as e:
    st.error(f"Organization data load nahi ho saka. ({e})")
    st.stop()



st.title("👋 Welcome! Let's set up your business.")
st.caption(
    "3 steps complete karein, phir aapka dashboard ready ho jayega."
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


tab1, tab2, tab3 = st.tabs(
    [
        "🏢 Organization",
        "🧑‍💼 Representatives",
        "📚 Knowledge Base"
    ]
)



# ============================================================
# TAB 1 ORGANIZATION
# ============================================================

with tab1:

    st.subheader("Complete your business profile")


    with st.form("onboarding_org_form"):

        current_business = org.get(
            "business_type",
            "Other"
        )


        business_type = st.selectbox(
            "Business type *",
            BUSINESS_TYPES,
            index=(
                BUSINESS_TYPES.index(current_business)
                if current_business in BUSINESS_TYPES
                else 0
            )
        )


        website = st.text_input(
            "Website *",
            value=org.get("website") or ""
        )


        business_email = st.text_input(
            "Business email *",
            value=org.get("business_email") or ""
        )


        business_phone = st.text_input(
            "Business phone *",
            value=org.get("business_phone") or ""
        )


        current_country = org.get(
            "country",
            "Pakistan"
        )


        country = st.selectbox(
            "Country *",
            COUNTRIES,
            index=(
                COUNTRIES.index(current_country)
                if current_country in COUNTRIES
                else 0
            )
        )


        address = st.text_area(
            "Address",
            value=org.get("address") or ""
        )


        description = st.text_area(
            "Description",
            value=org.get("description") or ""
        )


        save_org = st.form_submit_button(
            "Save Organization →",
            type="primary"
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
                "Organization details saved!"
            )


        except Exception as e:

            st.error(
                f"Save fail ho gaya. ({e})"
            )



# ============================================================
# TAB 2 REPRESENTATIVES
# ============================================================

with tab2:

    API_BASE_URL = st.secrets.get(
        "API_BASE_URL",
        "https://engageai-portal.onrender.com",
    )

    ORGANIZATION_ID = (
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )

    REQUEST_TIMEOUT = 120

    st.title("Representative Management")

    st.caption(
        "Add and manage company representatives."
    )

    def get_error_message(response):

        try:
            data = response.json()

            detail = data.get(
                "detail",
                data,
            )

            if isinstance(detail, str):
                return detail

            return str(detail)

        except ValueError:
            return (
                response.text
                or "Unexpected backend error."
            )

    def fetch_representatives():

        try:

            response = requests.get(
                f"{API_BASE_URL}/representatives",
                params={
                    "organization_id": ORGANIZATION_ID,
                },
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            return response.json()


        except requests.RequestException as error:

            st.error(
                f"Could not load representatives: {error}"
            )

            return []

    def check_calendar_status(
        representative_id: str,
    ):

        try:

            response = requests.get(
                f"{API_BASE_URL}/representatives/{representative_id}/calendar/check",
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            return response.json()


        except requests.RequestException as error:

            return {
                "calendar_connected": False,
                "connection_status": "Unknown",
                "error": str(error),
            }

    def add_representative(
        representative_name,
        service,
        service_description,
        company_email,
    ):

        payload = {

            "organization_id":
                ORGANIZATION_ID,

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

            response = requests.post(
                f"{API_BASE_URL}/representatives",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )


            if response.status_code == 201:

                return (
                    True,
                    "Representative added successfully."
                )


            return (
                False,
                get_error_message(response)
            )


        except requests.RequestException as error:

            return (
                False,
                str(error)
            )

    def delete_representative(
        representative_id,
    ):

        try:

            response = requests.delete(
                f"{API_BASE_URL}/representatives/{representative_id}",
                timeout=REQUEST_TIMEOUT,
            )


            if response.status_code == 204:

                return True


            return False


        except requests.RequestException:

            return False

    with st.form(
        "add_representative_form",
        clear_on_submit=True,
    ):

        st.subheader(
            "Add Representative"
        )


        representative_name = st.text_input(
            "Representative Name",
            placeholder="Ali",
        )


        service = st.text_input(
            "Service",
            placeholder="Vehicle Inspection",
        )


        service_description = st.text_area(
            "Service Description",
            placeholder=(
                "Describe the service provided..."
            ),
        )


        company_email = st.text_input(
            "Company Email",
            placeholder="ali@company.com",
        )


        submitted = st.form_submit_button(
            "Add Representative",
            use_container_width=True,
        )


        if submitted:


            if not representative_name.strip():

                st.error(
                    "Representative name is required."
                )


            elif not service.strip():

                st.error(
                    "Service is required."
                )


            elif not service_description.strip():

                st.error(
                    "Service description is required."
                )


            elif not company_email.strip():

                st.error(
                    "Company email is required."
                )


            else:

                success, message = add_representative(
                    representative_name.strip(),
                    service.strip(),
                    service_description.strip(),
                    company_email.strip(),
                )


                if success:

                    st.success(message)

                    st.rerun()


                else:

                    st.error(message)

    st.divider()

    st.subheader(
        "Representatives"
    )

    representatives = fetch_representatives()

    if not representatives:

        st.info(
            "No representatives added yet."
        )


    else:


        for representative in representatives:


            representative_id = (
                representative[
                    "representative_id"
                ]
            )


            # Check real Google status
            calendar_status = check_calendar_status(
                representative_id
            )


            connection_status = (
                calendar_status.get(
                    "connection_status",
                    "Unknown",
                )
            )



            with st.container(border=True):


                col1, col2, col3, col4, col5, col6, col7 = st.columns(
                    [
                        1.2,
                        1.2,
                        1.5,
                        2,
                        1.2,
                        1.2,
                        0.8,
                    ]
                )


                with col1:

                    st.write(
                        "**Representative**"
                    )

                    st.write(
                        representative.get(
                            "representative_name",
                            "Unknown",
                        )
                    )


                with col2:

                    st.write(
                        "**Service**"
                    )

                    st.write(
                        representative.get(
                            "service",
                            "",
                        )
                    )


                with col3:

                    st.write(
                        "**Email**"
                    )

                    st.write(
                        representative.get(
                            "company_email",
                            "",
                        )
                    )


                with col4:

                    st.write(
                        "**Description**"
                    )

                    st.write(
                        representative.get(
                            "service_description",
                            "",
                        )
                    )


                with col5:

                    st.write(
                        "**Invitation**"
                    )


                    invitation = representative.get(
                        "invitation_status",
                        "Pending",
                    )


                    if invitation == "Sent":

                        st.success(
                            "Sent"
                        )

                    elif invitation == "Email Failed":

                        st.error(
                            "Failed"
                        )

                    else:

                        st.warning(
                            invitation
                        )



                with col6:

                    st.write(
                        "**Calendar**"
                    )


                    if connection_status == "Connected":

                        st.success(
                            "Connected"
                        )


                    elif connection_status == "Revoked":

                        st.error(
                            "Revoked"
                        )


                    else:

                        st.warning(
                            "Not Connected"
                        )



                with col7:

                    st.write(
                        "**Action**"
                    )


                    if st.button(
                        "Delete",
                        key=f"delete_{representative_id}",
                        use_container_width=True,
                    ):

                        if delete_representative(
                            representative_id
                        ):

                            st.success(
                                "Deleted successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Delete failed."
                            )
with tab3:


    st.subheader(
        "Teach your AI about your business"
    )


    kb_type = st.radio(
        "Source type",
        [
            "Text",
            "PDF",
            "URL"
        ],
        horizontal=True
    )



    if kb_type == "Text":

        text_content = st.text_area(
            "Paste content"
        )


        if st.button(
            "Upload Text →"
        ):

            try:

                api_client.upload_knowledge_text(
                    text_content
                )

                st.success(
                    "Text uploaded!"
                )

                st.rerun()


            except Exception as e:

                st.error(
                    f"Upload fail ({e})"
                )



    elif kb_type == "PDF":


        pdf_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )


        if st.button(
            "Upload PDF →"
        ):


            if pdf_file:

                try:

                    api_client.upload_knowledge_pdf(
                        pdf_file
                    )


                    st.success(
                        "PDF uploaded!"
                    )

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"Upload fail ({e})"
                    )



    elif kb_type == "URL":


        url = st.text_input(
            "Website URL"
        )


        if st.button(
            "Upload URL →"
        ):


            try:

                api_client.upload_knowledge_url(
                    url
                )

                st.success(
                    "URL added!"
                )

                st.rerun()


            except Exception as e:

                st.error(
                    f"Upload fail ({e})"
                )



    st.divider()



    try:

        docs = api_client.list_knowledge()


    except Exception as e:

        docs = []

        st.error(
            f"Knowledge load nahi hui ({e})"
        )



    if docs:


        st.caption(
            f"{len(docs)} source(s) added:"
        )


        for doc in docs:

            with st.container(border=True):

                if isinstance(doc, str):
                    source_type = "File"
                    status = "Completed"
                    source_name = doc

                else:
                    source_type = doc.get(
                        "source_type",
                        doc.get(
                            "type",
                            "Unknown"
                        )
                    )

                    status = doc.get(
                        "processing_status",
                        doc.get(
                            "status",
                            "Completed"
                        )
                    )

                    source_name = doc.get(
                        "source_name",
                        doc.get(
                            "name",
                            ""
                        )
                    )

                st.markdown(
                    f"**{source_type}** — {status}"
                )

                if source_name:
                    st.caption(source_name)
    else:

        st.info(
            "Abhi koi knowledge source add nahi hua."
        )



# ============================================================
# FINISH SETUP
# ============================================================


st.divider()


if st.button(
    "✅ Finish Setup & Go to Dashboard →",
    type="primary",
    use_container_width=True
):

    try:

        api_client.complete_onboarding()

        st.session_state.onboarding_completed = True

        st.success(
            "Setup complete!"
        )

        # switch_page nahi — rerun se app.py naya nav_pages banayega
        # (Workspace: Dashboard, Profile) aur khud dashboard khul jayegi.
        st.rerun()


    except Exception as e:

        st.error(
            f"Fail ho gaya ({e})"
        )