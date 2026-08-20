"""
Módulo de adaptación para las herramientas del agente.
"""


def adapt_tool(tools) -> list[dict]:
    """
    Convierte las herramientas al formato esperado
    por el modelo (OpenAI/Groq).

    Args: 
        tools: Herramientas a adaptar.

    Returns:
        list[dict]: Herramientas en formato OpenAI/Groq.
    """

    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools
    ]