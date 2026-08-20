"""
Módulo de recuperación de fragmentos relevantes mediante búsqueda semántica
"""

from rag.embeddings import Embedder
from rag.vectorstore import VectorStore


class Retriever:
    """
    Recupera fragmentos relevantes utilizando similitud vectorial.
    """

    def __init__(
        self,
        top_k: int = 5,
        tolerance: float = 0.1,
    ) -> None:
        """
        Inicializa el recuperador.

        Args:
            top_k (int): Número máximo de fragmentos candidatos.
            tolerance (float): Margen adicional de distancia permitido
                               respecto al fragmento más similar.
        """

        self.embedder = Embedder()
        self.vectorstore = VectorStore()

        self.top_k = top_k
        self.tolerance = tolerance

    def search(
        self,
        query: str,
    ) -> list[dict]:
        """
        Busca fragmentos relevantes para una consulta.

        Primero genera el embedding de la consulta y recupera los
        fragmentos más cercanos. Después filtra los resultados utilizando
        la distancia del fragmento más similar como referencia.

        Args:
            query (str): Consulta de búsqueda.

        Returns:
            list[dict]: Fragmentos relevantes con su distancia asociada.
        """

        query_embedding = self.embedder.embed(query)

        results = self.vectorstore.search(
            query_embedding,
            n_results=self.top_k,
        )

        if not results:
            return []

        best_distance = results[0]["distance"]

        return [
            result
            for result in results
            if result["distance"]
            <= best_distance + self.tolerance
        ]


# ---
# Test
# ---

def main() -> None:
    retriever = Retriever()

    results = retriever.search(
        "Definición: Acción de Conversión"
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    main()