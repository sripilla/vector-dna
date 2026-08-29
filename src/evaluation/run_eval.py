from src.evaluation.retrieval_eval import evaluate_retrieval
from src.evaluation.generation_eval import evaluate_generation


def main():
    print("\n================================")
    print("VectorDNA Evaluation")
    print("================================")

    print("\nRunning retrieval evaluation...")
    retrieval_report = evaluate_retrieval()

    print("\nRunning generation evaluation...")
    generation_report = evaluate_generation()

    print("\n================================")
    print("FINAL EVALUATION")
    print("================================")

    print(
        f"Retrieval accuracy: "
        f"{retrieval_report['accuracy']:.2%}"
    )

    print(
        f"Generation accuracy: "
        f"{generation_report['accuracy']:.2%}"
    )


if __name__ == "__main__":
    main()