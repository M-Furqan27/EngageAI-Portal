"""
frontend/portal/0_onboarding.py

NEW FILE. Pehli baar login karne ke baad ye page dikhta hai (login.py se
redirect hoke). 3 tabs: Organization -> Representatives -> Knowledge Base.
"Finish Setup" click karte hi onboarding_completed = True ho jata hai,
aur agli baar se login seedha dashboard pe le jayega — ye page dobara
nahi dikhega.
"""

import streamlit as st
from utils import api_client

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()

# Agar onboarding pehle se complete ho chuki hai, seedha dashboard bhej do —
# ye page URL se bhi dobara access na ho sake.
try:
    org = api_client.get_organization_profile()
    if org.get("onboarding_completed"):
        st.switch_page("portal/3_dashboard.py")
except Exception as e:
    st.error(f"Organization data load nahi ho saka. ({e})")
    st.stop()

st.title("👋 Welcome! Let's set up your business.")
st.caption("3 steps complete karein, phir aapka dashboard ready ho jayega.")

BUSINESS_TYPES = ["Retail", "Healthcare", "Education", "Services", "Other"]
COUNTRIES = [
    "Pakistan", "India", "Bangladesh", "United Arab Emirates", "Saudi Arabia",
    "United States", "United Kingdom", "Canada", "Australia", "Germany",
    "France", "China", "Japan", "Turkey", "Qatar", "Kuwait", "Oman",
    "Bahrain", "Malaysia", "Indonesia", "Sri Lanka", "Nepal", "Afghanistan",
    "Egypt", "South Africa", "Nigeria", "Other",
]

tab1, tab2, tab3 = st.tabs(["🏢 Organization", "🧑‍💼 Representatives", "📚 Knowledge Base"])

# ============================================================
# TAB 1 — Organization details
# ============================================================
with tab1:
    st.subheader("Complete your business profile")

    with st.form("onboarding_org_form"):
        business_type = st.selectbox(
            "Business type *", BUSINESS_TYPES,
            index=BUSINESS_TYPES.index(org["business_type"]) if org.get("business_type") in BUSINESS_TYPES else 0,
        )
        website = st.text_input("Website *", value=org.get("website") or "", placeholder="https://yourbusiness.com")
        business_email = st.text_input("Business email *", value=org.get("business_email") or "")
        business_phone = st.text_input("Business phone *", value=org.get("business_phone") or "", placeholder="+92 3001234567")
        country = st.selectbox(
            "Country *", COUNTRIES,
            index=COUNTRIES.index(org["country"]) if org.get("country") in COUNTRIES else None,
            placeholder="Select your country",
        )
        address = st.text_area("Address (optional)", value=org.get("address") or "")
        description = st.text_area("Short business description (optional)", value=org.get("description") or "")

        org_saved = st.form_submit_button("Save Organization →", type="primary")

    if org_saved:
        required = [business_type, website, business_email, business_phone, country]
        if not all(required):
            st.error("Sab required (*) fields bharna zaroori hai.")
        else:
            payload = {
                "business_type": business_type, "website": website,
                "business_email": business_email, "business_phone": business_phone,
                "country": country, "address": address, "description": description,
            }
            try:
                api_client.update_organization_profile(payload)
                st.success("Organization details saved! Ab 'Representatives' tab pe jayein →")
            except Exception as e:
                st.error(f"Save fail ho gaya. ({e})")

# ============================================================
# TAB 2 — Representatives
# ============================================================
with tab2:
    st.subheader("Add your team representatives")
    st.caption("Ye log leads ke sath deal karenge — jaise Sales, Support, Finance.")

    with st.form("add_representative_form"):
        rep_name = st.text_input("Representative name *")
        rep_service = st.text_input("Service / Department *", placeholder="e.g. Sales")
        rep_desc = st.text_area("Service description (optional)")
        rep_email = st.text_input("Company email *", placeholder="rep@yourbusiness.com")

        rep_added = st.form_submit_button("Add Representative →", type="primary")

    if rep_added:
        if not all([rep_name, rep_service, rep_email]):
            st.error("Sab required (*) fields bharna zaroori hai.")
        else:
            try:
                api_client.create_representative({
                    "representative_name": rep_name,
                    "service": rep_service,
                    "service_description": rep_desc,
                    "company_email": rep_email,
                })
                st.success(f"{rep_name} add ho gaye!")
                st.rerun()
            except Exception as e:
                st.error(f"Add fail ho gaya. ({e})")

    st.divider()
    try:
        reps = api_client.list_representatives()
    except Exception as e:
        reps = []
        st.error(f"Representatives load nahi ho sake. ({e})")

    if reps:
        st.caption(f"{len(reps)} representative(s) added:")
        for rep in reps:
            with st.container(border=True):
                st.markdown(f"**{rep['representative_name']}** — {rep.get('service', '—')}")
                st.caption(rep["company_email"])
    else:
        st.info("Abhi koi representative add nahi hua.")

# ============================================================
# TAB 3 — Knowledge Base
# ============================================================
with tab3:
    st.subheader("Teach your AI about your business")
    st.caption("Text, PDF, ya website URL upload karein.")

    kb_type = st.radio("Source type", ["Text", "PDF", "URL"], horizontal=True)

    if kb_type == "Text":
        text_content = st.text_area("Paste your content here")
        if st.button("Upload Text →", type="primary"):
            if text_content.strip():
                try:
                    api_client.upload_knowledge_text(text_content)
                    st.success("Text uploaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload fail ho gaya. ({e})")
            else:
                st.error("Content khali nahi ho sakta.")

    elif kb_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if st.button("Upload PDF →", type="primary"):
            if pdf_file:
                try:
                    api_client.upload_knowledge_pdf(pdf_file)
                    st.success("PDF uploaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload fail ho gaya. ({e})")
            else:
                st.error("Pehle PDF select karein.")

    elif kb_type == "URL":
        url = st.text_input("Website URL", placeholder="https://yourbusiness.com/faq")
        if st.button("Upload URL →", type="primary"):
            if url.strip():
                try:
                    api_client.upload_knowledge_url(url)
                    st.success("URL added!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload fail ho gaya. ({e})")
            else:
                st.error("URL khali nahi ho sakta.")

    st.divider()
    try:
        docs = api_client.list_knowledge()
    except Exception as e:
        docs = []
        st.error(f"Knowledge base load nahi ho saki. ({e})")

    if docs:
        st.caption(f"{len(docs)} source(s) added:")
        for doc in docs:
            with st.container(border=True):
                st.markdown(f"**{doc['source_type']}** — {doc['processing_status']}")
    else:
        st.info("Abhi koi knowledge source add nahi hua.")

# ============================================================
# FINISH SETUP
# ============================================================
st.divider()
st.caption("Jab teeno steps complete ho jayein, setup finish karein — ye page dobara nahi dikhega.")
if st.button("✅ Finish Setup & Go to Dashboard →", type="primary", use_container_width=True):
    try:
        api_client.complete_onboarding()
        st.success("Setup complete! Redirecting...")
        st.switch_page("portal/3_dashboard.py")
    except Exception as e:
        st.error(f"Fail ho gaya. ({e})")