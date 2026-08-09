"""
frontend/utils/theme.py

EngageAI Design System — ek hi jagah se poori app (Home, Login, Signup,
Onboarding, Dashboard, Profile, Admin) ka look control hota hai.

Palette: Indigo → Violet gradient (primary), Teal (accent), deep navy
background — professional SaaS look (Linear / Notion / Stripe jaisa).

Usage:
    from utils.theme import inject_custom_css, page_header, badge, render_footer
    inject_custom_css()                 # sabse pehle, har page ke top par
    page_header("📊", "Dashboard", "Welcome back, Ali")
    badge("Connected", "success")
"""

import streamlit as st

# ----------------------------------------------------------------------
# PALETTE — single source of truth. Rang badalna ho to sirf yahan badlo.
# ----------------------------------------------------------------------
COLORS = {
    "primary": "#6366F1",       # Indigo
    "primary_dark": "#4F46E5",
    "accent": "#8B5CF6",        # Violet
    "teal": "#2DD4BF",          # Secondary accent
    "bg": "#0A0E1A",
    "bg_card": "#12162A",
    "bg_card_hover": "#161B33",
    "border": "rgba(255,255,255,0.08)",
    "text": "#F1F3F9",
    "text_muted": "#8B92A8",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
}


def inject_custom_css():
    st.markdown(
        f"""
        <style>
            :root {{
                --ea-primary: {COLORS['primary']};
                --ea-primary-dark: {COLORS['primary_dark']};
                --ea-accent: {COLORS['accent']};
                --ea-teal: {COLORS['teal']};
                --ea-bg-card: {COLORS['bg_card']};
                --ea-bg-card-hover: {COLORS['bg_card_hover']};
                --ea-border: {COLORS['border']};
                --ea-text-muted: {COLORS['text_muted']};
            }}

            /* ================= TYPOGRAPHY ================= */
            h1, h2, h3 {{ letter-spacing: -0.02em; font-weight: 700; }}
            [data-testid="stCaptionContainer"] p {{ letter-spacing: 0.02em; }}

            /* ================= APP BACKGROUND ================= */
            [data-testid="stAppViewContainer"] {{
                background: radial-gradient(circle at 15% 0%, rgba(99,102,241,0.08) 0%, transparent 45%),
                            radial-gradient(circle at 85% 20%, rgba(139,92,246,0.06) 0%, transparent 40%),
                            {COLORS['bg']};
            }}

            /* ================= BUTTONS ================= */
            .stButton > button {{
                border-radius: 10px;
                font-weight: 600;
                border: 1px solid var(--ea-border);
                transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;
            }}
            .stButton > button:hover {{
                transform: translateY(-1px);
                border-color: var(--ea-primary);
                box-shadow: 0 6px 18px rgba(99, 102, 241, 0.28);
            }}
            /* Primary (type="primary") buttons -> gradient fill */
            .stButton > button[kind="primary"] {{
                background: linear-gradient(135deg, var(--ea-primary) 0%, var(--ea-accent) 100%);
                border: none;
                color: white;
            }}
            .stButton > button[kind="primary"]:hover {{
                box-shadow: 0 8px 22px rgba(99, 102, 241, 0.45);
            }}

            /* ================= CARDS (bordered containers) ================= */
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                border-radius: 16px !important;
                border: 1px solid var(--ea-border) !important;
                background: var(--ea-bg-card) !important;
                transition: border-color 0.15s ease, box-shadow 0.15s ease;
            }}
            div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
                border-color: rgba(99, 102, 241, 0.35) !important;
                box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            }}

            /* ================= METRICS ================= */
            div[data-testid="stMetric"] {{
                background: var(--ea-bg-card);
                border: 1px solid var(--ea-border);
                border-radius: 14px;
                padding: 1rem 1.1rem;
            }}
            div[data-testid="stMetricValue"] {{
                background: linear-gradient(135deg, var(--ea-primary), var(--ea-accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
            }}

            /* ================= FORM INPUTS ================= */
            .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
                border-radius: 10px !important;
                border: 1px solid var(--ea-border) !important;
                background: rgba(255,255,255,0.02) !important;
                transition: border-color 0.12s ease, box-shadow 0.12s ease;
            }}
            .stTextInput input:focus, .stTextArea textarea:focus {{
                border-color: var(--ea-primary) !important;
                box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
            }}

            /* ================= EXPANDER ================= */
            div[data-testid="stExpander"] {{
                border-radius: 14px !important;
                border: 1px solid var(--ea-border) !important;
                background: var(--ea-bg-card) !important;
                overflow: hidden;
            }}

            /* ================= TABS ================= */
            button[data-baseweb="tab"] {{
                font-weight: 600;
            }}
            div[data-baseweb="tab-highlight"] {{
                background: linear-gradient(135deg, var(--ea-primary), var(--ea-accent)) !important;
            }}

            /* ================= SIDEBAR ================= */
            [data-testid="stSidebar"] {{
                background: #0D1120;
                border-right: 1px solid var(--ea-border);
            }}
            [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {{
                background: var(--ea-bg-card) !important;
            }}

            /* ---- Native page nav (Notion / Linear style) ---- */
            [data-testid="stSidebarNav"] {{
                padding-top: 0.5rem;
            }}
            [data-testid="stSidebarNav"] ul {{
                gap: 2px;
            }}
            [data-testid="stSidebarNav"] a,
            a[data-testid="stSidebarNavLink"] {{
                border-radius: 10px !important;
                margin: 1px 0.5rem;
                padding: 0.5rem 0.75rem !important;
                font-weight: 600;
                color: var(--ea-text-muted) !important;
                transition: background 0.12s ease, color 0.12s ease;
            }}
            [data-testid="stSidebarNav"] a:hover,
            a[data-testid="stSidebarNavLink"]:hover {{
                background: rgba(99, 102, 241, 0.10) !important;
                color: #F1F3F9 !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"],
            a[data-testid="stSidebarNavLink"][aria-current="page"] {{
                background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(139,92,246,0.16)) !important;
                color: #FFFFFF !important;
                border-left: 3px solid var(--ea-primary);
            }}
            [data-testid="stSidebarNavSeparator"],
            [data-testid="stSidebarNav"] > div > span {{
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.72rem;
                color: var(--ea-text-muted) !important;
            }}

            /* ================= BADGES (custom component) ================= */
            .ea-badge {{
                display: inline-flex;
                align-items: center;
                gap: 5px;
                padding: 3px 11px;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.01em;
            }}
            .ea-badge-success {{ background: rgba(34,197,94,0.15); color: {COLORS['success']}; border: 1px solid rgba(34,197,94,0.3); }}
            .ea-badge-warning {{ background: rgba(245,158,11,0.15); color: {COLORS['warning']}; border: 1px solid rgba(245,158,11,0.3); }}
            .ea-badge-danger  {{ background: rgba(239,68,68,0.15); color: {COLORS['danger']}; border: 1px solid rgba(239,68,68,0.3); }}
            .ea-badge-info    {{ background: rgba(59,130,246,0.15); color: {COLORS['info']}; border: 1px solid rgba(59,130,246,0.3); }}
            .ea-badge-neutral {{ background: rgba(255,255,255,0.06); color: {COLORS['text_muted']}; border: 1px solid var(--ea-border); }}

            /* ================= PAGE HEADER ================= */
            .ea-page-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 0.25rem;
            }}
            .ea-page-header-icon {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 46px;
                height: 46px;
                border-radius: 12px;
                background: linear-gradient(135deg, var(--ea-primary), var(--ea-accent));
                font-size: 1.4rem;
                margin-right: 14px;
            }}
            .ea-page-title {{
                font-size: 1.65rem;
                font-weight: 800;
                letter-spacing: -0.02em;
                color: #F5F6FA;
                margin: 0;
                line-height: 1.2;
            }}
            .ea-page-subtitle {{
                color: var(--ea-text-muted);
                font-size: 0.92rem;
                margin-top: 2px;
            }}

            /* ================= FOOTER ================= */
            .app-footer {{
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 1px solid var(--ea-border);
            }}
            .app-footer a {{
                color: #C9CDD3;
                text-decoration: none;
                font-size: 0.92rem;
                line-height: 2.1;
            }}
            .app-footer a:hover {{ color: var(--ea-primary); }}
            .app-footer .footer-heading {{
                color: #FAFAFA;
                font-weight: 700;
                font-size: 0.85rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 0.6rem;
            }}
            .app-footer .footer-bottom {{
                margin-top: 2rem;
                padding-top: 1.2rem;
                border-top: 1px solid rgba(250, 250, 250, 0.08);
                color: #8A8F98;
                font-size: 0.85rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# REUSABLE COMPONENTS — har page isay use kare taake look same rahe
# ----------------------------------------------------------------------

def page_header(icon: str, title: str, subtitle: str = ""):
    """Har page ke top par ek consistent branded header.
    Example: page_header("📊", "Dashboard", "Welcome back, Ali")"""
    st.markdown(
        f"""
        <div class="ea-page-header">
            <div style="display:flex; align-items:center;">
                <div class="ea-page-header-icon">{icon}</div>
                <div>
                    <p class="ea-page-title">{title}</p>
                    {f'<p class="ea-page-subtitle">{subtitle}</p>' if subtitle else ''}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(label: str, kind: str = "neutral", icon: str = "") -> None:
    """Renders a small pill badge. kind: success | warning | danger | info | neutral
    Example: badge("Connected", "success", "🟢")"""
    st.markdown(
        f'<span class="ea-badge ea-badge-{kind}">{icon + " " if icon else ""}{label}</span>',
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