def calculate_risk(result):

    risk_score = 0
    risk_flags = []

    openalex_found = result.get(
        "openalex_found",
        False
    )

    crossref_found = result.get(
        "crossref_found",
        False
    )

    confidence = result.get(
        "confidence",
        0
    )

    # Only penalize if BOTH databases fail

    if (
        not openalex_found
        and not crossref_found
    ):

        risk_score += 50

        risk_flags.append(
            "No database verification"
        )

    # Weak database match

    if (
        result.get(
            "openalex_score",
            0
        ) < 70
        and
        result.get(
            "crossref_score",
            0
        ) < 70
    ):

        risk_score += 20

        risk_flags.append(
            "No strong database match"
        )

    # Confidence checks

    if confidence < 60:

        risk_score += 15

        risk_flags.append(
            "Low confidence match"
        )

    if confidence < 40:

        risk_score += 15

        risk_flags.append(
            "Very low confidence match"
        )

    # Parser quality checks

    parsed = result.get(
        "parsed",
        {}
    )

    if not parsed.get("author"):

        risk_score += 10

        risk_flags.append(
            "Author not detected"
        )

    if not parsed.get("year"):

        risk_score += 10

        risk_flags.append(
            "Year not detected"
        )

    # Grey literature should not be treated
    # as inherently risky

    if (
        result.get("status")
        == "grey_literature"
    ):

        risk_score = max(
            0,
            risk_score - 30
        )

    risk_score = min(
        risk_score,
        100
    )

    if risk_score >= 70:

        risk_level = "high"

    elif risk_score >= 40:

        risk_level = "medium"

    else:

        risk_level = "low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_flags": risk_flags
    }
