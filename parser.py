import re


def parse_reference(reference):

    reference = " ".join(reference.split())

    doi_match = re.search(
        r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)",
        reference,
        re.IGNORECASE
    )

    doi = (
        doi_match.group(1)
        if doi_match
        else None
    )

    apa_match = re.match(
        r"^(.+?)\s*\((\d{4})\)\.?\s*(.+)$",
        reference
    )

    if apa_match:

        author = apa_match.group(1).strip()

        year = apa_match.group(2).strip()

        title = apa_match.group(3).strip()

        title = re.sub(
            r"^\.\s*",
            "",
            title
        )

        title = title.rstrip(".")

        return {
            "title": title,
            "author": author,
            "year": year,
            "doi": doi
        }

    year_match = re.search(
        r"\b(1[5-9]\d{2}|19\d{2}|20\d{2})\b",
        reference
    )

    year = (
        year_match.group(0)
        if year_match
        else None
    )

    words = reference.split()

    author = None

    if len(words) >= 2:

        if year and words[-1] == year:

            author = words[-2]

        else:

            author = words[-1]

    title = reference

    if doi:
        title = title.replace(
            doi,
            ""
        )

    if year:
        title = title.replace(
            year,
            ""
        )

    if author:
        title = title.replace(
            author,
            ""
        )

    title = " ".join(
        title.split()
    )

    title = title.rstrip(".")

    return {
        "title": title,
        "author": author,
        "year": year,
        "doi": doi
    }
