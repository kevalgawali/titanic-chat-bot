import streamlit as st
import requests
import base64
import os

from dotenv import load_dotenv
load_dotenv()

# on streamlit cloud, pull HF token from secrets
try:
    if "HUGGINGFACEHUB_API_TOKEN" in st.secrets:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
except Exception:
    pass

st.set_page_config(page_title="Titanic Chat", page_icon="🚢")
st.title("🚢 Titanic Dataset Chat Agent")
st.caption("Ask anything about the Titanic passengers — text answers and charts")

API_URL = os.getenv("API_URL", "http://localhost:8000")


def check_backend():
    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


# check once per session whether backend is up
if "backend_up" not in st.session_state:
    st.session_state.backend_up = check_backend()

# if no backend, import agent directly
if not st.session_state.backend_up:
    from agent import ask as local_ask


def get_response(question):
    if st.session_state.backend_up:
        resp = requests.post(
            f"{API_URL}/chat",
            json={"question": question},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    else:
        return local_ask(question)


# sidebar
with st.sidebar:
    mode = "API" if st.session_state.backend_up else "Local"
    st.info(f"Mode: **{mode}**")
    st.markdown("### Try asking:")
    st.markdown("- How many passengers survived?")
    st.markdown("- Show survival rate by gender as a bar chart")
    st.markdown("- What was the average fare for 1st class?")
    st.markdown("- Plot age distribution")
    st.markdown("- Survival rate by passenger class — bar chart")

# init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# render past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("plot"):
            st.image(base64.b64decode(msg["plot"]))

# handle input
if prompt := st.chat_input("Ask about Titanic data..."):
    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                result = get_response(prompt)
                answer = result.get("answer", "No answer returned.")
                st.markdown(answer)

                entry = {"role": "assistant", "content": answer}

                if result.get("plot"):
                    st.image(base64.b64decode(result["plot"]))
                    entry["plot"] = result["plot"]

                st.session_state.messages.append(entry)
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the backend. Make sure the FastAPI server is running.")
            except Exception as e:
                import traceback
                st.error(f"Error ({type(e).__name__}): {e}")
                st.code(traceback.format_exc(), language="text")
