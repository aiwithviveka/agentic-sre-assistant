import streamlit as st
from sre_agent import agent_executor  # Import the executor from your script
import sys
from io import StringIO

# 1. UI Configuration
st.set_page_config(page_title="Agentic SRE Assistant", page_icon="🛡️")
st.title("🛡️ Agentic SRE Assistant")
st.subheader("Autonomous Infrastructure Monitoring & Remediation")

# 2. Chat History Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input
if prompt := st.chat_input("What is the system status?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Agent Execution with UI feedback
    with st.chat_message("assistant"):
        with st.status("🛠️ SRE Agent is thinking...", expanded=True) as status:
            # Capturing terminal output to show "thoughts" in the UI
            try:
                # We call the agent here
                response = agent_executor.invoke({"input": prompt})
                output = response["output"]
                status.update(label="✅ Diagnosis Complete!", state="complete", expanded=False)
            except Exception as e:
                output = f"❌ Error: {str(e)}"
                status.update(label="❌ System Failure", state="error")

        st.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})