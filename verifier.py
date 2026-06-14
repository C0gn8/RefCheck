print("VERIFIER.PY LOADED")

import requests
from rapidfuzz import fuzz
from parser import parse_reference


def verify_reference(reference):

    print("VERIFY_REFERENCE CALLED")

    parsed = parse_reference(reference)

    title_search = parsed["title"]
    author_search = parsed["author"]
    year_search = parsed["year"]

    r = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": title_search,
            "per-page": 10
        },
        timeout=10
    )

    data = r.json()

    if not data.get("results"):
        return {
            "status": "not_found",
            "parsed": parsed
        }

    best_match = None
    best_confidence = 0

    for result in data["results"]:

        candidate_title = result.get("display_name", "")

        title_score = fuzz.partial_ratio(
            title_search.lower(),
            candidate_title.lower()
        )

        author_score = 0

        authorships = result.get("authorships", [])

        if author_search and authorships:

            author_names = [
                a.get("author", {}).get("display_name", "")
                for a in authorships
            ]

            best_author_score = 0

            for name in author_names:

                score = fuzz.partial_ratio(
                    author_search.lower(),
                    name.lower()
                )

                if score > best_author_score:
                    best_author_score = score

            author_score = best_author_score

        year_score = 0

        publication_year = result.get("publication_year")

        if year_search and publication_year:

            if str(publication_year) == str(year_search):
                year_score = 100

        confidence = (
            title_score * 0.7 +
            author_score * 0.2 +
            year_score * 0.1
        )

        if confidence > best_confidence:
            best_confidence = confidence
            best_match = result

    if best_confidence >= 85:
        status = "verified"
    elif best_confidence >= 60:
        status = "possible_match"
    else:
        status = "weak_match"

    return {
        "status": status,
        "confidence": round(best_confidence, 2),
        "parsed": parsed,
        "matched_title": best_match.get("display_name"),
        "matched_year": best_match.get("publication_year"),
        "openalex_id": best_match.get("id")
    }
