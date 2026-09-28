# RAG Pinecone Localization

Un módulo de retrieval chico pero escalable, hecho con Pinecone Serverless, sobre un tema bien específico: **localización y localization engineering**. La idea era no usar un dataset genérico, así que armé una base de conocimiento propia sobre el tema y construí un retriever híbrido que combina Pinecone (búsqueda semántica) con BM25 (búsqueda léxica).

Esto es un proyecto de retrieval, no un chatbot. No hay ningún paso de generación con LLM, el objetivo es devolver los chunks correctos para una consulta, no redactar una respuesta.

## De qué se trata

La base de conocimiento son 15 documentos Markdown cortos sobre localización: Translation Memories, SDLXLIFF, Trados Studio, match percentages, segmentación, placeholders/tags, XML, XPath, QA lingüística, límites de caracteres, terminología/glosarios, DTP, localización en CMS, Sitecore y formatos de archivo. El proyecto corre entero sin depender de que un sitio externo esté disponible.

## Arquitectura

```text
Documentos (data/documents/*.md)
   ↓
Chunking (RecursiveCharacterTextSplitter)
   ↓
Embeddings (OpenAI text-embedding-3-small)
   ↓
Pinecone Serverless (index)
   ↓
                ┌─ Retriever vectorial (Pinecone)
Query ──────────┤
                └─ Retriever BM25 (corpus local)
                       ↓
                EnsembleRetriever (pesos configurables)
                       ↓
                    Top 5 chunks
```

BM25 no puede consultar el index de Pinecone directamente — es un algoritmo léxico, y Pinecone es una base de vectores, no tienen nada que ver entre sí. Por eso el lado BM25 arma su propio corpus en memoria a partir de los mismos documentos de `data/documents/`, cortados exactamente igual que en la ingesta, usando los mismos `document_id` / `chunk_id`. Así, cuando `EnsembleRetriever` combina los dos resultados, un chunk que aparece en ambas listas es reconociblemente el mismo chunk en las dos.

## Requisitos

- Python 3.10+
- Cuenta de Pinecone con API key (el free tier alcanza, soporta indexes Serverless)
- API key de OpenAI (para los embeddings)
- Los paquetes de `requirements.txt`

## Configuración

Copiá `.env.example` a `.env` y completá tus keys:

```bash
cp .env.example .env
```

```text
PINECONE_API_KEY=tu-key-de-pinecone
OPENAI_API_KEY=tu-key-de-openai
INDEX_NAME=localization-rag
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
```

El `.env` está en `.gitignore` — nunca subas tus keys reales al repo. `PINECONE_CLOUD` / `PINECONE_REGION` tienen que coincidir con lo que soporte tu cuenta/plan de Pinecone (el free tier normalmente es `aws` / `us-east-1`). Si dejás esas dos variables vacías, el código las completa solo con esos mismos valores por defecto.

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# ahora completá el .env con tus keys
```

## Setup de Pinecone

`src/pinecone_setup.py` crea el index si todavía no existe, y no hace nada si ya está creado (así lo podés correr las veces que quieras sin miedo):

- **Nombre del index**: `INDEX_NAME` del `.env` (por defecto `localization-rag`)
- **Dimensión**: `1536`, que es la dimensión fija que devuelve `text-embedding-3-small`. Esta constante vive en un solo lugar (`src/config.py`) para que no se desincronice entre el index y los embeddings.
- **Métrica**: `cosine`
- **Tipo**: Serverless (`ServerlessSpec`), en el cloud/región que pongas en el `.env`
- **Namespace**: `localization` (también en `src/config.py`) — todos los vectores de este proyecto viven ahí, así el index podría tener otros proyectos en otros namespaces sin pisarse.

Para correrlo:

```bash
python -m src.pinecone_setup
```

## Ingesta

```bash
python -m src.ingest
```

Esto lee cada `.md` de `data/documents/`, divide cada uno con `RecursiveCharacterTextSplitter` (chunk de ~2200 caracteres, ~300 de overlap — más o menos 500-700 tokens para este tipo de texto técnico en inglés, sin depender de un tokenizer específico para calcularlo), genera el embedding de cada chunk con `text-embedding-3-small`, y sube todo a Pinecone.

Cada chunk tiene un **ID determinístico**: `f"{document_id}_{numero_de_chunk}"` (por ejemplo `sdlxliff.md_0`). Si corrés la ingesta de nuevo, se pisan los mismos vectores en vez de crear duplicados — así que es seguro volver a correrla después de editar un documento.

Metadata que se guarda por vector:

| campo | qué es |
|---|---|
| `document_id` | nombre del archivo, ej. `sdlxliff.md` — es el identificador estable que usa la evaluación |
| `source` | ruta al archivo original |
| `page` | siempre `""` (vacío) — son documentos Markdown, no PDFs con páginas, así que no existe un número de página real. Pinecone no acepta `null` en la metadata, por eso uso string vacío en vez de inventar una página |
| `category` | categoría temática de cada documento (`tm-and-matching`, `file-formats`, `cat-tools`, `terminology`, `engineering`, `qa`, `cms`) — ver `CATEGORY_MAP` en `src/ingest.py` |
| `chunk_id` | igual al ID del vector |
| `text` | el texto del chunk tal cual, para poder leerlo directo desde el resultado de la búsqueda |

## Retrieval híbrido

`src/retriever.py` arma dos retrievers y los combina con `EnsembleRetriever` de LangChain:

- un **retriever vectorial de Pinecone** (`PineconeVectorStore.as_retriever`) para similitud semántica
- un **retriever BM25** (`BM25Retriever`) armado con el mismo corpus de chunks, para matching léxico/de palabras exactas — esto es lo que da ventaja con términos técnicos y nombres propios como "SDLXLIFF" o "Sitecore", que una búsqueda puramente semántica a veces no prioriza tan bien como una paráfrasis

Los dos se combinan con pesos configurables (por defecto: vector `0.7`, BM25 `0.3`) en `src/config.py`. No son pesos "óptimos" ni nada por el estilo, son solo un punto de partida razonable — podés cambiar `VECTOR_WEIGHT` / `BM25_WEIGHT` y volver a correr para experimentar.

`src/rag_system.py` envuelve todo esto en una clase simple:

```python
from src.rag_system import RAGSystem

