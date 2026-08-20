"""
Módulo de gestión del contexto conversacional del agente
"""


from agent.agent import Agent
from chat.prompts import SYSTEM_PROMPT


class Conversation:
    """Gestiona el historial y contexto de una conversación."""

    def __init__(
        self,
        agent: Agent,
        max_turns: int = 3,
    ) -> None:
        """
        Inicializa una conversación.

        Args:
            agent (Agent): Agente encargado de procesar las consultas.
            max_turns (int): Número máximo de turnos almacenados.
        """

        self.agent = agent
        self.max_turns = max_turns

        self.history: list[dict] = []

    async def ask(
        self,
        question: str,
    ) -> dict:
        """
        Procesa una consulta del usuario mediante el agente.

        Args:
            question (str): Pregunta enviada por el usuario.

        Returns:
            dict: Respuesta del agente y metadatos asociados,
                  incluyendo ejecuciones de herramientas.
        """

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        messages.extend(self.history)

        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        response = await self.agent.invoke(messages)

        answer = response["answer"]

        # Guardar interacción final
        self.history.extend(
            [
                {
                    "role": "user",
                    "content": question,
                },
                {
                    "role": "assistant",
                    "content": answer,
                },
            ]
        )

        # Mantener únicamente los últimos N turnos
        self.history = self.history[-2 * self.max_turns:]

        # Devolver respuesta completa a la API
        return response