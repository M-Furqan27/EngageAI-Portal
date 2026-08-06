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

    st.subheader(
        "Add your team representatives"
    )


    with st.form(
        "add_representative_form"
    ):

        rep_name = st.text_input(
            "Representative name *"
        )


        rep_service = st.text_input(
            "Service *",
            placeholder="Sales"
        )


        rep_desc = st.text_area(
            "Service description"
        )


        rep_email = st.text_input(
            "Company email *"
        )


        add_rep = st.form_submit_button(
            "Add Representative →",
            type="primary"
        )



    if add_rep:

        if not all(
            [
                rep_name,
                rep_service,
                rep_email
            ]
        ):

            st.error(
                "Required fields fill karein."
            )


        else:

            try:

                api_client.create_representative(
                    {
                        "representative_name": rep_name,
                        "service": rep_service,
                        "service_description": rep_desc,
                        "company_email": rep_email
                    }
                )


                st.success(
                    "Representative added!"
                )

                st.rerun()


            except Exception as e:

                st.error(
                    f"Add fail ho gaya. ({e})"
                )



    st.divider()


    try:

        reps = api_client.list_representatives()


    except Exception as e:

        reps = []

        st.error(
            f"Representatives load nahi huay. ({e})"
        )



    if reps:


        for rep in reps:


            with st.container(border=True):


                st.markdown(
                    f"**{rep.get('representative_name','Unknown')}**"
                )


                st.caption(
                    rep.get(
                        "company_email",
                        ""
                    )
                )


    else:

        st.info(
            "Abhi koi representative add nahi hua."
        )



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

                    st.caption(
                        source_name
                    )


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