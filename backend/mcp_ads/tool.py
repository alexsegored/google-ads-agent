"""
Herramientas MCP Google Ads
"""

from mcp_ads.client import MCPClient
from tools.adapter import adapt_tool


class MCPTool:
    """Gestiona las herramientas disponibles en el servidor MCP."""

    def __init__(self):
        """Inicializa cliente MCP."""

        self.client = MCPClient()

    async def get_definition(self) -> list[dict]:
        """
        Devuelve la definición de las herramientas disponibles.

        Returns:
            list[dict]: Definición de las herramientas en
                        formato OpenAI/Groq.
        """

        session = await self.client.connect()

        tools = await session.list_tools()

        return adapt_tool(tools.tools)

    async def execute(
        self,
        tool: str,
        arguments: dict,
    ) -> dict:
        """
        Ejecuta una herramienta del servidor MCP.

        Args:
            tool (str): Nombre de la herramienta.
            arguments (dict): Parámetros necesarios para ejecutar
                              la herramienta.

        Returns:
            dict: Resultado de la ejecución.
        """

        try:
            session = await self.client.connect()

            result = await session.call_tool(
                tool,
                arguments,
            )

        except Exception as exc:
            return {
                "isError": True,
                "error": f"Fallo de conexión: {exc}",
            }

        if result.isError:
            return {
                "isError": True,
                "error": result.content[0].text,
            }

        return {
            "isError": False,
            **result.structuredContent,
        }


# ---
# Test
# ---

import asyncio

async def main():

    mcp = MCPTool()

    try:

        # Listar herramientas
        tools = await mcp.get_definition()
        print(tools)

        print(f"Session: {id(mcp.client.session)}")

        # Pruebas:
        # Tool: "customers_list_accessible_customers"
        result = await mcp.execute(
            tool="customers_list_accessible_customers",
            arguments={},
        )
        print(result)
        print(f"Session: {id(mcp.client.session)}")

        # Tool: "search_search" - correcta
        result = await mcp.execute(
            tool="search_search",
            arguments={
                "customer_id": "1374577103",
                "resource": "conversion_action",
                "fields": [
                    "conversion_action.name",
                ],
            },
        )
        print(result)
        print(f"Session: {id(mcp.client.session)}")

        # Tool: "search" - inexistente
        result = await mcp.execute(
            tool="search",
            arguments={
                "customer_id": "1374577103",
                "resource": "conversion_action",
                "fields": [
                    "conversion_action.name",
                ],
            },
        )
        print(result)

        # Tool: "search_search" + conversion_action.error - campo inexistente
        result = await mcp.execute(
            tool="search_search",
            arguments={
                "customer_id": "1374577103",
                "resource": "conversion_action",
                "fields": [
                    "conversion_action.error",
                ],
            },
        )
        print(result)


    finally:
        await mcp.client.close()

if __name__ == "__main__":
    asyncio.run(main())