rag = RAGSystem()
results = rag.retrieve("How are SDLXLIFF tags handled?")
# results: lista de dicts con rank, document_id, chunk_id, source, category, text
```

## Evaluación

```bash
python evaluate.py
```

`data/golden_set.json` tiene 5 preguntas de localización, cada una con el `document_id` que se espera que aparezca. Algunas preguntas usan términos técnicos exactos (para que BM25 tenga ventaja), otras están parafraseadas sin nombrar el término directamente (para que la búsqueda semántica tenga que hacer el trabajo).

Las preguntas están en español porque es un escenario bastante real: alguien que labura en localización consultando documentación técnica en inglés en su propio idioma. Los nombres propios y términos técnicos (SDLXLIFF, Trados Studio, XPath, etc.) son iguales en los dos idiomas, así que BM25 los sigue matcheando igual; el modelo de embeddings (`text-embedding-3-small`) se encarga de la similitud semántica cross-lingual para el resto de la oración.

**Recall@5** (por pregunta): `1` si el documento esperado aparece en algún lugar entre los top 5 resultados, `0` si no aparece. El valor agregado es el promedio entre las 5 preguntas.

**Precision@5** (por pregunta): `(cantidad de documentos relevantes recuperados) / 5`. Como el Golden Set solo marca *un* documento como relevante por pregunta, si acierta da `1/5 = 0.20`, y si no acierta da `0/5 = 0.00`. Esto a propósito **no es lo mismo** que recall — un recall perfecto de `1.00` sigue topeando la precisión en `0.20` por pregunta, porque de los 5 resultados devueltos solo uno puede ser "el" relevante bajo esta definición. Es el comportamiento esperado de la métrica, no un bug.

## Resultados

No pude correr la evaluación en el entorno donde armé este repo — no había keys de Pinecone ni de OpenAI disponibles ahí, y el pipeline directamente se niega a correr sin ellas (`pinecone_setup.py` tira `RuntimeError: Falta PINECONE_API_KEY en el .env` si falta la key, y `ingest.py`/`retriever.py` hacen lo mismo con `OPENAI_API_KEY`). Lo que sí pude validar sin usar ninguna API externa:

- Todos los módulos importan y compilan bien contra las versiones de dependencias que quedaron fijadas en `requirements.txt`.
- Corrí directamente la carga y el chunking de documentos (`src/ingest.py`): los 15 documentos generan 16 chunks sin errores.
- Corrí el lado BM25 del retriever híbrido (`src/retriever.py`) de forma standalone contra una consulta real ("How are SDLXLIFF tags handled?") y devolvió `sdlxliff.md` como primer resultado, confirmando que esa mitad de la arquitectura funciona de punta a punta.

Para tener números reales de Recall@5 / Precision@5, corré en orden, después de completar el `.env`:

```bash
python -m src.pinecone_setup
python -m src.ingest
python evaluate.py
```

La salida por consola de `evaluate.py` es el reporte que hay que usar — pegalo acá (o guardalo en tu entrega) una vez que lo corras con tus propias keys.

## Cómo reproducir el index

Para pasar de un clone recién hecho a una evaluación funcionando:

1. Cloná el repo.
2. `pip install -r requirements.txt`
3. `cp .env.example .env` y completá `PINECONE_API_KEY`, `OPENAI_API_KEY`, `PINECONE_CLOUD`, `PINECONE_REGION` (y opcionalmente cambiá `INDEX_NAME`).
4. `python -m src.pinecone_setup` — crea el index Serverless (cosine, 1536 dimensiones) si todavía no existe.
5. `python -m src.ingest` — corta los documentos de `data/documents/`, los embebe, y los sube al namespace `localization` con IDs determinísticos.
6. No hace falta nada extra para "inicializar" BM25 — `src/retriever.py` reconstruye su corpus en memoria desde `data/documents/` cada vez que se crea un `RAGSystem()`, usando la misma función de chunking que la ingesta.
7. Si querés probar consultas sueltas: `python -m src.rag_system` (corre una query de ejemplo al final del archivo), o importá `RAGSystem` como en el ejemplo de arriba.
8. `python evaluate.py` — corre el Golden Set y muestra Recall@5 / Precision@5.

## Estructura del repo

```text
rag-pinecone-localization/
│
├── data/
│   ├── documents/          # 15 documentos Markdown propios sobre localización
│   └── golden_set.json     # 5 preguntas de benchmark con su document_id esperado
│
├── src/
│   ├── config.py           # una sola fuente de verdad para nombres, dims, pesos
│   ├── pinecone_setup.py   # crea el index Serverless (idempotente)
│   ├── ingest.py            # carga, corta en chunks, embebe y sube a Pinecone
│   ├── retriever.py         # arma el retriever vectorial + BM25 + Ensemble
│   └── rag_system.py        # RAGSystem: la interfaz pública retrieve()
│
├── evaluate.py              # evaluación contra el Golden Set, Recall@5 / Precision@5
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
