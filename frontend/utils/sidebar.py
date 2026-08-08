import streamlit as st


def render_account_sidebar():
    user = st.session_state.get("user") or {}

    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")

    name = f"{first_name} {last_name}".strip() or "Account"
    email = user.get("email", "")

    # Initials
    initials = "".join(
        part[0].upper()
        for part in name.split()
        if part
    )[:2] or "U"

    with st.sidebar:

        # =====================================================
        # BRAND
        # =====================================================

        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                padding:0.5rem 0.4rem 1.4rem 0.4rem;
            ">
                <div style="
                    width:38px;
                    height:38px;
                    border-radius:11px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:linear-gradient(135deg,#FF4B3E,#E63E33);
                    color:white;
                    font-size:17px;
                    font-weight:800;
                    box-shadow:0 7px 20px rgba(255,75,62,0.22);
                ">
                    E
                </div>

                <div>
                    <div style="
                        color:#F5F7FA;
                        font-size:1.05rem;
                        font-weight:750;
                        line-height:1.1;
                    ">
                        EngageAI
                    </div>

                    <div style="
                        color:#737D8C;
                        font-size:0.68rem;
                        margin-top:3px;
                    ">
                        Business Portal
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =====================================================
        # WORKSPACE
        # =====================================================

        st.markdown(
            """
            <div style="
                color:#737D8C;
                font-size:0.68rem;
                font-weight:700;
                letter-spacing:0.08em;
                text-transform:uppercase;
                padding:0.35rem 0.45rem 0.55rem 0.45rem;
            ">
                Workspace
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation buttons
        if st.button(
            "📊  Dashboard",
            use_container_width=True,
            key="sidebar_dashboard",
        ):
            st.switch_page("portal/3_dashboard.py")

        if st.button(
            "👤  Profile",
            use_container_width=True,
            key="sidebar_profile",
        ):
            st.switch_page("portal/4_profile.py")

        # =====================================================
        # SEPARATOR
        # =====================================================

        st.markdown(
            """
            <div style="
                height:1px;
                background:rgba(255,255,255,0.07);
                margin:1.1rem 0;
            "></div>
            """,
            unsafe_allow_html=True,
        )

        # =====================================================
        # ACCOUNT CARD
        # =====================================================

        st.markdown(
            f"""
            <div class="account-card">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                ">

                    <div style="
                        min-width:40px;
                        width:40px;
                        height:40px;
                        border-radius:50%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        background:rgba(255,75,62,0.14);
                        border:1px solid rgba(255,75,62,0.25);
                        color:#FF6257;
                        font-size:0.85rem;
                        font-weight:750;
                    ">
                        {initials}
                    </div>

                    <div style="
                        min-width:0;
                    ">

                        <div style="
                            color:#F5F7FA;
                            font-size:0.86rem;
                            font-weight:700;
                            white-space:nowrap;
                            overflow:hidden;
                            text-overflow:ellipsis;
                        ">
                            {name}
                        </div>

                        <div style="
                            color:#737D8C;
                            font-size:0.70rem;
                            margin-top:2px;
                            white-space:nowrap;
                            overflow:hidden;
                            text-overflow:ellipsis;
                        ">
                            {email}
                        </div>

                    </div>

                </div>

                <div style="
                    margin-top:0.85rem;
                    padding-top:0.75rem;
                    border-top:1px solid rgba(255,255,255,0.06);
                    color:#737D8C;
                    font-size:0.68rem;
                ">
                    ● Account active
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        # =====================================================
        # LOGOUT
        # =====================================================

        st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

        if st.button(
            "🚪  Log out",
            use_container_width=True,
            key="sidebar_logout_btn",
        ):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.onboarding_completed = False
            st.rerun()