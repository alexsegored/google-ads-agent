"""
Herramienta RAG
"""

from rag.retrieval import Retriever
from tools.adapter import adapt_tool


class RAGTool:
    """Herramienta RAG para búsqueda semántica en documentación interna."""

    def __init__(self) -> None:
        self.retriever = Retriever()

        self.name = "search_documentation"

        self.description = (
            "Recupera información de la documentación interna mediante "
            "búsqueda semántica."
        )

        self.inputSchema = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Consulta del usuario que se utilizará para "
                        "buscar documentación interna relevante."
                    ),
                }
            },
            "required": ["query"],
        }

    async def get_definition(self) -> list[dict]:
        """
        Devuelve la definición de la herramienta.

        Returns:
            list[dict]: Definición en formato OpenAI/Groq.
        """

        return adapt_tool([self])

    async def execute(
        self,
        arguments: dict,
    ) -> dict:
        """
        Ejecuta una búsqueda sobre la documentación interna.

        Args:
            arguments (dict): Parámetros de entrada.

        Returns:
            dict: Resultado de la búsqueda.
        """

        query = arguments["query"]

        results = self.retriever.search(query)

        if not results:
            return {
                "isError": True,
                "error": (
                    "No se encontró información relevante "
                    "en la documentación."
                ),
            }

        context = "\n\n".join(
            f"Source: {result['metadata']['source']}\n"
            f"{result['text']}"
            for result in results
        )

        return {
            "isError": False,
            "context": context,
        }