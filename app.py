"""Module owner: Krishna Murari, Purpose: Streamlit conversational user interface, Reviewed by: Swet Kumar"""
import streamlit as st
from src.response_generator import process_query
from src import config

st.set_page_config(
    page_title="Healthcare Helpdesk Decision Support System",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Healthcare Helpdesk Decision Support System")
st.markdown("Welcome! Type your health-related question, symptom, or hospital query below.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.header("📊 Pipeline Analytics")
    if st.session_state.messages:
        last_meta = st.session_state.get("last_meta", {})
        st.metric("Detected Intent", last_meta.get("intent", "N/A"))
        st.metric("Confidence Score", f"{last_meta.get('confidence', 0.0):.2%}")
        st.metric("Recommended Dept", last_meta.get("department", "N/A"))
        st.metric("Priority Level", last_meta.get("priority", "N/A"))
        if last_meta.get("escalated"):
            st.error("⚠️ Status: Escalated to Human Staff")
        else:
            st.success("✅ Status: Automated Resolution")
    else:
        st.info("Ask a question in chat to view live pipeline metrics here.")
    
    st.markdown("---")
    st.markdown("**B.Tech CSE Project (SDG 3)**")
    st.markdown("ERP: `0261dcs028` | Team: Krishna Murari & Peers")

if prompt := st.chat_input("Type your query here (e.g., 'chest pain hai', 'book appointment')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    result = process_query(prompt)
    st.session_state["last_meta"] = result

    if not result["valid"]:
        response_text = f"❌ **Error:** {result['error']}"
    else:
        response_text = result["full_text"]

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.rerun()
