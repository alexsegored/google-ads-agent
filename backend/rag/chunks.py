"""
Módulo para la fragmentación de documentos Markdown
"""

class Chunker:
    """Divide un documento Markdown en fragmentos."""

    def split(
        self, 
        markdown: str,
        source: str
        ) -> list[dict]:
        """
        Divide un documento Markdown utilizando los encabezados.

        Cada fragmento corresponde al contenido comprendido entre dos
        encabezados `##` consecutivos.

        Args:
            markdown (str): Documento markdown a dividir.
            source (str): Nombre del documento de origen

        Returns:
            list[dict]: Lista de fragmentos obtenidos del documento. Cada fragmento contiene:
                - text: Contenido del fragmento.
                - metadata: Metadatos del fragmento.
        """

        chunks = []

        for i, chunk in enumerate(markdown.split("\n##")):
            chunk = chunk.strip()

            if chunk.endswith("---"):
                chunk = chunk[:-3].strip()

            if not chunk:
                continue
            
            # Recuperar '##'  
            if i > 0:
                chunk = f"## {chunk}"

            chunks.append({
                "text": chunk,
                "metadata": {
                    "source": source,
                },
            })

        return chunks