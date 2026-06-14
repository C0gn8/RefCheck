import re


def split_references(text):

    lines = text.splitlines()

    references = []
    current_reference = []

    for line in lines:

        line = line.strip()

        if not line:

            if current_reference:

                references.append(
                    " ".join(current_reference)
                )

                current_reference = []

            continue

        current_reference.append(line)

    if current_reference:

        references.append(
            " ".join(current_reference)
        )

    cleaned = []

    for reference in references:

        reference = re.sub(
            r"\s+",
            " ",
            reference
        ).strip()

        if reference:

            cleaned.append(reference)

    return cleaned
