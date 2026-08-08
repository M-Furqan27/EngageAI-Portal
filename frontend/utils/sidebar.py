import streamlit as st


def render_account_sidebar():
    """Render the logged-in user's professional account section."""

    user = st.session_state.get("user") or {}

    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")

    name = f"{first_name} {last_name}".strip() or "User"

    role = user.get("role") or "Owner"

    # Initials
    initials = "".join(
        part[0].upper()
        for part in name.split()
        if part
    )[:2] or "U"

    with st.sidebar:

        # ====================================================
        # ENGAGEAI BRAND
        # ====================================================

        st.markdown("## ✨ EngageAI")

        st.divider()

        # ====================================================
        # LOGGED-IN USER
        # ====================================================

        st.markdown("### 👤")

        st.markdown(
            f"**{name}**"
        )

        st.caption(
            f"{role.title()} · Signed in"
        )

        st.success(
            "● Active session"
        )

        # ====================================================
        # LOGOUT
        # ====================================================

        st.divider()

        if st.button(
            "🚪  Log out",
            use_container_width=True,
            key="sidebar_logout",
        ):

            st.session_state.token = None
            st.session_state.user = None
            st.session_state.onboarding_completed = False

            st.rerun()