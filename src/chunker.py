from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.document_loader import load_pdf_documents


def chunk_documents(documents):
    """
    Split loaded aviation documents into smaller chunks
    for semantic retrieval.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
        ],
    )

    chunks = []

    for document in documents:
        text = document["text"]
        source = document["source"]
        page = document["page"]

        split_texts = text_splitter.split_text(text)

        for index, chunk_text in enumerate(split_texts):

            chunks.append(
                {
                    "text": chunk_text,
                    "source": source,
                    "page": page,
                    "chunk_id": index,
                }
            )

    return chunks


if __name__ == "__main__":

    print("Loading aviation documents...")

    documents = load_pdf_documents()

    print(f"Loaded {len(documents)} pages.")

    print("\nCreating chunks...")

    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\nFirst chunk:")
    print(chunks[0]["text"])

    print("\nSource:")
    print(chunks[0]["source"])

    print("\nPage:")
    print(chunks[0]["page"])