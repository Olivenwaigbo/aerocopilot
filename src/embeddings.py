from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """
    Load the embedding model once and reuse it.
    """

    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )


if __name__ == "__main__":

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    test_text = "Hydraulic system inspection"

    vector = embeddings.embed_query(test_text)

    print("\nEmbedding model loaded successfully.")
    print(f"Model: {MODEL_NAME}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")