from pathlib import Path

from langchain_chroma import Chroma

from embeddings import get_embedding_model
from chunker import chunk_documents
from document_loader import load_pdf_documents


BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_STORE_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "aerocopilot_documents"


def get_vector_store():
    """
    Open the existing ChromaDB vector store.

    This does NOT reload documents or regenerate embeddings.
    It simply connects to the existing persistent database.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
    )

    return vector_store


def build_vector_store():
    """
    Build the ChromaDB vector store from the aviation documents.

    Use this function only when intentionally creating or
    rebuilding the vector database.
    """

    print("Loading documents...")

    documents = load_pdf_documents()

    print(f"Loaded {len(documents)} pages.")

    print("\nCreating chunks...")

    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\nLoading embedding model...")

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

    print("\nCreating ChromaDB vector store...")

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

    print("\nVector store created successfully.")
    print(f"Location: {VECTOR_STORE_DIR}")

    return vector_store


if __name__ == "__main__":

    build_vector_store()