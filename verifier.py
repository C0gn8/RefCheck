print("VERIFIER.PY LOADED")

import requests
from rapidfuzz import fuzz


def verify_reference(reference):

    print("VERIFY_REFERENCE CALLED")

    r = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": reference,
            "per-page": 5
        },
        timeout=10
    )

    data = r.json()

    if not data.get("results"):
        return {
            "status": "not_found"
        }

    best_match = None
    best_score = 0

    for result in data["results"]:

        title = result.get("display_name", "")

        score = fuzz.partial_ratio(
            reference.lower(),
            title.lower()
        )

        if score > best_score:
            best_score = score
            best_match = result

    if best_score >= 80:
        status = "verified"
    elif best_score >= 50:
        status = "possible_match"
    else:
        status = "weak_match"

    return {
        "status": status,
        "confidence": best_score,
        "matched_title": best_match.get("display_name"),
        "openalex_id": best_match.get("id")
    }
