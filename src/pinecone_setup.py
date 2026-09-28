"""Crea (si hace falta) el indice Serverless de Pinecone usado por el proyecto.

Se puede correr varias veces sin problema: si el indice ya existe, no se
vuelve a crear.
"""

from pinecone import Pinecone, ServerlessSpec

from src import config


def get_pinecone_client() -> Pinecone:
    if not config.PINECONE_API_KEY:
        raise RuntimeError("Falta PINECONE_API_KEY en el .env")
    return Pinecone(api_key=config.PINECONE_API_KEY)


def ensure_index_exists(pc: Pinecone) -> None:
    """Crea el indice si todavia no existe."""
    existing = [idx["name"] for idx in pc.list_indexes()]

    if config.INDEX_NAME in existing:
        print(f"El indice '{config.INDEX_NAME}' ya existe, no se recrea.")
        return

    print(f"Creando indice '{config.INDEX_NAME}' ({config.EMBEDDING_DIMENSION} dim, "
          f"metric={config.METRIC}, cloud={config.PINECONE_CLOUD}, region={config.PINECONE_REGION})...")

    pc.create_index(
        name=config.INDEX_NAME,
        dimension=config.EMBEDDING_DIMENSION,
        metric=config.METRIC,
        spec=ServerlessSpec(cloud=config.PINECONE_CLOUD, region=config.PINECONE_REGION),
    )
    print("Indice creado.")


def main() -> None:
    pc = get_pinecone_client()
    ensure_index_exists(pc)

    # Chequeo rapido de que el indice quedo accesible
    index = pc.Index(config.INDEX_NAME)
    stats = index.describe_index_stats()
    print("Stats del indice:", stats)


if __name__ == "__main__":
    main()
