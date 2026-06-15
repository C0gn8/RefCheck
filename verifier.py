print("VERIFIER.PY LOADED")

import requests
from rapidfuzz import fuzz

from parser import parse_reference
from risk_analyzer import calculate_risk
from grey_literature import is_grey_literature

OPENALEX_URL = "https://api.openalex.org/works"
CROSSREF_URL = "https://api.crossref.org/works"


def search_openalex(title_search):

    try:

        r = requests.get(
            OPENALEX_URL,
            params={
                "search": title_search,
                "per-page": 10
            },
            timeout=3
        )

        data = r.json()

        return data.get(
            "results",
            []
        )

    except Exception:

        return []


def search_crossref(title_search, doi=None):

    try:

        if doi:

            r = requests.get(
                f"{CROSSREF_URL}/{doi}",
                timeout=3
            )

            if r.status_code == 200:

                data = r.json()

                return [
                    data.get(
                        "message",
                        {}
                    )
                ]

        r = requests.get(
            CROSSREF_URL,
            params={
                "query.title": title_search,
                "rows": 10
            },
            timeout=3
        )

        data = r.json()

        return (
            data.get(
                "message",
                {}
            ).get(
                "items",
                []
            )
        )

    except Exception:

        return []


def score_openalex(result, parsed):

    title_search = parsed.get("title") or ""
    author_search = parsed.get("author") or ""
    year_search = parsed.get("year")

    candidate_title = (
        result.get("display_name")
        or ""
    )

    title_score = fuzz.partial_ratio(
        title_search.lower(),
        candidate_title.lower()
    )

    author_score = 0

    if author_search:

        for author in result.get(
            "authorships",
            []
        ):

            author_name = (
                author.get(
                    "author",
                    {}
                ).get(
                    "display_name"
                )
                or ""
            )

            score = fuzz.partial_ratio(
                author_search.lower(),
                author_name.lower()
            )

            author_score = max(
                author_score,
                score
            )

    year_score = 0

    publication_year = result.get(
        "publication_year"
    )

    if (
        year_search
        and publication_year
        and str(year_search)
        == str(publication_year)
    ):
        year_score = 100

    confidence = (
        title_score * 0.7
        + author_score * 0.2
        + year_score * 0.1
    )

    return confidence, title_score


def score_crossref(result, parsed):

    title_search = parsed.get("title") or ""
    author_search = parsed.get("author") or ""
    year_search = parsed.get("year")

    title_list = result.get(
        "title",
        []
    )

    candidate_title = (
        title_list[0]
        if title_list
        else ""
    )

    title_score = fuzz.partial_ratio(
        title_search.lower(),
        candidate_title.lower()
    )

    author_score = 0

    if author_search:

        for author in result.get(
            "author",
            []
        ):

            family = (
                author.get("family")
                or ""
            )

            score = fuzz.partial_ratio(
                author_search.lower(),
                family.lower()
            )

            author_score = max(
                author_score,
                score
            )

    year_score = 0

    issued = result.get(
        "issued",
        {}
    )

    date_parts = issued.get(
        "date-parts",
        []
    )

    if date_parts and date_parts[0]:

        publication_year = str(
            date_parts[0][0]
        )

        if (
            year_search
            and publication_year
            == str(year_search)
        ):
            year_score = 100

    confidence = (
        title_score * 0.7
        + author_score * 0.2
        + year_score * 0.1
    )

    return confidence, title_score, candidate_title


def verify_reference(reference):

    parsed = parse_reference(
        reference
    )

    title_search = (
        parsed.get("title")
        or ""
    )

    openalex_results = search_openalex(
        title_search
    )

    crossref_results = search_crossref(
        title_search,
        parsed.get("doi")
    )

    best_openalex = None
    best_openalex_score = 0

    best_crossref_score = 0
    best_crossref_title = None

    for result in openalex_results:

        score, _ = score_openalex(
            result,
            parsed
        )

        if score > best_openalex_score:

            best_openalex_score = score
            best_openalex = result

    for result in crossref_results:

        score, _, candidate_title = score_crossref(
            result,
            parsed
        )

        if score > best_crossref_score:

            best_crossref_score = score
            best_crossref_title = candidate_title

    confidence = max(
        best_openalex_score,
        best_crossref_score
    )

    openalex_found = (
        best_openalex_score >= 70
    )

    crossref_found = (
        best_crossref_score >= 70
    )

    grey_literature = is_grey_literature(
        reference
    )

    if grey_literature:

        status = "grey_literature"

    elif (
        best_openalex_score < 70
        and best_crossref_score < 70
    ):

        status = "suspicious"

    elif (
        confidence >= 85
        and (
            openalex_found
            or crossref_found
        )
    ):

        status = "verified"

    elif confidence >= 60:

        status = "possible_match"

    else:

        status = "weak_match"

    result = {
        "status": status,

        "confidence": round(
            confidence,
            2
        ),

        "parsed": parsed,

        "doi": parsed.get("doi"),

        "openalex_found": openalex_found,
        "openalex_score": round(
            best_openalex_score,
            2
        ),

        "crossref_found": crossref_found,
        "crossref_score": round(
            best_crossref_score,
            2
        ),

        "matched_title": (
            best_openalex.get(
                "display_name"
            )
            if best_openalex
            else None
        ),

        "matched_crossref_title": (
            best_crossref_title
        ),

        "openalex_id": (
            best_openalex.get(
                "id"
            )
            if best_openalex
            else None
        )
    }

    result.update(
        calculate_risk(result)
    )

    return result
