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



import streamlit as st
from utils import api_client


st.set_page_config(
    page_title="Profile",
    page_icon="🏢",
    layout="wide"
)


# =========================
# AUTH
# =========================

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()



# =========================
# STATE
# =========================

if "profile_edit_mode" not in st.session_state:
    st.session_state.profile_edit_mode = False



# =========================
# LOAD ORGANIZATION DATA
# =========================

try:

    organization = api_client.get_organization_profile()

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
    "Manage your complete organization setup."
)



# =========================
# VIEW MODE
# =========================

if not st.session_state.profile_edit_mode:


    st.subheader(
        "Business Information"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write("**Business Type**")

        st.write(
            organization.get(
                "business_type",
                "-"
            )
        )


        st.write("**Website**")

        st.write(
            organization.get(
                "website",
                "-"
            )
        )


        st.write("**Business Email**")

        st.write(
            organization.get(
                "business_email",
                "-"
            )
        )



    with col2:


        st.write("**Phone**")

        st.write(
            organization.get(
                "business_phone",
                "-"
            )
        )


        st.write("**Country**")

        st.write(
            organization.get(
                "country",
                "-"
            )
        )


        st.write("**Address**")

        st.write(
            organization.get(
                "address",
                "-"
            )
        )


    st.write(
        "**Description**"
    )

    st.write(
        organization.get(
            "description",
            "-"
        )
    )



    st.divider()



    if st.button(
        "✏️ Edit Profile",
        type="primary",
        use_container_width=True
    ):

        st.session_state.profile_edit_mode = True

        st.rerun()



# =========================
# EDIT MODE
# =========================

else:


    st.subheader(
        "Edit Profile"
    )


    business_type = st.text_input(
        "Business Type",
        value=organization.get(
            "business_type",
            ""
        )
    )


    website = st.text_input(
        "Website",
        value=organization.get(
            "website",
            ""
        )
    )


    business_email = st.text_input(
        "Business Email",
        value=organization.get(
            "business_email",
            ""
        )
    )


    business_phone = st.text_input(
        "Business Phone",
        value=organization.get(
            "business_phone",
            ""
        )
    )


    country = st.text_input(
        "Country",
        value=organization.get(
            "country",
            ""
        )
    )


    address = st.text_area(
        "Address",
        value=organization.get(
            "address",
            ""
        )
    )


    description = st.text_area(
        "Description",
        value=organization.get(
            "description",
            ""
        )
    )


    st.divider()


    if st.button(
        "💾 Save Changes",
        type="primary",
        use_container_width=True
    ):


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
                "Profile updated successfully!"
            )


            st.session_state.profile_edit_mode = False

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
    "🧑‍💼 Representatives"
)


try:

    representatives = api_client.list_representatives()

except Exception as e:

    representatives = []

    st.error(
        f"Representatives load nahi ho sake ({e})"
    )



if representatives:


    for rep in representatives:

        with st.container(border=True):

            col1, col2, col3 = st.columns(3)


            with col1:

                st.write(
                    "**Name**"
                )

                st.write(
                    rep.get(
                        "representative_name",
                        "-"
                    )
                )


            with col2:

                st.write(
                    "**Service**"
                )

                st.write(
                    rep.get(
                        "service",
                        "-"
                    )
                )


            with col3:

                st.write(
                    "**Email**"
                )

                st.write(
                    rep.get(
                        "company_email",
                        "-"
                    )
                )


else:

    st.info(
        "No representatives added yet."
    )



# =========================
# ADD REPRESENTATIVE
# ONLY EDIT MODE
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


            if not representative_name:
                
                st.error(
                    "Representative name required"
                )


            elif not service:

                st.error(
                    "Service required"
                )


            elif not company_email:

                st.error(
                    "Email required"
                )


            else:


                payload = {

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
                        f"Failed ({e})"
                    )            