def calculate_risk(result):

    risk_score = 0
    risk_flags = []

    if not result["openalex_found"]:
        risk_score += 25
        risk_flags.append(
            "No OpenAlex verification"
        )

    if not result["crossref_found"]:
        risk_score += 25
        risk_flags.append(
            "No Crossref verification"
        )

    if (
        result["openalex_score"] < 70
        and result["crossref_score"] < 70
    ):
        risk_score += 30
        risk_flags.append(
            "No strong database match"
        )

    confidence = result["confidence"]

    if confidence < 60:
        risk_score += 20
        risk_flags.append(
            "Low confidence match"
        )

    if confidence < 40:
        risk_score += 20
        risk_flags.append(
            "Very low confidence match"
        )

    title_similarity = result.get(
        "title_similarity",
        100
    )

    if title_similarity < 75:
        risk_score += 20
        risk_flags.append(
            "Major title mismatch"
        )

    parsed = result["parsed"]

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
