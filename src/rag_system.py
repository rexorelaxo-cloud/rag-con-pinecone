"""Interfaz publica y simple del sistema de retrieval hibrido.

Uso:
    rag = RAGSystem()
    results = rag.retrieve("How are SDLXLIFF tags handled?")
"""

from src import config
from src.retriever import build_hybrid_retriever


class RAGSystem:
    def __init__(
        self,
        top_k: int = config.TOP_K,
        vector_weight: float = config.VECTOR_WEIGHT,
        bm25_weight: float = config.BM25_WEIGHT,
    ):
        self.top_k = top_k
        self.retriever = build_hybrid_retriever(
            top_k=top_k, vector_weight=vector_weight, bm25_weight=bm25_weight
        )

    def retrieve(self, query: str) -> list[dict]:
        """Devuelve el top_k de chunks recuperados con su metadata.

        EnsembleRetriever combina vector search y BM25 por rank fusion, no
        por un score unico comparable, asi que devolvemos la posicion
        (rank) en vez de inventar un score falso.
        """
        docs = self.retriever.invoke(query)[: self.top_k]

        results = []
        for rank, doc in enumerate(docs, start=1):
            results.append({
                "rank": rank,
                "document_id": doc.metadata.get("document_id"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "source": doc.metadata.get("source"),
                "category": doc.metadata.get("category"),
                "text": doc.page_content,
            })

        return results


if __name__ == "__main__":
    rag = RAGSystem()
    for r in rag.retrieve("How are SDLXLIFF tags handled?"):
        print(r["rank"], r["document_id"])
