from pathlib import Path
import sys
import json

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from src.rag_chain import ask_aerocopilot


# ---------------------------------------------------------
# Evaluation dataset
# ---------------------------------------------------------

TEST_FILE = PROJECT_ROOT / "tests" / "test_questions.json"


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def load_test_questions():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def contains_expected_source(result, expected_source):
    if not expected_source:
        return True

    citations = result.get("citations", [])

    for citation in citations:
        source = citation.get("source", "").lower()

        if expected_source.lower() in source:
            return True

    return False


def is_abstention(result):
    answer = result.get("answer", "").lower()

    abstention_phrases = [
        "could not find enough information",
        "not enough information",
        "cannot find enough information",
        "insufficient information",
        "i don't have enough information",
        "i do not have enough information",
    ]

    return any(
        phrase in answer
        for phrase in abstention_phrases
    )


# ---------------------------------------------------------
# Run evaluation
# ---------------------------------------------------------

def main():

    questions = load_test_questions()

    total = len(questions)
    passed = 0
    failed = 0

    retrieval_correct = 0
    behavior_correct = 0

    print("=" * 70)
    print("AeroCopilot RAG Evaluation")
    print("=" * 70)

    for question in questions:

        question_id = question["id"]
        question_text = question["question"]
        expected_source = question.get("expected_source")
        should_abstain = question.get("should_abstain", False)

        print()
        print(f"{question_id}: {question_text}")

        try:

            result = ask_aerocopilot(
                question_text,
                k=4
            )

            # -------------------------------------------------
            # Retrieval evaluation
            # -------------------------------------------------

            retrieval_ok = contains_expected_source(
                result,
                expected_source
            )

            if retrieval_ok:
                retrieval_correct += 1

            # -------------------------------------------------
            # Answer behavior evaluation
            # -------------------------------------------------

            if should_abstain:

                behavior_ok = is_abstention(result)

            else:

                behavior_ok = not is_abstention(result)

            if behavior_ok:
                behavior_correct += 1

            # -------------------------------------------------
            # Overall result
            # -------------------------------------------------

            if retrieval_ok and behavior_ok:

                passed += 1

                print("PASS")

            else:

                failed += 1

                print("FAIL")

                if not retrieval_ok:
                    print(
                        f"  Retrieval mismatch. "
                        f"Expected source: {expected_source}"
                    )

                if not behavior_ok:
                    print(
                        f"  Answer behavior mismatch. "
                        f"Expected abstention: {should_abstain}"
                    )

        except Exception as error:

            failed += 1

            print("ERROR")
            print(f"  {error}")

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    retrieval_accuracy = (
        retrieval_correct / total * 100
        if total
        else 0
    )

    behavior_accuracy = (
        behavior_correct / total * 100
        if total
        else 0
    )

    print()
    print("=" * 70)
    print("Evaluation Results")
    print("=" * 70)

    print(f"Total questions: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    print(
        f"Retrieval accuracy: "
        f"{retrieval_accuracy:.1f}%"
    )

    print(
        f"Behavior accuracy: "
        f"{behavior_accuracy:.1f}%"
    )

    print("=" * 70)


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()