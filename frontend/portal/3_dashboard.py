import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import api_client
from utils.sidebar import render_account_sidebar
from utils.theme import inject_custom_css, page_header
from utils.auth import require_login

inject_custom_css()

require_login()

render_account_sidebar()

page_header("📊", "Dashboard", f"Welcome back, {st.session_state.user.get('first_name', '')}")

# ---------------- summary fetch ----------------
try:
    summary = api_client.get_dashboard_summary()
except Exception as e:
    st.error(f"Dashboard data load nahi ho saka. ({e})")
    st.stop()

# ---------------- top metric cards ----------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Leads", summary.get("total_leads", 0))
c2.metric("Active Employees", summary.get("active_employees", 0))
c3.metric("Inactive Employees", summary.get("inactive_employees", 0))
c4.metric("Knowledge Sources", summary.get("total_knowledge_sources", 0))
c5.metric("Representatives", summary.get("total_representatives", 0))
st.caption(
    f"👥 {summary.get('active_representatives', 0)} active representative(s) "
    f"out of {summary.get('total_representatives', 0)}"
)

st.divider()

# ---------------- lead pipeline ----------------
st.subheader("Lead Pipeline")
p1, p2, p3, p4 = st.columns(4)
p1.metric("🆕 New", summary.get("new_leads", 0))
p2.metric("📞 Contacted", summary.get("contacted_leads", 0))
p3.metric("✅ Qualified", summary.get("qualified_leads", 0))
p4.metric("❌ Lost", summary.get("lost_leads", 0))

st.divider()

# ---------------- leads over time chart ----------------
st.subheader("Leads Over Time (Last 30 Days)")

try:
    lot = api_client.get_leads_over_time(days=30)
    df = pd.DataFrame(lot["points"])
    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["count"], marker="o", color="#6366F1")
    ax.set_xlabel("Date")
    ax.set_ylabel("Leads Captured")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()

    st.pyplot(fig)
except Exception as e:
    st.error(f"Chart load nahi ho saka. ({e})")