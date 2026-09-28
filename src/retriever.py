"""Retriever hibrido: combina busqueda semantica en Pinecone con BM25 local.

BM25 no puede consultar el indice de Pinecone (es un vector store, no un
motor lexico), asi que armamos el corpus de BM25 en memoria a partir de los
mismos documentos/chunks que se subieron a Pinecone. Ambos retrievers
comparten los mismos document_id/chunk_id, para que los resultados se
puedan comparar y combinar de forma coherente.
"""

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from src import config
from src.ingest import chunk_documents, load_documents
from src.pinecone_setup import get_pinecone_client


def build_bm25_corpus() -> list[Document]:
    """Reconstruye localmente el mismo corpus de chunks que se subio a Pinecone."""
    docs = load_documents()
    chunks = chunk_documents(docs)
    return [Document(page_content=c["text"], metadata=c["metadata"]) for c in chunks]


def build_vector_retriever(top_k: int = config.TOP_K):
    """Retriever semantico contra Pinecone."""
    config.require_openai_key()
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL, api_key=config.OPENAI_API_KEY)
    pc = get_pinecone_client()
    index = pc.Index(config.INDEX_NAME)

    vector_store = PineconeVectorStore(index=index, embedding=embeddings, namespace=config.NAMESPACE)
    return vector_store.as_retriever(search_kwargs={"k": top_k})


def build_bm25_retriever(top_k: int = config.TOP_K) -> BM25Retriever:
    """Retriever lexico BM25 sobre el corpus local de chunks."""
    corpus = build_bm25_corpus()
    retriever = BM25Retriever.from_documents(corpus)
    retriever.k = top_k
    return retriever


def build_hybrid_retriever(
    top_k: int = config.TOP_K,
    vector_weight: float = config.VECTOR_WEIGHT,
    bm25_weight: float = config.BM25_WEIGHT,
) -> EnsembleRetriever:
    """Combina el retriever de Pinecone y el de BM25 con pesos configurables.

    Los pesos no son valores "optimos", son solo un punto de partida
    razonable (por defecto 0.7 vector / 0.3 BM25).
    """
    vector_retriever = build_vector_retriever(top_k)
    bm25_retriever = build_bm25_retriever(top_k)

    return EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[vector_weight, bm25_weight],
    )
