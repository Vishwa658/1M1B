import pickle

import faiss

from sentence_transformers import SentenceTransformer

from config import (
    RAG_INDEX_PATH,
    RAG_METADATA_PATH,
    EMBEDDING_MODEL,
    TOP_K_DOCUMENTS
)


model = SentenceTransformer(
    EMBEDDING_MODEL
)


index = faiss.read_index(
    RAG_INDEX_PATH
)


with open(
    RAG_METADATA_PATH,
    "rb"
) as file:

    metadata = pickle.load(file)


def retrieve_documents(question):

    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    scores, indexes = index.search(
        query_embedding,
        TOP_K_DOCUMENTS
    )

    results = []

    for score, index_number in zip(
        scores[0],
        indexes[0]
    ):

        if index_number == -1:
            continue

        item = metadata[index_number]

        results.append({

            "score": float(score),

            "filename": item["filename"],

            "text": item["text"]

        })

    return results


def build_context(question):

    documents = retrieve_documents(
        question
    )

    context_parts = []

    for document in documents:

        context_parts.append(
            f"""
SOURCE: {document['filename']}

{document['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    return context, documents