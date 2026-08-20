"""
Módulo para gestión del almacenamiento vectorial - ChromaDB
"""

import chromadb


class VectorStore:
    """Gestiona la persistencia y búsqueda de documentos en ChromaDB."""

    def __init__(self) -> None:
        """
        Inicializa la colección de documentos en ChromaDB.

        La base de datos se almacena de forma persistente en disco y utiliza
        distancia coseno para calcular la similitud entre embeddings.
        """

        client = chromadb.PersistentClient(
            path="rag/db"
        )

        self.collection = client.get_or_create_collection(
            name="documents",
            metadata={
                "hnsw:space": "cosine",
            },
        )

    def add(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        """
        Almacena fragmentos de texto junto con sus embeddings y metadatos en ChromaDB. 

        Cada fragmento recibe un identificador único generado a partir
        de su posición dentro de la lista.

        Args:
            chunks (list[dict]): Fragmentos de texto a almacenar. Cada fragmento contiene: Texto + Metadatos
            embeddings (list[list[float]]): Embeddings asociados a cada fragmento.
        """

        # ids = [
        #     f"chunk_{i}"
        #     for i in range(len(chunks))
        # ]

        ids = [
            f"{chunk['metadata']['source']}_chunk_{i}"
            for i, chunk in enumerate(chunks)
        ]

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            chunk["metadata"]
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ) -> list[dict]:
        """
        Recupera los fragmentos más similares a un embedding de consulta.

        Args:
            query_embedding (list[float]): Embedding de la consulta.
            n_results (int): Número máximo de resultados a devolver.

        Returns:
            list[dict]: Lista de fragmentos con su texto y distancia
                        respecto a la consulta.
        """

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        documents = result["documents"][0]
        distances = result["distances"][0]
        metadatas = result["metadatas"][0]

        return [
            {
                "text": document,
                "distance": distance,
                "metadata": metadata,
            }
            for document, distance, metadata in zip(
                documents,
                distances,
                metadatas,
            )
        ]