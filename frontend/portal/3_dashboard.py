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


# ============================================================
# GLOBAL THEME / AUTH / SIDEBAR
# ============================================================

inject_custom_css()

require_login()

render_account_sidebar()


# ============================================================
# DASHBOARD HEADER
# ============================================================

user = st.session_state.get("user") or {}

first_name = user.get("first_name", "")

welcome_name = first_name if first_name else "there"


st.title("Dashboard")

st.caption(
    f"Welcome back, {welcome_name}. "
    "Here's what's happening with your business."
)


# ============================================================
# FETCH DASHBOARD SUMMARY
# ============================================================

try:

    summary = api_client.get_dashboard_summary()

except Exception as e:

    st.error(
        f"Dashboard data load nahi ho saka. ({e})"
    )

    st.stop()


# ============================================================
# KPI DATA
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


# ============================================================
# KPI CARDS
# ============================================================

st.markdown("### Business Overview")

kpi_columns = st.columns(5)

for column, (label, value, icon) in zip(
    kpi_columns,
    kpis,
):

    with column:

        with st.container(border=True):

            st.caption(
                f"{icon}  {label}"
            )

            st.metric(
                label="",
                value=value,
            )


# ============================================================
# LEAD PIPELINE
# ============================================================

st.markdown("### Lead Pipeline")

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


for column, (label, value, icon) in zip(
    pipeline_columns,
    pipeline,
):

    with column:

        with st.container(border=True):

            st.caption(
                f"{icon}  {label}"
            )

            st.metric(
                label="",
                value=value,
            )


# ============================================================
# CHART SECTION
# ============================================================

st.markdown("### Analytics")

chart_left, chart_right = st.columns(
    [2.15, 1],
    gap="large",
)


# ============================================================
# LEADS OVER TIME
# ============================================================

with chart_left:

    with st.container(border=True):

        st.subheader("Leads Over Time")

        st.caption(
            "Lead activity during the last 30 days."
        )

        try:

            lot = api_client.get_leads_over_time(
                days=30
            )

            points = lot.get(
                "points",
                [],
            )

            df = pd.DataFrame(points)

            if df.empty:

                st.info(
                    "No lead activity available "
                    "for the last 30 days."
                )

                st.caption(
                    "Once leads are captured, "
                    "their daily activity will appear here."
                )

            else:

                df["date"] = pd.to_datetime(
                    df["date"]
                )

                df["count"] = pd.to_numeric(
                    df["count"],
                    errors="coerce",
                ).fillna(0)

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=df["date"],
                        y=df["count"],
                        mode="lines+markers",
                        line=dict(
                            color="#FF4B3E",
                            width=3,
                            shape="spline",
                        ),
                        marker=dict(
                            size=6,
                            color="#FF4B3E",
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
                    height=350,

                    margin=dict(
                        l=10,
                        r=10,
                        t=15,
                        b=10,
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

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

        except Exception as e:

            st.error(
                f"Chart load nahi ho saka. ({e})"
            )


# ============================================================
# LEAD DISTRIBUTION
# ============================================================

with chart_right:

    with st.container(border=True):

        st.subheader("Lead Distribution")

        st.caption(
            "Current pipeline breakdown."
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

        total_pipeline = sum(
            lead_values
        )

        if total_pipeline == 0:

            st.info(
                "No lead data available yet."
            )

            st.caption(
                "Your lead distribution will "
                "appear here once leads are captured."
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

                height=350,

                margin=dict(
                    l=5,
                    r=5,
                    t=10,
                    b=5,
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                showlegend=True,

                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.08,
                    xanchor="center",
                    x=0.5,
                    font=dict(
                        color="#9AA3B2",
                        size=10,
                    ),
                ),

                annotations=[
                    dict(
                        text=(
                            f"<b>{total_pipeline}</b>"
                            "<br>"
                            "<span style='font-size:11px'>"
                            "Total Leads"
                            "</span>"
                        ),

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

            st.plotly_chart(
                donut,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )


# ============================================================
# REPRESENTATIVE SUMMARY
# ============================================================

st.markdown("### Team")

active_reps = summary.get(
    "active_representatives",
    0,
)

total_reps = summary.get(
    "total_representatives",
    0,
)


with st.container(border=True):

    team_col1, team_col2 = st.columns(
        [3, 1]
    )

    with team_col1:

        st.subheader(
            "Representative Activity"
        )

        st.caption(
            "Your current representative availability."
        )

    with team_col2:

        st.metric(
            "Active",
            f"{active_reps}/{total_reps}",
        )