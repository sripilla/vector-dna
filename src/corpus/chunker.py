def chunk_sections(
    sections: list[dict],
    max_chars: int = 1000,
    source: str | None = None,
) -> list[dict]:
    chunks = []

    for section in sections:
        text = section["text"].strip()

        if not text:
            continue

        section_chunks = []

        if len(text) <= max_chars:
            section_chunks.append(text)
        else:
            words = text.split()
            current_words = []
            current_length = 0

            for word in words:
                additional_length = len(word) + (1 if current_words else 0)

                if current_length + additional_length > max_chars:
                    section_chunks.append(" ".join(current_words))
                    current_words = [word]
                    current_length = len(word)
                else:
                    current_words.append(word)
                    current_length += additional_length

            if current_words:
                section_chunks.append(" ".join(current_words))

        for text_chunk in section_chunks:
            chunks.append(
                {
                    "source": source,
                    "section": section["section"],
                    "text": text_chunk,
                }
            )

    for index, chunk in enumerate(chunks):
        chunk["chunk_index"] = index

    return chunks