import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)


# Load Environment Variables

load_dotenv()


# Page Config

st.set_page_config(
    page_title="AI Personality Chat",
    page_icon="🤖",
    layout="wide"
)


# Custom CSS

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.title {
    text-align: center;
    color: white;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 20px;
}

.mode-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #1E1E1E;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# Title

st.markdown(
    "<div class='title'>🤖 AI Personality Chat</div>",
    unsafe_allow_html=True
)

# Model

model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)


# Sidebar

st.sidebar.title("🎭 Choose Personality")

mode_choice = st.sidebar.radio(
    "Select AI Mode",
    [
        "😡 Angry",
        "😂 Funny",
        "😢 Sad"
    ]
)

if mode_choice == "😡 Angry":
    mode = (
        "You are an angry AI agent. "
        "You respond aggressively and impatiently."
    )

elif mode_choice == "😂 Funny":
    mode = (
        "You are a very funny AI agent. "
        "You respond with humor and jokes."
    )

else:
    mode = (
        "You are a very sad AI agent. "
        "You respond in a depressed and emotional tone."
    )


# Session State

if "messages" not in st.session_state:

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

# Reset chat if mode changes
if st.session_state.current_mode != mode:

    st.session_state.current_mode = mode

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# Chat History

for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)


# User Input

prompt = st.chat_input(
    "Type your message..."
)

if prompt:

    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.spinner("Thinking..."):

        response = model.invoke(
            st.session_state.messages
        )

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    with st.chat_message("assistant"):
        st.write(response.content)