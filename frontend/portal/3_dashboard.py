import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import api_client
from utils.sidebar import render_account_sidebar
from utils.theme import inject_custom_css
from utils.auth import require_login


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Dashboard | EngageAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
require_login()
render_account_sidebar()


# ============================================================
# DASHBOARD CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        /* Main dashboard spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Header */
        .dashboard-header {
            margin-bottom: 1.8rem;
        }

        .dashboard-title {
            font-size: 2rem;
            font-weight: 750;
            letter-spacing: -0.04em;
            margin-bottom: 0.2rem;
        }

        .dashboard-subtitle {
            color: #8f98a6;
            font-size: 0.95rem;
        }

        /* KPI cards */
        .kpi-card {
            background: linear-gradient(
                145deg,
                rgba(28, 33, 42, 0.96),
                rgba(19, 23, 30, 0.96)
            );
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 16px;
            padding: 1.15rem 1.2rem;
            min-height: 125px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.16);
            transition: all 0.2s ease;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 75, 62, 0.28);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
        }

        .kpi-label {
            color: #929aa7;
            font-size: 0.82rem;
            font-weight: 600;
            margin-bottom: 0.55rem;
        }

        .kpi-value {
            color: #f5f7fa;
            font-size: 1.85rem;
            font-weight: 750;
            line-height: 1;
        }

        .kpi-icon {
            float: right;
            font-size: 1.3rem;
            opacity: 0.9;
        }

        /* Section title */
        .section-title {
            color: #f5f7fa;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.9rem;
        }

        /* Pipeline cards */
        .pipeline-card {
            background: rgba(22, 27, 35, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            min-height: 100px;
        }

        .pipeline-label {
            color: #929aa7;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .pipeline-value {
            color: #f5f7fa;
            font-size: 1.55rem;
            font-weight: 750;
            margin-top: 0.35rem;
        }

        /* Chart container */
        .chart-card {
            background: rgba(18, 23, 30, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 16px;
            padding: 1rem 1rem 0.5rem 1rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }

        /* Small info text */
        .muted {
            color: #858e9c;
            font-size: 0.82rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

first_name = st.session_state.user.get("first_name", "")
welcome_name = first_name if first_name else "there"

st.markdown(
    f"""
    <div class="dashboard-header">
        <div class="dashboard-title">Dashboard</div>
        <div class="dashboard-subtitle">
            Welcome back, {welcome_name}. Here's what's happening with your business.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FETCH SUMMARY
# ============================================================

try:
    summary = api_client.get_dashboard_summary()
except Exception as e:
    st.error(f"Dashboard data load nahi ho saka. ({e})")
    st.stop()


# ============================================================
# KPI CARDS
# ============================================================

kpis = [
    (
        "Total Leads",
        summary.get("total_leads", 0),
        "👥",
    ),
    (
        "Active Employees",
        summary.get("active_employees", 0),
        "👤",
    ),
    (
        "Inactive Employees",
        summary.get("inactive_employees", 0),
        "⏸️",
    ),
    (
        "Knowledge Sources",
        summary.get("total_knowledge_sources", 0),
        "📚",
    ),
    (
        "Representatives",
        summary.get("total_representatives", 0),
        "🤝",
    ),
]

columns = st.columns(5)

for column, (label, value, icon) in zip(columns, kpis):
    with column:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# LEAD PIPELINE
# ============================================================

st.markdown(
    '<div class="section-title">Lead Pipeline</div>',
    unsafe_allow_html=True,
)

pipeline = [
    (
        "New",
        summary.get("new_leads", 0),
        "🆕",
    ),
    (
        "Contacted",
        summary.get("contacted_leads", 0),
        "📞",
    ),
    (
        "Qualified",
        summary.get("qualified_leads", 0),
        "✅",
    ),
    (
        "Lost",
        summary.get("lost_leads", 0),
        "❌",
    ),
]

pipeline_columns = st.columns(4)

for column, (label, value, icon) in zip(pipeline_columns, pipeline):
    with column:
        st.markdown(
            f"""
            <div class="pipeline-card">
                <div class="pipeline-label">{icon} {label}</div>
                <div class="pipeline-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# LEADS OVER TIME
# ============================================================

chart_left, chart_right = st.columns([2.2, 1])

with chart_left:

    st.markdown(
        '<div class="section-title">Leads Over Time</div>',
        unsafe_allow_html=True,
    )

    try:
        lot = api_client.get_leads_over_time(days=30)

        df = pd.DataFrame(lot.get("points", []))

        if df.empty:
            st.info("No lead activity available for the last 30 days.")

        else:
            df["date"] = pd.to_datetime(df["date"])
            df["count"] = pd.to_numeric(
                df["count"],
                errors="coerce",
            ).fillna(0)

            fig = go.Figure()

            # Area
            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["count"],
                    mode="lines",
                    line=dict(
                        color="#FF4B3E",
                        width=3,
                        shape="spline",
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(255, 75, 62, 0.10)",
                    hovertemplate=(
                        "<b>%{x|%b %d, %Y}</b>"
                        "<br>Leads: %{y}"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                height=360,
                margin=dict(
                    l=15,
                    r=15,
                    t=20,
                    b=15,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#9AA3B2",
                ),
                xaxis=dict(
                    title=None,
                    showgrid=False,
                    zeroline=False,
                    tickformat="%b %d",
                ),
                yaxis=dict(
                    title=None,
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.06)",
                    zeroline=False,
                    rangemode="tozero",
                ),
                hoverlabel=dict(
                    bgcolor="#171C24",
                    bordercolor="#343B47",
                    font=dict(
                        color="#FFFFFF",
                    ),
                ),
                showlegend=False,
            )

            st.markdown(
                '<div class="chart-card">',
                unsafe_allow_html=True,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Chart load nahi ho saka. ({e})")


# ============================================================
# LEAD DISTRIBUTION
# ============================================================

with chart_right:

    st.markdown(
        '<div class="section-title">Lead Distribution</div>',
        unsafe_allow_html=True,
    )

    lead_labels = [
        "New",
        "Contacted",
        "Qualified",
        "Lost",
    ]

    lead_values = [
        summary.get("new_leads", 0),
        summary.get("contacted_leads", 0),
        summary.get("qualified_leads", 0),
        summary.get("lost_leads", 0),
    ]

    total_pipeline = sum(lead_values)

    if total_pipeline == 0:

        st.markdown(
            """
            <div class="chart-card">
                <div class="muted" style="padding: 6rem 1rem; text-align:center;">
                    No lead data available yet.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        donut = go.Figure(
            data=[
                go.Pie(
                    labels=lead_labels,
                    values=lead_values,
                    hole=0.68,
                    textinfo="none",
                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>Leads: %{value}"
                        "<br>%{percent}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        donut.update_layout(
            height=360,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.05,
                xanchor="center",
                x=0.5,
                font=dict(
                    color="#9AA3B2",
                    size=11,
                ),
            ),
            annotations=[
                dict(
                    text=f"<b>{total_pipeline}</b><br><span style='font-size:11px'>Total Leads</span>",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        color="#F5F7FA",
                        size=18,
                    ),
                )
            ],
        )

        st.markdown(
            '<div class="chart-card">',
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            donut,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# REPRESENTATIVE SUMMARY
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

active_reps = summary.get("active_representatives", 0)
total_reps = summary.get("total_representatives", 0)

st.markdown(
    f"""
    <div class="muted">
        🤝 {active_reps} active representative(s) out of {total_reps}
    </div>
    """,
    unsafe_allow_html=True,
)