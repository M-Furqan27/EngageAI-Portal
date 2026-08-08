import streamlit as st


def render_account_sidebar():
    """Render only the logged-in user's account section."""

    user = st.session_state.get("user") or {}

    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")

    name = f"{first_name} {last_name}".strip() or "User"
    role = user.get("role") or "Owner"

    with st.sidebar:

        # Space between navigation and account
        st.write("")

        st.divider()

        # Logged-in user
        st.markdown("👤")

        st.markdown(
            f"**{name}**"
        )

        st.caption(
            f"{role.title()} · Signed in"
        )

        st.success(
            "● Active session"
        )

        st.divider()

        # Logout
        if st.button(
            "🚪  Log out",
            use_container_width=True,
            key="sidebar_logout",
        ):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.onboarding_completed = False

            st.rerun()