import re


def split_references(text):

    text = text.replace("\r\n", "\n")

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    references = []
    current = []

    for line in lines:

        # Numbered styles:
        #
        # 1. Author...
        # [1] Author...
        #

        starts_new = (
            re.match(r"^\d+\.", line)
            or re.match(r"^\[\d+\]", line)
        )

        # Author-year styles:
        #
        # Smith J (2020)
        # Brown A. (2018)
        #

        if re.match(
            r"^[A-Z][A-Za-z' -]+.*\(\d{4}\)",
            line
        ):
            starts_new = True

        if starts_new:

            if current:

                references.append(
                    " ".join(current)
                )

            current = [line]

        else:

            current.append(line)

    if current:

        references.append(
            " ".join(current)
        )

    cleaned = []

    for ref in references:

        ref = re.sub(
            r"^\d+\.\s*",
            "",
            ref
        )

        ref = re.sub(
            r"^\[\d+\]\s*",
            "",
            ref
        )

        ref = " ".join(
            ref.split()
        )

        if ref:

            cleaned.append(ref)

    return cleaned
