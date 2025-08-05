import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from src.graphs.workflow import WorkflowGraph


def main():
    st.title("Weather & Document Assistant")
    
    # Initialize workflow
    workflow = WorkflowGraph()
    
    # Create chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from workflow
        with st.chat_message("assistant"):
            response = workflow.run(prompt)
            st.markdown(response["response"])
            st.session_state.messages.append({"role": "assistant", "content": response["response"]})

if __name__ == "__main__":
    main()
