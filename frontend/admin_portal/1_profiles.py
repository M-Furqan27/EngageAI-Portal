import streamlit as st
from utils import api_client

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()

st.title("🛠️ Admin — Employee Access")
st.caption("Apni organization ke employees ka status manage karein.")

# ============================================================
# ADD EMPLOYEE FORM
# ============================================================
with st.expander("➕ Naya Employee Add Karein", expanded=False):
    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First name *")
        last_name = col2.text_input("Last name *")

        email = st.text_input("Email *")
        phone = st.text_input("Phone *", placeholder="+92 3001234567")

        role = st.selectbox("Department *", ["Sales", "Finance", "Support"])

        password = st.text_input("Password *", type="password")
        confirm_password = st.text_input("Confirm password *", type="password")

        add_clicked = st.form_submit_button("Add Employee →", type="primary")

    if add_clicked:
        required = [first_name, last_name, email, phone, password]
        if not all(required):
            st.error("Sab required (*) fields bharna zaroori hai.")
        elif password != confirm_password:
            st.error("Password match nahi kar raha.")
        else:
            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "password": password,
                "role": role,
            }
            try:
                api_client.create_employee(payload)
                st.success(f"{first_name} {last_name} ({role}) add ho gaye!")
                st.rerun()
            except Exception as e:
                st.error(f"Employee add nahi ho saka. ({e})")

st.divider()

ROLES = ["All", "Sales", "Finance", "Support"]

# ---------------- filter ----------------
selected_role = st.selectbox("Department (role) se filter karein", ROLES)

st.divider()

# ---------------- fetch users ----------------
try:
    users = api_client.get_organization_users()
except Exception as e:
    st.error(f"Employees load nahi ho sake. ({e})")
    st.stop()

users = [u for u in users if u.get("role") != "Owner"]

if not users:
    st.info("Abhi koi employee nahi hai. Upar 'Add Employee' se pehla employee banayein.")
    st.stop()

if selected_role != "All":
    users = [u for u in users if u.get("role") == selected_role]

if not users:
    st.info(f"{selected_role} department mein koi employee nahi mila.")
    st.stop()

# ---------------- list ----------------
for user in users:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([2.5, 2, 1.5, 1.5])

        with col1:
            st.markdown(f"**{user['first_name']} {user['last_name']}**")
            st.caption(user["email"])

        with col2:
            st.caption("Department")
            st.write(user.get("role", "—"))

        with col3:
            st.caption("Status")
            if user["status"] == "Active":
                st.success("Active", icon="✅")
            else:
                st.error("Inactive", icon="⛔")

        with col4:
            st.caption(" ")
            if user["status"] == "Active":
                if st.button("Deactivate", key=f"deact_{user['user_id']}", use_container_width=True):
                    try:
                        api_client.toggle_user_status(user["user_id"], "Inactive")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Fail ho gaya. ({e})")
            else:
                if st.button("Activate", key=f"act_{user['user_id']}", type="primary", use_container_width=True):
                    try:
                        api_client.toggle_user_status(user["user_id"], "Active")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Fail ho gaya. ({e})")