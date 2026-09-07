from pathlib import Path

from langchain_chroma import Chroma

from src.embeddings import get_embedding_model
from src.chunker import chunk_documents
from src.document_loader import load_pdf_documents


BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_STORE_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "aerocopilot_documents"


def build_vector_store():
    """
    Build the ChromaDB vector store from the aviation documents.
    """

    print("Loading aviation documents...")

    documents = load_pdf_documents()

    print(f"Loaded {len(documents)} pages.")

    print("Creating document chunks...")

    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    ids = [
        f"{chunk['source']}_{chunk['page']}_{chunk['chunk_id']}"
        for chunk in chunks
    ]

    print("Creating ChromaDB vector store...")

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
    )

    print("Adding document chunks...")

    vector_store.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids,
    )

    print("Vector store created successfully.")

    return vector_store


def get_vector_store():
    """
    Get the ChromaDB vector store.

    If the vector store does not exist or contains no documents,
    automatically build it from the aviation documents.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
    )

    # Check whether the collection contains documents.
    try:
        count = vector_store._collection.count()
    except Exception:
        count = 0

    if count == 0:
        print("Vector store is empty.")
        print("Building vector store from aviation documents...")

        vector_store = build_vector_store()

    return vector_store


if __name__ == "__main__":
    build_vector_store()