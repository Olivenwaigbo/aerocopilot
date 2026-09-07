# AeroCopilot — System Architecture

## 1. Overview

AeroCopilot is an AI-powered aviation knowledge assistant built around a Retrieval-Augmented Generation (RAG) architecture.

The system retrieves relevant information from a controlled collection of aviation technical documents before passing that information to a large language model.

This architecture is designed to reduce unsupported answers and provide traceable responses.

---

## 2. High-Level Architecture

```text
                    AVIATION DOCUMENTS
                           |
                           v
                  +-------------------+
                  | Document Loader   |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  | Text Extraction   |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  | Document Chunker  |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  | Embedding Model   |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |    ChromaDB       |
                  |   Vector Store    |
                  +-------------------+
                           ^
                           |
                    Semantic Search
                           |
                    USER QUESTION
                           |
                           v
                  +-------------------+
                  |    Retriever      |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  | Relevant Chunks   |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |     Groq LLM      |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  | Grounded Answer   |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  | Citation Layer    |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |  AeroCopilot UI   |
                  +-------------------+
3. Document Ingestion

AeroCopilot currently uses a controlled collection of synthetic aviation PDF documents.

The ingestion pipeline:

Finds aviation PDF documents.
Extracts their text.
Preserves document and page metadata.
Splits the extracted text into smaller chunks.

Each chunk retains metadata such as:

Source document
Page number
Chunk ID

This metadata is later used for citations.

4. Chunking

The system uses RecursiveCharacterTextSplitter.

Current configuration:

Chunk size: 700 characters
Chunk overlap: 100 characters

The overlap helps preserve context between neighboring chunks.

The chunking strategy can be adjusted later based on retrieval evaluation results.

5. Embeddings

AeroCopilot uses:

sentence-transformers/all-MiniLM-L6-v2

The embedding model converts text into numerical vectors representing semantic meaning.

This allows AeroCopilot to retrieve conceptually similar text even when the wording of the user's question differs from the wording used in the source document.

6. Vector Database

The prototype uses ChromaDB as the vector store.

Collection:

aerocopilot_documents

The vector database stores:

Document chunks
Embeddings
Source metadata
Page metadata
Chunk identifiers

The database is persisted locally so that documents do not need to be re-embedded every time the application starts.

7. Retrieval

When a user submits a question, AeroCopilot performs semantic similarity search.

The current retrieval configuration returns:

Top K = 4

The retrieved chunks are then provided as context to the language model.

The retrieval layer is deliberately separated from the generation layer so that retrieval performance can be evaluated independently.

8. Retrieval-Augmented Generation

AeroCopilot uses Retrieval-Augmented Generation rather than asking the language model to answer from general knowledge.

The process is:

User Question
      ↓
Semantic Retrieval
      ↓
Relevant Document Chunks
      ↓
Context Assembly
      ↓
LLM
      ↓
Grounded Answer

The LLM is instructed to answer using the retrieved documentation rather than relying on unsupported knowledge.

9. Grounding and Abstention

A key design principle is that AeroCopilot should distinguish between:

Information that exists in the document collection

The system should answer using the retrieved evidence.

Information that does not exist

The system should abstain.

For example:

Question:
What is the maximum cruise speed of the AERO-100?

Response:
I could not find enough information in the available
AeroCopilot documents to answer this question reliably.

This behavior was explicitly tested during evaluation.

10. Citation Architecture

The citation layer extracts source information from retrieved documents.

Each citation contains:

Source
Page
Retrieval Score

Duplicate source/page combinations are removed.

This allows the application to present the evidence behind an answer without requiring the language model to invent citation references.

11. Application Layer

The current user interface is built using Streamlit.

The interface provides:

Aviation question input
Example questions
Grounded answers
Source citations
Retrieved evidence
Document collection information
System status
Responsible-use messaging
12. API Layer

The next development stage will expose AeroCopilot through a FastAPI backend.

The API will separate the application interface from the RAG engine.

Planned endpoints include:

GET  /health
POST /ask
GET  /documents
GET  /search

This architecture will allow AeroCopilot to eventually support:

Web applications
Mobile applications
Internal enterprise applications
Flutter clients
Other aviation software systems
13. Technology Stack
Frontend
Streamlit
Backend
FastAPI
RAG Framework
LangChain
Language Model
Groq
Embeddings
Sentence Transformers
Vector Database
ChromaDB
Document Processing
PyPDF
python-docx
Programming Language
Python
Testing
Pytest
14. Responsible AI

AeroCopilot is a research and product prototype.

It is not designed to:

Replace approved aircraft documentation
Replace qualified aviation professionals
Make autonomous maintenance decisions
Control aircraft systems
Control maintenance equipment
Provide regulatory certification
Override established procedures

The system should be treated as an information retrieval and decision-support tool.

15. Current Architecture Status

The core RAG architecture has been implemented and tested.

Current evaluation:

Test questions: 8
Passed: 8
Failed: 0

Retrieval accuracy: 100%
Behavior accuracy: 100%

These results are based on a small synthetic evaluation dataset and should not be interpreted as production-level aviation reliability.

16. Next Architecture Evolution

The next stage is to introduce a FastAPI service layer:

                  AeroCopilot UI
                         |
                         v
                    FastAPI API
                         |
                         v
                    RAG Engine
                    /        \
                   /          \
             Retriever       Groq
                 |
                 v
              ChromaDB
                 |
                 v
        Aviation Documents