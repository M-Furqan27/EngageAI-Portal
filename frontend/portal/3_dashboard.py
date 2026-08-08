import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import api_client

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Pehle login karein.")
    st.stop()

with st.sidebar:
    st.divider()
    if st.button("🚪 Log out", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.onboarding_completed = False
        st.switch_page("app.py")

st.title("📊 Dashboard")
st.caption(f"Welcome, {st.session_state.user.get('first_name', '')}")

# ---------------- summary fetch ----------------
try:
    summary = api_client.get_dashboard_summary()
except Exception as e:
    st.error(f"Dashboard data load nahi ho saka. ({e})")
    st.stop()

# ---------------- top metric cards ----------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Leads", summary["total_leads"])
c2.metric("Active Employees", summary["active_employees"])
c3.metric("Inactive Employees", summary["inactive_employees"])
c4.metric("Knowledge Sources", summary["total_knowledge_sources"])

st.divider()

# ---------------- lead pipeline ----------------
st.subheader("Lead Pipeline")
p1, p2, p3, p4 = st.columns(4)
p1.metric("🆕 New", summary["new_leads"])
p2.metric("📞 Contacted", summary["contacted_leads"])
p3.metric("✅ Qualified", summary["qualified_leads"])
p4.metric("❌ Lost", summary["lost_leads"])

st.divider()

# ---------------- leads over time chart ----------------
st.subheader("Leads Over Time (Last 30 Days)")

try:
    lot = api_client.get_leads_over_time(days=30)
    df = pd.DataFrame(lot["points"])
    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["count"], marker="o", color="#FF4B4B")
    ax.set_xlabel("Date")
    ax.set_ylabel("Leads Captured")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()

    st.pyplot(fig)
except Exception as e:
    st.error(f"Chart load nahi ho saka. ({e})")
    
 