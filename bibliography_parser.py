import re


def split_references(text):

    text = text.replace("\r\n", "\n")

    # Handle numbered bibliographies:
    # 1.
    # 2.
    # 3.

    numbered_refs = re.split(
        r"\n?\s*(?=\d+\.\s)",
        text
    )

    numbered_refs = [
        ref.strip()
        for ref in numbered_refs
        if ref.strip()
    ]

    if len(numbered_refs) > 1:

        cleaned = []

        for ref in numbered_refs:

            ref = re.sub(
                r"^\d+\.\s*",
                "",
                ref
            )

            ref = " ".join(
                ref.split()
            )

            cleaned.append(ref)

        return cleaned

    # Fallback:
    # blank-line-separated references

    references = []

    current = []

    for line in text.splitlines():

        line = line.strip()

        if not line:

            if current:

                references.append(
                    " ".join(current)
                )

                current = []

            continue

        current.append(line)

    if current:

        references.append(
            " ".join(current)
        )

    cleaned = []

    for ref in references:

        ref = " ".join(
            ref.split()
        )

        if ref:

            cleaned.append(ref)

    return cleaned
