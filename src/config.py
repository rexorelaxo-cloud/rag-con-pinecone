"""Configuracion centralizada del proyecto, leida desde variables de entorno."""

import os
from dotenv import load_dotenv

load_dotenv()

def _env(name: str, default: str) -> str:
    """Como os.getenv, pero trata '' (variable presente pero vacia) como no seteada."""
    value = os.getenv(name)
    return value if value else default


# Pinecone
PINECONE_API_KEY = _env("PINECONE_API_KEY", "")
INDEX_NAME = _env("INDEX_NAME", "localization-rag")
PINECONE_CLOUD = _env("PINECONE_CLOUD", "aws")
PINECONE_REGION = _env("PINECONE_REGION", "us-east-1")

# OpenAI
OPENAI_API_KEY = _env("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536  # dimension fija de text-embedding-3-small


def require_openai_key() -> None:
    """Falla temprano y con un mensaje claro si falta la key, en vez de un
    traceback feo mas adelante dentro de openai/langchain."""
    if not OPENAI_API_KEY:
        raise RuntimeError("Falta OPENAI_API_KEY en el .env")

# Namespace de Pinecone donde vive este proyecto
NAMESPACE = "localization"

# Metrica del indice (debe coincidir con la usada en pinecone_setup.py)
METRIC = "cosine"

# Chunking
# ~600 tokens de texto en ingles equivalen aprox. a 2400-3000 caracteres.
# Usamos un tamano en caracteres para no depender de un tokenizer especifico.
CHUNK_SIZE = 2200
CHUNK_OVERLAP = 300

# Rutas
DOCUMENTS_DIR = "data/documents"
GOLDEN_SET_PATH = "data/golden_set.json"

# Pesos del retriever hibrido (ver src/retriever.py)
VECTOR_WEIGHT = 0.7
BM25_WEIGHT = 0.3

# Cuantos resultados finales devuelve el retriever
TOP_K = 5
