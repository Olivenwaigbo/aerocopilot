from pathlib import Path
from typing import List, Dict

import fitz  # PyMuPDF


BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def load_pdf_documents() -> List[Dict]:
    """
    Load all PDF documents from the documents directory.

    Returns:
        A list of dictionaries containing:
        - extracted text
        - source filename
        - page number
    """

    documents = []

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF documents found in {DOCUMENTS_DIR}"
        )

    for pdf_path in pdf_files:

        pdf = fitz.open(pdf_path)

        for page_number, page in enumerate(pdf):

            text = page.get_text("text").strip()

            if not text:
                continue

            documents.append(
                {
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_number + 1,
                }
            )

        pdf.close()

    return documents


if __name__ == "__main__":

    docs = load_pdf_documents()

    print(f"\nLoaded {len(docs)} pages.\n")

    for doc in docs[:5]:

        print("=" * 70)
        print(f"Source: {doc['source']}")
        print(f"Page: {doc['page']}")
        print("-" * 70)
        print(doc["text"][:500])
        print()