import re


def parse_reference(reference):

    year_match = re.search(r"\b(19|20)\d{2}\b", reference)

    year = year_match.group(0) if year_match else None

    words = reference.split()

    author = None

    if len(words) >= 2:
        author = words[-2]

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
