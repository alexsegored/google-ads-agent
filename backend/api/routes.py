"""
Rutas de la API
"""

from fastapi import APIRouter
from fastapi import Request

from api.models import ChatRequest
from api.models import ChatResponse
from chat.conversation import Conversation

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: Request,
    body: ChatRequest,
) -> ChatResponse:
    """
    Envía una consulta al agente.

    Args:
        request (Request): Solicitud HTTP.
        body (ChatRequest): Mensaje enviado por el cliente.

    Returns:
        ChatResponse: Respuesta generada por el agente.
    """

    response = await request.app.state.conversation.ask(
        body.message,
    )

    return ChatResponse(
        response=response["answer"],
        tool_executions=response["tool_executions"],
    )


@router.post("/reset")
async def reset(
    request: Request,
) -> dict:
    """
    Reinicia la conversación actual.

    Args:
        request (Request): Solicitud HTTP.

    Returns:
        dict: Confirmación del reinicio.
    """

    request.app.state.conversation = Conversation(
        request.app.state.agent,
    )

    return {
        "message": "Conversación reiniciada",
    }