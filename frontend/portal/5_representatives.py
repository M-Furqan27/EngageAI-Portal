"""
frontend/portal/5_representatives.py

Representatives ka ongoing management page (onboarding ke baad bhi).
Onboarding wizard (0_onboarding.py) mein sirf ek-baar-wala 'add representative'
tab tha — ye page ussi list/create logic ko dashboard ke andar se hamesha
accessible banata hai, taake Owner baad mein bhi naye representatives add
kar sake aur mojooda list dekh sake.
"""

import streamlit as st
from utils import api_client

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()

st.title("🧑‍💼 Representatives")
st.caption("Ye log leads ke sath deal karte hain — jaise Sales, Support, Finance.")

# ============================================================
# ADD REPRESENTATIVE FORM
# ============================================================
with st.expander("➕ Naya Representative Add Karein", expanded=False):
    with st.form("add_representative_form_main"):
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

# ============================================================
# LIST REPRESENTATIVES
# ============================================================
try:
    reps = api_client.list_representatives()
except Exception as e:
    reps = []
    st.error(f"Representatives load nahi ho sake. ({e})")

if reps:
    st.caption(f"{len(reps)} representative(s):")
    for rep in reps:
        with st.container(border=True):
            col1, col2 = st.columns([2.5, 2])
            with col1:
                st.markdown(f"**{rep['representative_name']}**")
                st.caption(rep["company_email"])
            with col2:
                st.caption("Service / Department")
                st.write(rep.get("service", "—"))
            if rep.get("service_description"):
                st.caption(rep["service_description"])
else:
    st.info("Abhi koi representative add nahi hua. Upar 'Add Representative' se pehla representative banayein.")
