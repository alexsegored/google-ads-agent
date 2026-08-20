"""
Módulo de generación de embeddings
"""

from sentence_transformers import SentenceTransformer


class Embedder:
    """Genera embeddings utilizando BAAI/bge-m3."""

    def __init__(self) -> None:
        """Inicializa el modelo de generación de embeddings."""

        self.model = SentenceTransformer("BAAI/bge-m3")

    def embed(self, text: str) -> list[float]:
        """
        Genera el embedding de un único texto.

        Args:
            text (str): Texto para el que se genera el embedding.

        Returns:
            list[float]: Vector de embeddings normalizado.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Genera embeddings para varios textos.

        Args:
            texts (list[str]): Lista de textos a procesar.

        Returns:
            list[list[float]]: Lista de vectores de embeddings normalizados.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()