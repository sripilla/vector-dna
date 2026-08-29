from src.evaluation.dataset import EVALUATION_DATASET
from src.generation.generator import Generator


def evaluate_generation():
    generator = Generator(top_k=3)

    results = []

    for item in EVALUATION_DATASET:
        question = item["question"]
        expected_topic = item["expected_topic"]

        answer = generator.answer(question)["answer"]

        if expected_topic is None:
            passed = (
                "I don't know based on the provided documentation."
                in answer
            )
        else:
            passed = expected_topic.lower() in answer.lower()

        results.append(
            {
                "question": question,
                "answer": answer,
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
    report = evaluate_generation()

    print("\n==============================")
    print("Generation Evaluation Report")
    print("==============================")

    print(f"Total questions: {report['total']}")
    print(f"Correct: {report['correct']}")
    print(f"Accuracy: {report['accuracy']:.2%}")

    print("\nDetails:")

    for result in report["results"]:
        status = "PASS" if result["passed"] else "FAIL"

        print(f"\n[{status}] {result['question']}")
        print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()