"""
Aplicación Streamlit
"""

import streamlit as st

import json

from api import reset_chat
from api import send_message


st.set_page_config(
    page_title="Agente",
    layout="wide",
)


def render_tool(tool: dict) -> None:
    """
    Muestra la información de una herramienta ejecutada.

    Args:
        tool (dict): Información de la herramienta.
    """

    with st.expander(tool["tool"]):

        st.write("Request")
        st.json(tool["request"])

        st.write("Response")
        st.json(tool["response"])


def render_message(message: dict) -> None:
    """
    Muestra un mensaje del chat.

    Args:
        message (dict): Mensaje a mostrar.
    """

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        for tool in message.get("tool_executions", []):
            render_tool(tool)


# Barra lateral

with st.sidebar:

    st.divider()

    if st.button(
        "Nueva conversación",
        use_container_width=True,
    ):

        reset_chat()

        st.session_state.messages = []

        st.rerun()


# Historial

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    render_message(message)


# Entrada del usuario

if prompt := st.chat_input("Pregunta lo que quieras"):

    user_message = {
        "role": "user",
        "content": prompt,
    }

    st.session_state.messages.append(user_message)

    render_message(user_message)

    with st.spinner("Pensando..."):
        response = send_message(prompt)

    assistant_message = {
        "role": "assistant",
        "content": response["response"],
        "tool_executions": response["tool_executions"],
    }

    render_message(assistant_message)

    st.session_state.messages.append(
        assistant_message
    )