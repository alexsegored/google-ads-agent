"""
Cliente para la API del backend
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


def send_message(message: str) -> dict:
    """
    Envía un mensaje al backend.

    Args:
        message (str): Mensaje del usuario.

    Returns:
        dict: Respuesta devuelta por la API.
    """

    response = requests.post(
        f"{API_URL}/chat",
        json={
            "message": message,
        },
    )

    response.raise_for_status()

    return response.json()


def reset_chat() -> None:
    """
    Reinicia la conversación en el backend.
    """

    response = requests.post(
        f"{API_URL}/reset",
    )

    response.raise_for_status()