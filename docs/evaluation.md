# AeroCopilot — RAG Evaluation

## 1. Evaluation Objective

The purpose of this evaluation is to determine whether AeroCopilot can:

1. Retrieve the correct aviation document for a user question.
2. Provide answers grounded in the retrieved documents.
3. Refuse to answer when the required information is not present.
4. Return useful source and page citations.
5. Avoid unsupported or fabricated information.

The evaluation uses a controlled synthetic aviation document collection.

---

## 2. Test Dataset

The initial evaluation contains 8 test questions.

| ID | Question | Expected Source | Expected Behavior |
|---|---|---|---|
| Q001 | What should be checked during a hydraulic system inspection? | Inspection Manual | Answer |
| Q002 | What should be done if hydraulic leakage is detected? | Maintenance Manual | Answer |
| Q003 | What is required when performing a safety risk assessment? | Safety Procedures | Answer |
| Q004 | What should be done during an abnormal aircraft condition? | Operations Manual | Answer |
| Q005 | What is the maximum cruise speed of the AERO-100? | No source | Abstain |
| Q006 | What is the tire pressure for the AERO-100? | No source | Abstain |
| Q007 | What PPE should be used during maintenance? | Safety Procedures | Answer |
| Q008 | What should be checked during a visual inspection? | Inspection Manual | Answer |

---

## 3. Evaluation Method

Each question is passed through the complete AeroCopilot RAG pipeline:

User Question
↓
Semantic Retrieval
↓
Relevant Document Chunks
↓
Context Construction
↓
Groq LLM
↓
Grounded Response
↓
Citation Generation

For questions with an expected source, the evaluation checks whether the expected document appears among the retrieved results.

For questions where the information is intentionally absent, the evaluation checks whether AeroCopilot correctly abstains instead of generating an unsupported answer.

---

## 4. Evaluation Results

### Overall Results

- Total questions: **8**
- Passed: **8**
- Failed: **0**
- Retrieval accuracy: **100%**
- Behavior accuracy: **100%**

### Retrieval Accuracy

AeroCopilot correctly retrieved the expected source document for all answerable questions.

**Result: 8/8 — 100%**

### Abstention Behavior

AeroCopilot correctly recognized that the following information was not present in the available document collection:

- AERO-100 maximum cruise speed
- AERO-100 tire pressure

Instead of inventing values, the system returned an abstention response.

**Result: 2/2 — 100%**

---

## 5. Why Abstention Matters

Aviation information systems require a strong distinction between known and unknown information.

AeroCopilot is therefore designed not to treat every question as answerable.

When sufficient evidence cannot be found, the system responds:

> I could not find enough information in the available AeroCopilot documents to answer this question reliably.

This is an intentional product behavior.

The goal is to reduce unsupported responses and make the system's limitations visible to the user.

---

## 6. Citation Strategy

AeroCopilot returns citations based on the documents retrieved by the semantic search layer.

Each citation contains:

- Source document
- Page number
- Retrieval score

Duplicate document/page combinations are removed before the response is returned.

Example:

```text
Source: aero100_inspection_manual.pdf
Page: 1