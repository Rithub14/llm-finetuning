import streamlit as st
import requests

st.set_page_config(page_title="Customer Support LLM", page_icon="🤖", layout="wide")

st.title("🤖 Customer Support Assistant")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

def ask_backend(message: str):
    url = "http://127.0.0.1:8000/generate/"
    payload = {"query": message}
    response = requests.post(url, json=payload)
    return response.json()["response"]

# Chat UI
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)

user_input = st.chat_input("Ask your question…")

if user_input:
    st.session_state.history.append(("user", user_input))

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        answer = ask_backend(user_input)
        st.write(answer)

    st.session_state.history.append(("assistant", answer))
