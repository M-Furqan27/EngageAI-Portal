import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>

        /* =========================================================
           ENGAGEAI — GLOBAL DESIGN SYSTEM
           ========================================================= */

        :root {
            --ea-bg: #0B0F14;
            --ea-surface: #111720;
            --ea-surface-2: #161D27;
            --ea-surface-3: #1B2430;

            --ea-border: rgba(255, 255, 255, 0.08);
            --ea-border-hover: rgba(255, 75, 62, 0.35);

            --ea-text: #F5F7FA;
            --ea-text-secondary: #A7B0BE;
            --ea-text-muted: #737D8C;

            --ea-primary: #FF4B3E;
            --ea-primary-hover: #FF6257;
            --ea-primary-soft: rgba(255, 75, 62, 0.12);

            --ea-success: #22C55E;
            --ea-warning: #F59E0B;
            --ea-danger: #EF4444;
            --ea-info: #3B82F6;

            --ea-radius: 14px;
            --ea-radius-small: 10px;

            --ea-shadow:
                0 10px 30px rgba(0, 0, 0, 0.22);
        }


        /* =========================================================
           GLOBAL APP
           ========================================================= */

        .stApp {
            background:
                radial-gradient(
                    circle at 85% 0%,
                    rgba(255, 75, 62, 0.055),
                    transparent 28%
                ),
                var(--ea-bg);
            color: var(--ea-text);
        }


        /* Main content width / spacing */

        .block-container {
            max-width: 1450px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }


        /* =========================================================
           TYPOGRAPHY
           ========================================================= */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--ea-text) !important;
            letter-spacing: -0.025em;
            font-weight: 700;
        }

        h1 {
            font-size: 2.15rem !important;
        }

        h2 {
            font-size: 1.55rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
        }

        p,
        label,
        span {
            color: inherit;
        }

        [data-testid="stCaptionContainer"] p {
            color: var(--ea-text-muted);
            letter-spacing: 0.01em;
        }


        /* =========================================================
           SIDEBAR
           ========================================================= */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #0E141C 0%,
                    #0A0F15 100%
                );

            border-right: 1px solid var(--ea-border);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.2rem;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: var(--ea-text-secondary);
        }


        /* Sidebar navigation */

        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 10px;
            margin: 3px 8px;
            transition:
                background 0.18s ease,
                color 0.18s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: var(--ea-primary-soft);
            color: var(--ea-text);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background:
                linear-gradient(
                    90deg,
                    rgba(255, 75, 62, 0.18),
                    rgba(255, 75, 62, 0.07)
                );
            color: #FFFFFF;
            border-left: 3px solid var(--ea-primary);
        }


        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button,
        .stFormSubmitButton > button {
            min-height: 42px;
            border-radius: var(--ea-radius-small);
            border: 1px solid var(--ea-border);
            background: var(--ea-surface-2);
            color: var(--ea-text);
            font-weight: 650;

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease,
                border-color 0.15s ease,
                background 0.15s ease;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            border-color: var(--ea-border-hover);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
            background: var(--ea-surface-3);
        }


        /* Primary buttons */

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    var(--ea-primary),
                    #E63E33
                );

            border-color: transparent;
            color: #FFFFFF;

            box-shadow:
                0 8px 22px rgba(255, 75, 62, 0.20);
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background:
                linear-gradient(
                    135deg,
                    var(--ea-primary-hover),
                    var(--ea-primary)
                );

            box-shadow:
                0 10px 28px rgba(255, 75, 62, 0.28);
        }


        /* =========================================================
           INPUTS
           ========================================================= */

        div[data-baseweb="input"],
        div[data-baseweb="textarea"],
        div[data-baseweb="select"] {
            background: var(--ea-surface-2);
            border-radius: var(--ea-radius-small);
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="select"] > div {
            background: transparent;
            border-color: var(--ea-border);
            border-radius: var(--ea-radius-small);
        }

        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="textarea"]:focus-within,
        div[data-baseweb="select"]:focus-within {
            border-color: rgba(255, 75, 62, 0.55);
            box-shadow:
                0 0 0 1px rgba(255, 75, 62, 0.20);
        }

        input,
        textarea {
            color: var(--ea-text) !important;
        }


        /* =========================================================
           CARDS / CONTAINERS
           ========================================================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(22, 29, 39, 0.95),
                    rgba(15, 21, 29, 0.95)
                );

            border:
                1px solid var(--ea-border) !important;

            border-radius:
                var(--ea-radius) !important;

            box-shadow:
                var(--ea-shadow);

            transition:
                border-color 0.18s ease,
                transform 0.18s ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color:
                rgba(255, 255, 255, 0.12) !important;
        }


        /* =========================================================
           METRICS
           ========================================================= */

        div[data-testid="stMetric"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(22, 29, 39, 0.96),
                    rgba(16, 21, 29, 0.96)
                );

            border:
                1px solid var(--ea-border);

            border-radius:
                var(--ea-radius);

            padding:
                1.15rem 1.2rem;

            box-shadow:
                var(--ea-shadow);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--ea-text-muted) !important;
        }

        div[data-testid="stMetricValue"] {
            color: var(--ea-text) !important;
            font-weight: 750;
        }


        /* =========================================================
           TABS
           ========================================================= */

        button[data-baseweb="tab"] {
            color: var(--ea-text-muted);
            font-weight: 600;
        }

        button[data-baseweb="tab"]:hover {
            color: var(--ea-text);
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--ea-primary);
        }

        div[data-baseweb="tab-highlight"] {
            background: var(--ea-primary);
        }


        /* =========================================================
           EXPANDERS
           ========================================================= */

        div[data-testid="stExpander"] {
            background: var(--ea-surface);
            border: 1px solid var(--ea-border);
            border-radius: var(--ea-radius);
            overflow: hidden;
        }

        div[data-testid="stExpander"]:hover {
            border-color: rgba(255, 255, 255, 0.12);
        }


        /* =========================================================
           ALERTS
           ========================================================= */

        div[data-testid="stAlert"] {
            border-radius: var(--ea-radius-small);
            border: 1px solid var(--ea-border);
        }


        /* =========================================================
           FILE UPLOADER
           ========================================================= */

        section[data-testid="stFileUploaderDropzone"] {
            background: var(--ea-surface-2);
            border: 1px dashed rgba(255, 255, 255, 0.16);
            border-radius: var(--ea-radius);
        }

        section[data-testid="stFileUploaderDropzone"]:hover {
            border-color: var(--ea-primary);
            background: var(--ea-primary-soft);
        }


        /* =========================================================
           DIVIDERS
           ========================================================= */

        hr {
            border-color:
                rgba(255, 255, 255, 0.07) !important;
        }


        /* =========================================================
           RADIO / CHECKBOX
           ========================================================= */

        div[data-testid="stRadio"] label,
        div[data-testid="stCheckbox"] label {
            color: var(--ea-text-secondary);
        }


        /* =========================================================
           DATAFRAME / TABLE
           ========================================================= */

        div[data-testid="stDataFrame"] {
            border:
                1px solid var(--ea-border);

            border-radius:
                var(--ea-radius);

            overflow: hidden;
        }


        /* =========================================================
           ACCOUNT SIDEBAR CARD
           ========================================================= */

        .account-card {
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 75, 62, 0.10),
                    rgba(22, 29, 39, 0.90)
                );

            border:
                1px solid rgba(255, 75, 62, 0.18);

            border-radius:
                var(--ea-radius);

            padding:
                1rem;

            margin-top:
                0.75rem;
        }


        /* =========================================================
           FOOTER
           ========================================================= */

        .app-footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top:
                1px solid var(--ea-border);
        }

        .app-footer a {
            color: var(--ea-text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            line-height: 2.1;
            transition: color 0.15s ease;
        }

        .app-footer a:hover {
            color: var(--ea-primary);
        }

        .app-footer .footer-heading {
            color: var(--ea-text);
            font-weight: 700;
            font-size: 0.82rem;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }

        .app-footer .footer-bottom {
            margin-top: 2rem;
            padding-top: 1.2rem;
            border-top:
                1px solid rgba(255, 255, 255, 0.06);

            color: var(--ea-text-muted);
            font-size: 0.82rem;
        }


        /* =========================================================
           SCROLLBAR
           ========================================================= */

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--ea-bg);
        }

        ::-webkit-scrollbar-thumb {
            background: #303946;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #465161;
        }


        /* =========================================================
           MOBILE
           ========================================================= */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.2rem;
            }

            h1 {
                font-size: 1.75rem !important;
            }

            h2 {
                font-size: 1.35rem !important;
            }

            div[data-testid="stMetric"] {
                padding: 0.9rem;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def anchor(section_id: str):
    st.markdown(
        f'<div id="{section_id}"></div>',
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        '<div class="app-footer">',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            '<div class="footer-heading">EngageAI</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Your business never closes. "
            "Now your front desk doesn't either."
        )

    with c2:
        st.markdown(
            '<div class="footer-heading">Product</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<a href="#top">Home</a><br>'
            '<a href="#services">Services</a><br>'
            '<a href="#about">About</a>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            '<div class="footer-heading">Account</div>',
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "Log in",
                key="footer_login",
                use_container_width=True,
            ):
                st.switch_page("portal/1_login.py")

        with b2:
            if st.button(
                "Sign up",
                key="footer_signup",
                use_container_width=True,
            ):
                st.switch_page("portal/2_signup.py")

    with c4:
        st.markdown(
            '<div class="footer-heading">Contact</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<a href="#contact">Get in touch</a><br>'
            '<a href="mailto:hello@engageai.app">'
            'hello@engageai.app'
            '</a>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="footer-bottom">'
        '© 2026 EngageAI · Built for the Mari Energies Bootcamp — '
        'AI &amp; Agentic Development'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )