# Localization RAG with Pinecone

## Qué es

Un sistema de retrieval sobre un tema puntual: localización de software (Trados, SDLXLIFF, TMs, XPath, QA lingüística, etc.). No genera respuestas con un LLM, solo busca y devuelve los chunks de texto más relevantes para una pregunta. Combina búsqueda semántica (embeddings + Pinecone) con búsqueda por palabras clave (BM25).

Los documentos son 15 archivos Markdown que escribí yo mismo sobre distintos temas de localización, para no depender de ningún dataset externo.

## Cómo funciona

```text
Documentos
   ↓
Chunks
   ↓
Embeddings
   ↓
Pinecone

Pregunta
   ↓
Pinecone + BM25
   ↓
Top 5 resultados
```

Los documentos se cortan en chunks y cada chunk se convierte en un embedding con OpenAI, que se guarda en un index de Pinecone. Cuando llega una pregunta, se busca de dos formas al mismo tiempo: por significado (Pinecone) y por palabras exactas (BM25, corriendo sobre los mismos chunks en memoria). Los dos resultados se combinan con `EnsembleRetriever` de LangChain y devuelve los 5 mejores.

## Estructura

```text
data/
src/
evaluate.py
requirements.txt
.env.example
README.md
```

- `data/documents/`: los 15 documentos Markdown.
- `data/golden_set.json`: 5 preguntas de prueba con el documento que se espera como respuesta.
- `src/config.py`: nombres, dimensión del embedding, pesos, todo en un solo lugar.
- `src/pinecone_setup.py`: crea el index de Pinecone.
- `src/ingest.py`: corta los documentos en chunks y los sube a Pinecone.
- `src/retriever.py`: arma el retriever híbrido (Pinecone + BM25).
- `src/rag_system.py`: la clase `RAGSystem`, con el método `retrieve()`.
- `evaluate.py`: corre el Golden Set y calcula las métricas.

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
```

Después completá el `.env` con tus keys.

## Configuración

El `.env` necesita:

```text
PINECONE_API_KEY=tu key de pinecone
OPENAI_API_KEY=tu key de openai
INDEX_NAME=localization-rag
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
```

## Crear el índice

```bash
python -m src.pinecone_setup
```

Crea el index en Pinecone (Serverless, cosine, 1536 dimensiones) si todavía no existe. Si ya existe, no hace nada.

## Ingesta

```bash
python -m src.ingest
```

Lee los documentos, los corta en chunks, genera los embeddings y los sube a Pinecone. Cada chunk tiene un ID fijo, así que si lo corrés de nuevo no se duplica nada, solo se pisa.

## Evaluación

```bash
python evaluate.py
```

El script le hace las 5 preguntas del Golden Set al `RAGSystem` y para cada una calcula:

- **Recall@5**: 1 si el documento esperado aparece entre los 5 resultados, 0 si no.
- **Precision@5**: cuántos de los 5 resultados son el documento correcto, dividido 5. Como solo hay un documento correcto marcado por pregunta, acertar da como máximo 0.20.

Al final muestra el promedio de las 5 preguntas.

## Resultados

No llegué a correr la evaluación completa en el entorno donde armé el proyecto, porque no tenía las API keys ahí. Corré `python evaluate.py` con tus propias keys y pegá acá el resultado que te tira la consola.
