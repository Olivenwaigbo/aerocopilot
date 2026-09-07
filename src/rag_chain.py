import os
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.retriever import search_documents
from src.citations import build_citations


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ---------------------------------------------------------
# GROQ CONFIGURATION
# ---------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Check your .env file."
    )


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY,
)


# ---------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are AeroCopilot, an aviation knowledge assistant.

Your job is to answer questions using ONLY the
information provided in the retrieved aviation documents.

IMPORTANT RULES:

1. Do not invent information.

2. Do not use outside knowledge to fill gaps.

3. If the retrieved documents do not contain enough
   information to answer the question, clearly say:

   "I could not find enough information in the available
   AeroCopilot documents to answer this question reliably."

4. Never fabricate procedures, measurements, limits,
   aircraft specifications, maintenance instructions,
   regulatory requirements, or safety information.

5. Keep answers clear and concise.

6. When possible, reference the source document and
   page number.

7. AeroCopilot is a research prototype and must not
   replace approved aviation documentation or qualified
   aviation professionals.

Retrieved aviation information:

{context}
"""


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


# ---------------------------------------------------------
# CONTEXT BUILDER
# ---------------------------------------------------------

def build_context(results) -> str:
    """
    Convert retrieved documents into a context string
    that can be passed to the LLM.
    """

    context_parts = []

    for index, (document, score) in enumerate(
        results,
        start=1,
    ):

        source = document.metadata.get(
            "source",
            "Unknown source",
        )

        page = document.metadata.get(
            "page",
            "Unknown page",
        )

        text = document.page_content.strip()

        context_parts.append(
            f"""
SOURCE {index}
Document: {source}
Page: {page}

{text}
"""
        )

    return "\n".join(context_parts)


# ---------------------------------------------------------
# RAG FUNCTION
# ---------------------------------------------------------

def ask_aerocopilot(
    question: str,
    k: int = 4,
) -> Dict:

    # Retrieve relevant evidence
    results = search_documents(
        question,
        k=k,
    )

    # Build context
    context = build_context(results)

    # Generate grounded answer
    messages = prompt.format_messages(
        question=question,
        context=context,
    )

    response = llm.invoke(messages)

    citations = build_citations(results)

    return {
        "question": question,
        "answer": response.content,
        "citations": citations,
        "retrieved_documents": results,
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    question = (
        "What should be checked during a hydraulic system inspection?"
    )

    print("\n" + "=" * 70)
    print("AEROCOPILOT")
    print("=" * 70)

    print("\nQUESTION:")
    print(question)

    result = ask_aerocopilot(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for citation in result["citations"]:

        print(
            f"- {citation['source']} "
            f"(Page {citation['page']})"
        )

    print("\n" + "=" * 70)