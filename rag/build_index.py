import os
import pickle

import faiss

from sentence_transformers import SentenceTransformer


DOCUMENT_FOLDER = "rag/documents"

INDEX_FILE = "rag/faiss.index"

METADATA_FILE = "rag/metadata.pkl"

MODEL_NAME = "BAAI/bge-small-en-v1.5"


def read_documents():

    documents = []

    for filename in os.listdir(DOCUMENT_FOLDER):

        if not filename.endswith(".txt"):
            continue

        path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        documents.append({
            "filename": filename,
            "text": text
        })

    return documents


def create_chunks(text, chunk_size=800, overlap=150):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def build_index():

    documents = read_documents()

    chunks = []

    metadata = []

    for document in documents:

        document_chunks = create_chunks(
            document["text"]
        )

        for chunk in document_chunks:

            chunks.append(chunk)

            metadata.append({
                "filename": document["filename"],
                "text": chunk
            })

    model = SentenceTransformer(
        MODEL_NAME
    )

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    faiss.write_index(
        index,
        INDEX_FILE
    )

    with open(
        METADATA_FILE,
        "wb"
    ) as file:

        pickle.dump(
            metadata,
            file
        )

    print(
        f"Created RAG index with {len(chunks)} chunks."
    )


if __name__ == "__main__":

    build_index()