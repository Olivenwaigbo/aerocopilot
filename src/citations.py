from typing import List, Dict


def build_citations(results) -> List[Dict]:
    """
    Build clean, deduplicated citations from retrieved
    documents.
    """

    citations = []

    seen = set()

    for document, score in results:

        source = document.metadata.get(
            "source",
            "Unknown source",
        )

        page = document.metadata.get(
            "page",
            "Unknown page",
        )

        key = (source, page)

        if key in seen:
            continue

        seen.add(key)

        citations.append(
            {
                "source": source,
                "page": page,
                "score": round(float(score), 4),
            }
        )

    return citations