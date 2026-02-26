import streamlit as st
from agent import run_agent

st.title("📊 Monday.com BI Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask a business question:")

if query:
    result = run_agent(query, st.session_state.chat_history)

    st.session_state.chat_history.append({"role": "user", "content": query})
    st.session_state.chat_history.append({"role": "assistant", "content": result["summary"]})

    st.markdown("### 💡 Insight")
    st.write(result["summary"])

    st.markdown("### 🔍 Agent Trace")
    st.text(result["trace"])