def build_context(results):
    """Convert retrieved chunks into clean LLM context."""

    parts = []

    for i, result in enumerate(results, start=1):
        parts.append(
            f"""Source {i}
Source: {result["source"]}
Section: {result["section"]}

{result["text"]}"""
        )

    return "\n\n---\n\n".join(parts)