import streamlit as st
from utils.theme import inject_custom_css, anchor, render_footer

st.set_page_config(page_title="AI Chatbot Platform", page_icon="🟠", layout="wide")

inject_custom_css()

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.user = None
if "onboarding_completed" not in st.session_state:
    st.session_state.onboarding_completed = False


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
# FEATURES — 3 cards ("Services")
# ============================================================
def features_section():
    anchor("services")
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
# ABOUT
# ============================================================
def about_section():
    anchor("about")
    st.caption("ABOUT US")
    st.header("Built for businesses that never stop")

    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.write(
            "EngageAI ek AI-powered customer engagement platform hai jo "
            "chhoti aur medium businesses ko unke leads, representatives, "
            "knowledge base aur meetings ek hi jagah se manage karne mein "
            "madad deta hai — bina extra headcount ke."
        )
        st.write(
            "Hamara maqsad simple hai: har business ka front desk 24/7 "
            "chalta rahe, chahe office band ho ya khula."
        )
    with right:
        with st.container(border=True):
            st.markdown("**Why EngageAI**")
            st.caption("✔ Setup in under 10 minutes")
            st.caption("✔ No credit card required to start")
            st.caption("✔ Built for Sales, Support & Finance teams")
            st.caption("✔ Your data, your organization, always")


# ============================================================
# CONTACT
# ============================================================
def contact_section():
    anchor("contact")
    st.caption("CONTACT")
    st.header("Get in touch")

    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**📧 Email**")
            st.caption("hello@engageai.app")
    with c2:
        with st.container(border=True):
            st.markdown("**📞 Phone**")
            st.caption("+92 300 0000000")
    with c3:
        with st.container(border=True):
            st.markdown("**📍 Location**")
            st.caption("Sindh, Pakistan")


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
    anchor("top")
    hero_section()
    st.divider()
    sequence_section()
    st.divider()
    features_section()
    st.divider()
    about_section()
    st.divider()
    contact_section()
    st.divider()
    cta_section()
    render_footer()


# ============================================================
# NAVIGATION
# ============================================================
home = st.Page(home_page, title="Home", icon="🏠", default=True)
login_page = st.Page("portal/1_login.py", title="Log in", icon="🔑", url_path="login")
signup_page = st.Page("portal/2_signup.py", title="Sign up", icon="🆕", url_path="signup")
onboarding_page = st.Page("portal/0_onboarding.py", title="Onboarding", icon="👋", url_path="onboarding")
admin_page = st.Page("admin_portal/1_profiles.py", title="Admin", icon="🛠️", url_path="admin")
dashboard_page = st.Page("portal/3_dashboard.py", title="Dashboard", icon="📊", url_path="dashboard")
profile_page = st.Page("portal/4_profile.py", title="Profile", icon="🏢", url_path="profile")

is_logged_in = st.session_state.token is not None
onboarding_done = st.session_state.onboarding_completed
is_admin = is_logged_in and st.session_state.user and st.session_state.user.get("role") == "admin"

if not is_logged_in:
    # Home + Login/Signup normal sidebar mein dikhte hain. Onboarding/
    # Dashboard/Profile/Admin bhi ROUTING ke liye isi list mein shamil
    # hain (taake koi in ka direct link khole to us page ka apna
    # require_login() chal ke Login par bhej sake) — lekin CSS se unhe
    # sidebar mein chhupa dete hain, sirf Home/Login/Signup dikhte hain.
    st.markdown(
        """
        <style>
            a[href$="/onboarding"],
            a[href$="/dashboard"],
            a[href$="/profile"],
            a[href$="/admin"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    nav_pages = {
        "": [home],
        "Account": [login_page, signup_page, onboarding_page, dashboard_page, profile_page, admin_page],
    }
elif is_logged_in and not onboarding_done:
    # Login ho gaya lekin onboarding baaki — sirf onboarding show hoga
    nav_pages = {"Setup": [onboarding_page]}
else:
    # Onboarding complete — sirf dashboard + profile (+ admin agar role admin hai)
    pages = [dashboard_page, profile_page]
    if is_admin:
        pages.append(admin_page)
    nav_pages = {"Workspace": pages}

pg = st.navigation(nav_pages)
pg.run()