"""Pipeline de ingesta: lee los documentos de localizacion, los divide en
chunks, genera embeddings y los sube a Pinecone.

Se puede correr mas de una vez: los IDs de los vectores son deterministicos
(document_id + numero de chunk), asi que volver a correrlo simplemente
sobreescribe los mismos vectores en vez de duplicarlos.
"""

import glob
import os

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import config
from src.pinecone_setup import ensure_index_exists, get_pinecone_client

# Categoria tematica por documento, para que la metadata sirva para algo
# (ej: filtrar por categoria en Pinecone). Si aparece un doc nuevo que no
# esta en el mapa, cae al default generico en vez de romper.
CATEGORY_MAP = {
    "translation-memory.md": "tm-and-matching",
    "match-percentages.md": "tm-and-matching",
    "segments-and-segmentation.md": "tm-and-matching",
    "terminology-glossaries.md": "terminology",
    "sdlxliff.md": "file-formats",
    "xml-localization.md": "file-formats",
    "localization-file-formats.md": "file-formats",
    "trados-studio.md": "cat-tools",
    "xpath-basics.md": "engineering",
    "dtp-localization-engineering.md": "engineering",
    "placeholders-and-tags.md": "qa",
    "linguistic-qa.md": "qa",
    "character-limits.md": "qa",
    "cms-localization.md": "cms",
    "sitecore-localization.md": "cms",
}
DEFAULT_CATEGORY = "localization-engineering"


def load_documents() -> list[dict]:
    """Lee todos los .md de data/documents y arma un dict por documento."""
    docs = []
    paths = sorted(glob.glob(os.path.join(config.DOCUMENTS_DIR, "*.md")))

    for path in paths:
        document_id = os.path.basename(path)  # ej: "sdlxliff.md"
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"document_id": document_id, "source": path, "text": text})

    return docs


def chunk_documents(docs: list[dict]) -> list[dict]:
    """Divide cada documento en chunks con overlap, guardando metadata util."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )

    chunks = []
    for doc in docs:
        pieces = splitter.split_text(doc["text"])
        for i, piece in enumerate(pieces):
            chunk_id = f"{doc['document_id']}_{i}"
            chunks.append({
                "id": chunk_id,
                "text": piece,
                "metadata": {
                    "document_id": doc["document_id"],
                    "source": doc["source"],
                    # son Markdown, no hay numero de pagina real; Pinecone no
                    # acepta null en metadata, asi que usamos "" en vez de None
                    "page": "",
                    "category": CATEGORY_MAP.get(doc["document_id"], DEFAULT_CATEGORY),
                    "chunk_id": chunk_id,
                    "text": piece,
                },
            })

    return chunks


def upload_chunks(chunks: list[dict]) -> None:
    """Genera embeddings y sube los chunks a Pinecone con IDs deterministicos."""
    config.require_openai_key()
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL, api_key=config.OPENAI_API_KEY)

    pc = get_pinecone_client()
    ensure_index_exists(pc)
    index = pc.Index(config.INDEX_NAME)

    vector_store = PineconeVectorStore(index=index, embedding=embeddings, namespace=config.NAMESPACE)

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["id"] for c in chunks]

    # add_texts con el mismo id pisa el vector anterior, no crea uno nuevo
    vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    print(f"Subidos {len(chunks)} chunks al namespace '{config.NAMESPACE}'.")


def main() -> None:
    docs = load_documents()
    print(f"Encontrados {len(docs)} documentos en {config.DOCUMENTS_DIR}")

    chunks = chunk_documents(docs)
    print(f"Generados {len(chunks)} chunks (chunk_size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})")

    upload_chunks(chunks)


if __name__ == "__main__":
    main()
