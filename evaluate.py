"""Evalua el retriever hibrido contra el Golden Set y calcula Recall@5 y Precision@5.

Definicion usada aca (ver README para mas detalle):
- Recall@5 por pregunta: 1 si el documento esperado aparece entre los top 5
  resultados, 0 si no. El agregado es el promedio sobre todas las preguntas.
- Precision@5 por pregunta: como el Golden Set solo marca UN documento como
  relevante por pregunta, precision = (1 si aparece, 0 si no) / 5.
  Es decir, no es lo mismo que recall: incluso acertando, precision@5 nunca
  pasa de 0.20 porque de los 5 resultados solo uno puede ser "el correcto".
"""

import json

from src.config import GOLDEN_SET_PATH
from src.rag_system import RAGSystem


def load_golden_set() -> list[dict]:
    with open(GOLDEN_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate() -> None:
    golden_set = load_golden_set()
    rag = RAGSystem()

    print("=" * 40)
    print("Evaluacion del RAG")
    print("=" * 40)

    recalls = []
    precisions = []

    for i, item in enumerate(golden_set, start=1):
        question = item["pregunta"]
        expected_doc = item["documento_id_esperado"]

        results = rag.retrieve(question)
        retrieved_docs = [r["document_id"] for r in results]

        hit = 1 if expected_doc in retrieved_docs else 0
        recall_at_5 = hit
        precision_at_5 = hit / 5

        recalls.append(recall_at_5)
        precisions.append(precision_at_5)

        print(f"\nPregunta {i}")
        print(f"Consulta: {question}")
        print(f"Esperado: {expected_doc}")
        print("Recuperados:")
        for r in results:
            print(f"{r['rank']}. {r['document_id']}")

        print(f"\nRecall@5: {recall_at_5}")
        print(f"Precision@5: {precision_at_5:.2f}")

    aggregate_recall = sum(recalls) / len(recalls)
    aggregate_precision = sum(precisions) / len(precisions)

    print("\n" + "=" * 40)
    print("Resultados agregados")
    print("=" * 40)
    print(f"Recall@5: {aggregate_recall:.2f}")
    print(f"Precision@5: {aggregate_precision:.2f}")
    print("=" * 40)


if __name__ == "__main__":
    evaluate()
