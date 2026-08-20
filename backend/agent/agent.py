"""
Agente
"""

import json
import os

from dotenv import load_dotenv
from groq import Groq

from mcp_ads.tool import MCPTool
from rag.tool import RAGTool

load_dotenv()

MODEL = "openai/gpt-oss-120b"


class Agent:
    """Coordina la interacción entre el modelo y las herramientas."""

    def __init__(self) -> None:
        """Inicializa el agente y las herramientas disponibles."""

        self.rag = RAGTool()
        self.mcp = MCPTool()

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.tools = None

    async def get_tools(self) -> list[dict]:
        """
        Obtiene la definición de todas las herramientas disponibles.

        Returns:
            list[dict]: Herramientas en formato OpenAI/Groq.
        """

        rag_tools = await self.rag.get_definition()
        mcp_tools = await self.mcp.get_definition()

        return [
            *rag_tools,
            *mcp_tools,
        ]

    async def execute_tool(
        self,
        tool: str,
        arguments: dict,
    ) -> dict:
        """
        Ejecuta la herramienta solicitada por el modelo.

        Args:
            tool (str): Nombre de la herramienta.
            arguments (dict): Parámetros de entrada.

        Returns:
            dict: Resultado de la ejecución.
        """

        if tool == self.rag.name:
            return await self.rag.execute(arguments)

        return await self.mcp.execute(
            tool,
            arguments,
        )

    async def invoke(
        self,
        messages: list[dict],
    ) -> dict:
        """
        Ejecuta el ciclo de conversación con el modelo.

        El modelo puede solicitar una o varias herramientas antes de
        generar la respuesta final.

        Args:
            messages (list[dict]): Historial de mensajes.

        Returns:
            dict: Respuesta final del agente y herramientas ejecutadas.
        """

        if self.tools is None:
            self.tools = await self.get_tools()

        tool_executions = []

        while True:

            response = self.client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                parallel_tool_calls=False,
            )

            assistant_message = response.choices[0].message

            messages.append(
                assistant_message.model_dump(
                    exclude_none=True,
                )
            )

            if not assistant_message.tool_calls:
                return {
                    "answer": assistant_message.content,
                    "tool_executions": tool_executions,
                }

            for tool_call in assistant_message.tool_calls:

                tool = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments or "{}"
                )

                result = await self.execute_tool(
                    tool,
                    arguments,
                )

                tool_executions.append(
                    {
                        "tool": tool,
                        "request": arguments,
                        "response": result,
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )