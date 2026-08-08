"""
frontend/utils/theme.py

Global look-and-feel helpers — ek hi jagah se poori app (Home, Login,
Signup, Onboarding, Dashboard, Profile, Admin) ka polish control hota
hai. app.py isay sabse pehle call karta hai, isliye har page automatically
isi CSS/branding ke sath render hoti hai.
"""

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
            /* ---- Typography ---- */
            h1, h2, h3 { letter-spacing: -0.02em; }
            [data-testid="stCaptionContainer"] p {
                letter-spacing: 0.06em;
            }

            /* ---- Buttons: rounded, subtle hover lift ---- */
            .stButton > button {
                border-radius: 10px;
                font-weight: 600;
                transition: transform 0.12s ease, box-shadow 0.12s ease;
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 14px rgba(255, 75, 62, 0.25);
            }

            /* ---- Bordered containers (cards): soften + shadow ---- */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 14px !important;
            }

            /* ---- Footer ---- */
            .app-footer {
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 1px solid rgba(250, 250, 250, 0.12);
            }
            .app-footer a {
                color: #C9CDD3;
                text-decoration: none;
                font-size: 0.92rem;
                line-height: 2.1;
            }
            .app-footer a:hover { color: #FF4B3E; }
            .app-footer .footer-heading {
                color: #FAFAFA;
                font-weight: 700;
                font-size: 0.85rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 0.6rem;
            }
            .app-footer .footer-bottom {
                margin-top: 2rem;
                padding-top: 1.2rem;
                border-top: 1px solid rgba(250, 250, 250, 0.08);
                color: #8A8F98;
                font-size: 0.85rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def anchor(section_id: str):
    """Home page ke andar ek invisible marker — footer ke anchor links
    (#services, #about, #contact) isi id par scroll karte hain."""
    st.markdown(f'<div id="{section_id}"></div>', unsafe_allow_html=True)


def render_footer():
    st.markdown('<div class="app-footer">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="footer-heading">EngageAI</div>', unsafe_allow_html=True)
        st.caption("Your business never closes. Now your front desk doesn't either.")

    with c2:
        st.markdown('<div class="footer-heading">Product</div>', unsafe_allow_html=True)
        st.markdown(
            '<a href="#top">Home</a><br>'
            '<a href="#services">Services</a><br>'
            '<a href="#about">About</a>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown('<div class="footer-heading">Account</div>', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        if b1.button("Log in", key="footer_login", use_container_width=True):
            st.switch_page("portal/1_login.py")
        if b2.button("Sign up", key="footer_signup", use_container_width=True):
            st.switch_page("portal/2_signup.py")

    with c4:
        st.markdown('<div class="footer-heading">Contact</div>', unsafe_allow_html=True)
        st.markdown(
            '<a href="#contact">Get in touch</a><br>'
            '<a href="mailto:hello@engageai.app">hello@engageai.app</a>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="footer-bottom">© 2026 EngageAI · Built for the Mari Energies Bootcamp — '
        'AI &amp; Agentic Development</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)
