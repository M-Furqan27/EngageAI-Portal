import streamlit as st

st.set_page_config(page_title="AI Chatbot Platform", page_icon="🟠", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.user = None


# ============================================================
# HERO — headline + live chat mockup (st.chat_message se, koi custom CSS nahi)
# ============================================================
def hero_section():
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.caption("● ONLINE SINCE 12:00 AM")
        st.title("Your business never closes. Now your front desk doesn't either.")
        st.write(
           "EngageAI helps organizations manage representatives, knowledge base,employees, leads and meetings from one centralized platform."
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Get started free →", type="primary", use_container_width=True):
                st.switch_page("portal/2_signup.py")
        with c2:
            if st.button("Log in", use_container_width=True):
                st.switch_page("portal/1_login.py")
        st.caption("No credit card required · Live on your website in under 10 minutes")

    with right:
        with st.container(border=True):
            st.subheader("Platform Overview")

            st.success("✔ Organization Created")
            st.success("✔ Representatives Added")
            st.success("✔ Knowledge Base Ready")
            st.success("✔ Employees Managed")
            st.success("✔ Lead Tracking")
            st.success("✔ Meeting Scheduling")


# ============================================================
# SEQUENCE — "What happens after hours" 4 steps
# ============================================================
def sequence_section():
    st.caption("WHILE YOU SLEEP")
    st.header("What happens after hours")
    st.caption("One conversation, four things handled automatically.")

    steps = [
        ("1", "Create Organization", "A question comes in through your website's chat widget, any time of day."),
        ("2", "Complete Onboarding", "Grounded in your own documents, pricing, and policies — not generic guesses."),
        ("3", "Add Representatives", "Captured and sent to the right department — Sales, Support, or Finance."),
        ("4", "Upload Knowledge Base", "Straight onto your teammate's calendar. Both sides get confirmed automatically."),
    ]
    cols = st.columns(4)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            with st.container(border=True):
                st.subheader(num)
                st.markdown(f"**{title}**")
                st.caption(desc)


# ============================================================
# FEATURES — 3 cards
# ============================================================
def features_section():
    st.caption("INSIDE YOUR DASHBOARD")
    st.header("Everything in one view")

    features = [
        ("Knowledge base", "Teach it your business",
         "Store PDFs, documents and website links for your organization.."),
        ("Lead management", "Track customer leads and manage their status., tracked",
         "See who talked to your AI, what they asked, and where they are in your pipeline."),
        ("Team & calendars", "Employees & Representatives",
         "Assign roles across Sales, Support, and Finance — each with their own calendar and queue."),
    ]
    cols = st.columns(3)
    for col, (tag, title, desc) in zip(cols, features):
        with col:
            with st.container(border=True):
                st.caption(tag.upper())
                st.markdown(f"**{title}**")
                st.caption(desc)


# ============================================================
# CTA BAND
# ============================================================
def cta_section():
    with st.container(border=True):
        st.subheader("Start managing your organization from one platform.")
        st.caption("Create your organization and start using EngageAI today.")
        _, mid, _ = st.columns([1, 1, 1])
        with mid:
            if st.button("Create your account →", type="primary", use_container_width=True):
                st.switch_page("portal/2_signup.py")


# ============================================================
# HOME PAGE
# ============================================================
def home_page():
    hero_section()
    st.divider()
    sequence_section()
    st.divider()
    features_section()
    st.divider()
    cta_section()
    st.caption("© 2026 EngageAI · Built for the Mari Energies Bootcamp — AI & Agentic Development")


# ============================================================
# NAVIGATION
# ============================================================
home = st.Page(home_page, title="Home", icon="🏠", default=True)
login_page = st.Page("portal/1_login.py", title="Log in", icon="🔑")
signup_page = st.Page("portal/2_signup.py", title="Sign up", icon="🆕")
onboarding_page = st.Page("portal/0_onboarding.py", title="Onboarding", icon="👋")
admin_page = st.Page("admin_portal/1_profiles.py", title="Admin", icon="🛠️")
dashboard_page = st.Page("portal/3_dashboard.py", title="Dashboard", icon="📊")
profile_page = st.Page("portal/4_profile.py", title="Profile", icon="🏢")
# representatives_page = st.Page("portal/5_representatives.py", title="Representatives", icon="🧑‍💼")

pg = st.navigation({
    "": [home],
    "Account": [login_page, signup_page, onboarding_page, admin_page, dashboard_page, profile_page],
    # "Widget" group hataya — chat_widget.py page ab navigation mein nahi
})

pg.run()