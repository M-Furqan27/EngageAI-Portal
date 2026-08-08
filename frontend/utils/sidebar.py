import streamlit as st


def render_account_sidebar():
    """
    Minimal professional EngageAI sidebar.
    Navigation is handled by Streamlit's navigation system.
    """

    user = st.session_state.get("user") or {}

    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")

    name = f"{first_name} {last_name}".strip() or "User"

    role = user.get("role", "Owner")

    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        st.markdown(
            "## ✨ EngageAI"
        )

        st.markdown(
            "<div style='height:0.5rem'></div>",
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # ACCOUNT AREA
        # ----------------------------------------------------

        st.markdown(
            "<div style='height:8rem'></div>",
            unsafe_allow_html=True,
        )

        st.divider()

        # ----------------------------------------------------
        # USER
        # ----------------------------------------------------

        st.markdown(
            f"👤 **{name}**"
        )

        st.caption(
            role.title()
        )

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        if st.button(
            "🚪  Log out",
            use_container_width=True,
            key="sidebar_logout",
        ):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.onboarding_completed = False

            st.rerun()