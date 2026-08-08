import streamlit as st


def render_account_sidebar():
    """Render a compact professional logged-in user section."""

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

        # ----------------------------------------------------
        # Brand
        # ----------------------------------------------------

        st.markdown("## ✨ EngageAI")

        st.divider()

        # ----------------------------------------------------
        # Logged-in user card
        # ----------------------------------------------------

        st.markdown(
            f"""
<div style="
    padding: 14px;
    border-radius: 14px;
    background: linear-gradient(
        145deg,
        rgba(255,75,62,0.10),
        rgba(22,29,39,0.90)
    );
    border: 1px solid rgba(255,255,255,0.08);
">

    <div style="
        display:flex;
        align-items:center;
        gap:11px;
    ">

        <div style="
            width:42px;
            height:42px;
            min-width:42px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            background:linear-gradient(
                135deg,
                #8B5CF6,
                #6D28D9
            );
            color:white;
            font-size:14px;
            font-weight:800;
        ">
            {initials}
        </div>

        <div style="min-width:0;">

            <div style="
                color:#F5F7FA;
                font-size:0.88rem;
                font-weight:700;
                white-space:nowrap;
                overflow:hidden;
                text-overflow:ellipsis;
            ">
                {name}
            </div>

            <div style="
                color:#858E9C;
                font-size:0.70rem;
                margin-top:3px;
            ">
                {role.title()} · Signed in
            </div>

        </div>

    </div>

    <div style="
        margin-top:12px;
        padding-top:10px;
        border-top:1px solid rgba(255,255,255,0.06);
        color:#22C55E;
        font-size:0.70rem;
        font-weight:600;
    ">
        ● Active session
    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:0.65rem'></div>",
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # Logout
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