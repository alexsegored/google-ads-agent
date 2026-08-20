"""
Módulo de ingesta de documentos
"""

from pathlib import Path

from rag.chunks import Chunker
from rag.embeddings import Embedder
from rag.vectorstore import VectorStore


DOCUMENT_PATH = Path("rag/documents/conversionaction.md")


def read_document(path: Path) -> str:
    """
    Lee un documento Markdown desde disco.

    Args:
        path (Path): Ruta del documento.

    Returns:
        str: Contenido del documento.
    """

    return path.read_text(
        encoding="utf-8"
    )


def main() -> None:
    """
    Ejecuta el proceso completo de ingesta:

    1. Lee el documento fuente.
    2. Divide el contenido en fragmentos.
    3. Genera embeddings para cada fragmento.
    4. Almacena los fragmentos y embeddings en ChromaDB.
    """

    # Lectura del documento
    markdown = read_document(DOCUMENT_PATH)

    # Documento de origen
    source = DOCUMENT_PATH.name

    # Fragmentación del documento
    chunker = Chunker()
    chunks = chunker.split(
        markdown,
        source,
        )

    # Generación de embeddings
    embedder = Embedder()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedder.embed_many(texts)

    # Almacenamiento vectorial
    store = VectorStore()
    store.add(
        chunks,
        embeddings,
    )

    print(
        f"Documentos en la colección: "
        f"{store.collection.count()}"
    )

    print(
        f"Se han indexado {len(chunks)} chunks."
    )


if __name__ == "__main__":
    main()