"""
Cliente MCP Google Ads
"""

import os
import sys

from contextlib import AsyncExitStack

from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()


class MCPClient:
    """Gestiona la conexión con el servidor MCP"""

    def __init__(self):
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "ads_mcp.server"],
            env={
                **os.environ,
                "GOOGLE_ADS_DEVELOPER_TOKEN": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
                "GOOGLE_ADS_LOGIN_CUSTOMER_ID": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
                "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            }
        )

        self._stack: AsyncExitStack | None = None
        self.session: ClientSession | None = None

    async def connect(self) -> ClientSession:
        """
        Obtiene una sesión MCP activa.

        Si ya existe una sesión abierta, la reutiliza. De lo contrario,
        crea una nueva conexión e inicializa la sesión.

        Returns:
            ClientSession: Sesión MCP inicializada.
        """

        if self.session is not None:
            return self.session

        stack = AsyncExitStack()

        try:
            read, write = await stack.enter_async_context(
                stdio_client(self.server_params)
            )

            session = await stack.enter_async_context(
                ClientSession(read, write)
            )

            await session.initialize()

        except Exception:
            await stack.aclose()
            raise

        self._stack = stack
        self.session = session

        return session

    async def close(self) -> None:
        """Cierra la sesión MCP si existe."""

        if self._stack is None:
            return

        try:
            await self._stack.aclose()
        finally:
            self.session = None
            self._stack = None