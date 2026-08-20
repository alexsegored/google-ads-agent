"""
Configuración FastAPI
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from agent.agent import Agent
from chat.conversation import Conversation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona la inicialización y liberación de recursos de la aplicación.

    Durante el arranque se crean las instancias compartidas del agente y
    la conversación, y se establece la conexión con el servidor MCP.
    Al finalizar la aplicación se cierran los recursos abiertos.
    """

    print("Iniciando API...")

    app.state.agent = Agent()

    app.state.conversation = Conversation(
        app.state.agent,
    )

    await app.state.agent.mcp.client.connect()

    print("API lista")

    yield

    print("Cerrando API...")

    await app.state.agent.mcp.client.close()

    print("Recursos liberados")


app = FastAPI(
    title="TFM",
    version="1.0.0",
    lifespan=lifespan,
)

from api.routes import router

app.include_router(router)


@app.get("/")
async def root() -> dict:
    """
    Comprueba que la API está disponible.

    Returns:
        dict: Estado de la aplicación.
    """

    return {
        "status": "ok",
        "message": "API funcionando correctamente",
    }