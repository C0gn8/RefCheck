print("VERIFIER.PY LOADED")

import requests
from rapidfuzz import fuzz
from parser import parse_reference


def verify_reference(reference):

    print("VERIFY_REFERENCE CALLED")

    parsed = parse_reference(reference)

    title_search = parsed["title"]

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
    best_score = 0

    for result in data["results"]:

        candidate_title = result.get("display_name", "")

        score = fuzz.ratio(
            title_search.lower(),
            candidate_title.lower()
        )

        if score > best_score:
            best_score = score
            best_match = result

    if best_score >= 90:
        status = "verified"
    elif best_score >= 70:
        status = "possible_match"
    else:
        status = "weak_match"

    return {
        "status": status,
        "confidence": round(best_score, 2),
        "parsed": parsed,
        "matched_title": best_match.get("display_name"),
        "openalex_id": best_match.get("id")
    }
