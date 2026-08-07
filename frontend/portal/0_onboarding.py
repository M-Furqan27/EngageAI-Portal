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


# ---------------- AUTH CHECK ----------------

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()



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

    

    st.header("🧑‍💼 Representatives")
    st.caption(
        "Add and manage company representatives."
    )


    API_BASE_URL = st.secrets.get(
        "API_BASE_URL",
        "https://engageai-portal.onrender.com",
    )


    ORGANIZATION_ID = (
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )


    REQUEST_TIMEOUT = 120



    def get_error_message(response):

        try:

            data = response.json()

            detail = data.get(
                "detail",
                data,
            )

            return (
                detail
                if isinstance(detail, str)
                else str(detail)
            )

        except:

            return response.text



    def fetch_representatives():

        try:

            response = requests.get(
                f"{API_BASE_URL}/representatives",
                params={
                    "organization_id": ORGANIZATION_ID
                },
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            st.error(
                f"Could not load representatives: {e}"
            )

            return []



    def check_calendar_status(
        representative_id
    ):

        try:

            response = requests.get(
                f"{API_BASE_URL}/representatives/{representative_id}/calendar/check",
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            return response.json()

        except:

            return {
                "connection_status":
                    "Unknown"
            }



    def add_representative(
        name,
        service,
        description,
        email,
    ):


        payload = {

            "organization_id":
                ORGANIZATION_ID,

            "representative_name":
                name,

            "service":
                service,

            "service_description":
                description,

            "company_email":
                email,
        }


        try:

            response = requests.post(
                f"{API_BASE_URL}/representatives",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )


            if response.status_code == 201:

                return True, "Representative added."


            return False, get_error_message(response)


        except Exception as e:

            return False, str(e)



    def delete_representative(
        representative_id
    ):

        try:

            response = requests.delete(
                f"{API_BASE_URL}/representatives/{representative_id}",
                timeout=REQUEST_TIMEOUT,
            )

            return response.status_code == 204


        except:

            return False




    # ADD FORM

    with st.form(
        "onboarding_rep_form",
        clear_on_submit=True
    ):

        st.subheader(
            "Add Representative"
        )


        name = st.text_input(
            "Representative Name"
        )


        service = st.text_input(
            "Service"
        )


        description = st.text_area(
            "Service Description"
        )


        email = st.text_input(
            "Company Email"
        )


        submit = st.form_submit_button(
            "Add Representative",
            use_container_width=True
        )


        if submit:


            if not name or not service or not description or not email:

                st.error(
                    "All fields are required."
                )


            else:

                success, message = add_representative(
                    name,
                    service,
                    description,
                    email,
                )


                if success:

                    st.success(message)
                    st.rerun()

                else:

                    st.error(message)



    st.divider()


    st.subheader(
        "Existing Representatives"
    )


    representatives = fetch_representatives()



    if not representatives:

        st.info(
            "No representatives added yet."
        )


    else:


        for rep in representatives:


            rep_id = rep["representative_id"]


            calendar = check_calendar_status(
                rep_id
            )


            with st.container(border=True):


                c1,c2,c3,c4,c5,c6 = st.columns(
                    [
                        1.2,
                        1.2,
                        2,
                        2,
                        1.2,
                        1
                    ]
                )


                with c1:

                    st.write("**Name**")
                    st.write(
                        rep.get(
                            "representative_name"
                        )
                    )


                with c2:

                    st.write("**Service**")
                    st.write(
                        rep.get(
                            "service"
                        )
                    )


                with c3:

                    st.write("**Email**")
                    st.write(
                        rep.get(
                            "company_email"
                        )
                    )


                with c4:

                    st.write("**Invitation**")

                    st.write(
                        rep.get(
                            "invitation_status",
                            "Pending"
                        )
                    )


                with c5:

                    st.write("**Calendar**")

                    st.write(
                        calendar.get(
                            "connection_status",
                            "Unknown"
                        )
                    )


                with c6:

                    st.write("**Action**")


                    if st.button(
                        "Delete",
                        key=f"del_{rep_id}"
                    ):

                        if delete_representative(rep_id):

                            st.success(
                                "Deleted"
                            )

                            st.rerun()



# ============================================================
# TAB 3 KNOWLEDGE BASE
# ============================================================

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


        st.success(
            "Setup complete!"
        )


        st.switch_page(
            "portal/3_dashboard.py"
        )


    except Exception as e:

        st.error(
            f"Fail ho gaya ({e})"
        )