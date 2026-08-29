from src.evaluation.dataset import EVALUATION_DATASET
from src.retrieval.retriever import Retriever


def evaluate_retrieval():
    retriever = Retriever(top_k=3)

    results = []

    for item in EVALUATION_DATASET:
        question = item["question"]
        expected_source = item["expected_source"]

        retrieved = retriever.search(question)

        retrieved_sources = [
            result["source"]
            for result in retrieved
        ]

        if expected_source is None:
            passed = len(retrieved) == 0
        else:
            passed = expected_source in retrieved_sources

        results.append(
            {
                "question": question,
                "expected_source": expected_source,
                "retrieved_sources": retrieved_sources,
                "passed": passed,
            }
        )

    correct = sum(
        1 for result in results
        if result["passed"]
    )

    total = len(results)

    accuracy = correct / total if total else 0

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "results": results,
    }


def main():
    report = evaluate_retrieval()

    print("\n==============================")
    print("Retrieval Evaluation Report")
    print("==============================")

    print(f"Total questions: {report['total']}")
    print(f"Correct: {report['correct']}")
    print(f"Accuracy: {report['accuracy']:.2%}")

    print("\nDetails:")

    for result in report["results"]:
        status = "PASS" if result["passed"] else "FAIL"

        print(f"\n[{status}] {result['question']}")
        print(f"Expected: {result['expected_source']}")
        print(f"Retrieved: {result['retrieved_sources']}")


if __name__ == "__main__":
    main()