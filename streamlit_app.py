import os
import base64
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agent import ask

st.set_page_config(page_title="Titanic Chat", page_icon="🚢")

# sidebar with suggestions
with st.sidebar:
    st.title("💬 Titanic Chat")
    st.markdown("Ask anything about the Titanic dataset.")
    st.markdown("### Try asking:")
    st.markdown("- How many passengers survived?")
    st.markdown("- Show survival rate by gender as a bar chart")
    st.markdown("- What was the average fare for 1st class?")
    st.markdown("- Plot age distribution")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


def render_message(msg):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("plot"):
            st.image(base64.b64decode(msg["plot"]))

# display past messages
for m in st.session_state.messages:
    render_message(m)

# user input
if prompt := st.chat_input("Ask about Titanic data…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = ask(prompt)
                answer = result.get("answer", "")
                st.markdown(answer)

                entry = {"role": "assistant", "content": answer}
                if result.get("plot"):
                    st.image(base64.b64decode(result["plot"]))
                    entry["plot"] = result["plot"]

                st.session_state.messages.append(entry)
            except Exception as e:
                st.error(f"Error: {e}")
