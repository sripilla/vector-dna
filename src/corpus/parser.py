from pathlib import Path


def parse_document(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    chunks = []
    current_section = None
    current_lines = []

    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Sphinx heading:
        # Heading text
        # ^^^^^^^^^^^^
        if (
            stripped
            and i + 1 < len(lines)
            and lines[i + 1].strip()
            and set(lines[i + 1].strip()) <= set("=*^~-")
            and len(lines[i + 1].strip()) >= 3
        ):
            if current_lines:
                chunks.append(
                    {
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                    }
                )
                current_lines = []

            current_section = stripped
            i += 2
            continue

        current_lines.append(line)
        i += 1

    if current_lines:
        chunks.append(
            {
                "section": current_section,
                "text": "\n".join(current_lines).strip(),
            }
        )

    return chunks