"""
Modelos de entrada y salida de la API
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Mensaje enviado por el cliente."""

    message: str


class ToolExecution(BaseModel):
    """Información de una herramienta ejecutada."""

    tool: str
    request: dict
    response: dict


class ChatResponse(BaseModel):
    """Respuesta devuelta por la API."""

    response: str
    tool_executions: list[ToolExecution]