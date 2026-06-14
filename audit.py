def generate_audit(results):

    total = len(results)

    verified = 0
    possible = 0
    suspicious = 0
    weak = 0

    flagged_references = []

    total_risk = 0

    for item in results:

        result = item["result"]

        total_risk += result["risk_score"]

        if result["status"] == "verified":
            verified += 1

        elif result["status"] == "possible_match":
            possible += 1

        elif result["status"] == "weak_match":
            weak += 1

        elif result["status"] == "suspicious":
            suspicious += 1

        if result["risk_level"] != "low":

            flagged_references.append({
                "reference": item["reference"],
                "risk_level": result["risk_level"],
                "risk_score": result["risk_score"],
                "risk_flags": result["risk_flags"]
            })

    average_risk = (
        total_risk / total
        if total > 0
        else 100
    )

    integrity_score = round(
        max(0, 100 - average_risk),
        2
    )

    if integrity_score >= 85:
        overall_risk = "low"

    elif integrity_score >= 60:
        overall_risk = "medium"

    else:
        overall_risk = "high"

    return {
        "total_references": total,
        "verified": verified,
        "possible_matches": possible,
        "weak_matches": weak,
        "suspicious": suspicious,
        "integrity_score": integrity_score,
        "overall_risk": overall_risk,
        "flagged_references": flagged_references
    }
