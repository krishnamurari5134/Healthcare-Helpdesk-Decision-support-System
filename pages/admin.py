"""Module owner: Swet Kumar, Purpose: Streamlit admin staff panel for logs and escalations, Reviewed by: Krishna Murari"""
import streamlit as st
import pandas as pd
from src.database import get_all_logs, count_by_intent
from src.escalation import list_pending, mark_resolved, list_all

st.set_page_config(page_title="Helpdesk Admin Panel", page_icon="🛡️", layout="wide")

st.title("🛡️ Healthcare Helpdesk - Staff Admin Panel")
st.markdown("Monitor incoming patient queries, track escalations, and manage helpdesk operations.")

tab1, tab2, tab3 = st.tabs(["📋 Query Logs", "🚨 Escalated Queries", "⚙️ System Control (Review 3)"])

with tab1:
    st.subheader("All Handled Query Logs")
    logs = get_all_logs()
    if logs:
        df_logs = pd.DataFrame(logs)
        st.dataframe(df_logs, use_container_width=True)
        
        counts = count_by_intent()
        st.bar_chart(pd.Series(counts))
    else:
        st.info("No query logs recorded yet.")

with tab2:
    st.subheader("Pending Human Escalations")
    pending = list_pending()
    if pending:
        for item in pending:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**ID:** {item['id']} | **Time:** {item['timestamp']}")
                st.write(f"**Query:** {item['query']}")
                st.write(f"**Reason:** `{item['reason']}` | **Priority:** `{item['priority']}`")
            with col2:
                if st.button("Mark Resolved", key=f"resolve_{item['id']}"):
                    mark_resolved(item['id'])
                    st.success(f"Resolved escalation {item['id']}")
                    st.rerun()
            st.markdown("---")
    else:
        st.success("No pending escalations! All clear.")

with tab3:
    st.subheader("Knowledge Base & Model Management (Review 3 Stubs)")
    st.info("These advanced administrative controls are scheduled for implementation in Review 3.")
    
    kb_query = st.text_input("Add/Edit KB Question (TODO Review 3)")
    kb_answer = st.text_area("Add/Edit KB Answer (TODO Review 3)")
    if st.button("Save KB Entry [TODO]", disabled=True):
        pass
    
    if st.button("Retrain Intent Model [TODO]", disabled=True):
        pass
