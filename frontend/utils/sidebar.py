import streamlit as st


def render_account_sidebar():
    """
    Render the authenticated user's account information
    and logout control in the Streamlit sidebar.
    """

    user = st.session_state.get("user") or {}

    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")
    email = user.get("email", "")

    name = f"{first_name} {last_name}".strip()

    if not name:
        name = "Account"

    # ========================================================
    # ENGAGEAI BRAND
    # ========================================================

    st.sidebar.title("✨ EngageAI")

    st.sidebar.caption(
        "Business Portal"
    )

    st.sidebar.divider()

    # ========================================================
    # WORKSPACE
    # ========================================================

    st.sidebar.subheader("Workspace")

    st.sidebar.caption(
        "Use the navigation menu above to move between portal sections."
    )

    st.sidebar.divider()

    # ========================================================
    # ACCOUNT
    # ========================================================

    st.sidebar.subheader("Account")

    st.sidebar.write(
        f"👤 **{name}**"
    )

    if email:
        st.sidebar.caption(email)

    st.sidebar.success(
        "Account active"
    )

    # ========================================================
    # LOGOUT
    # ========================================================

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Log out",
        use_container_width=True,
        key="sidebar_logout",
    ):

        st.session_state.token = None
        st.session_state.user = None
        st.session_state.onboarding_completed = False

        st.rerun()