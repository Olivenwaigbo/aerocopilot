from pathlib import Path
from functools import lru_cache

from langchain_chroma import Chroma

from src.embeddings import get_embedding_model


BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_STORE_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "aerocopilot_documents"


@lru_cache(maxsize=1)
def get_vector_store():
    """
    Open the existing persistent ChromaDB vector store once
    and reuse it for subsequent searches.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_STORE_DIR),
        embedding_function=embeddings,
    )

    return vector_store


def search_documents(query: str, k: int = 4):
    """
    Search the existing vector store for the most relevant
    document chunks.
    """

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    return results


if __name__ == "__main__":

    query = "What should be checked during a hydraulic system inspection?"

    results = search_documents(query, k=3)

    print("\nSearch results:\n")

    for document, score in results:

        print("=" * 70)

        print(
            f"Source: {document.metadata.get('source')}"
        )

        print(
            f"Page: {document.metadata.get('page')}"
        )

        print(
            f"Score: {score}"
        )

        print("\nContent:")

        print(
            document.page_content[:500]
        )