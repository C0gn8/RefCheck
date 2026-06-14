import re


def parse_reference(reference):

    reference = " ".join(reference.split())

    year_match = re.search(
        r"\((1[5-9]\d{2}|19\d{2}|20\d{2})\)",
        reference
    )

    if year_match:

        year = year_match.group(1)

        before_year = reference[:year_match.start()].strip()
        after_year = reference[year_match.end():].strip()

        author = before_year
        title = after_year

        return {
            "title": title,
            "author": author,
            "year": year
        }

    year_match = re.search(
        r"\b(1[5-9]\d{2}|19\d{2}|20\d{2})\b",
        reference
    )

    year = year_match.group(0) if year_match else None

    words = reference.split()

    author = None

    if len(words) >= 2:

        if year and words[-1] == year:
            author = words[-2]

        else:
            author = words[-1]

    title = reference

    if year:
        title = title.replace(year, "")

    if author:
        title = title.replace(author, "")

    title = " ".join(title.split())

    return {
        "title": title,
        "author": author,
        "year": year
    }
