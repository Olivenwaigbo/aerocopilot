from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter

from document_loader import load_pdf_documents


def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 700,
    chunk_overlap: int = 100,
):
    """
    Split extracted documents into smaller searchable chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
        ],
    )

    chunks = []

    for document in documents:

        split_texts = splitter.split_text(document["text"])

        for index, text in enumerate(split_texts):

            chunks.append(
                {
                    "text": text,
                    "source": document["source"],
                    "page": document["page"],
                    "chunk_id": index,
                }
            )

    return chunks


if __name__ == "__main__":

    documents = load_pdf_documents()

    chunks = chunk_documents(documents)

    print(f"\nDocuments/pages loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}\n")

    for chunk in chunks[:5]:

        print("=" * 70)
        print(f"Source: {chunk['source']}")
        print(f"Page: {chunk['page']}")
        print(f"Chunk: {chunk['chunk_id']}")
        print("-" * 70)
        print(chunk["text"])
        print()