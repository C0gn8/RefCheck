from pathlib import Path

from bibliography_parser import split_references
from verifier import verify_reference


def evaluate_file(filepath):

    text = Path(filepath).read_text(
        encoding="utf-8"
    )

    references = split_references(text)

    verified = 0
    possible = 0
    weak = 0
    suspicious = 0

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    total_risk = 0

    flagged = []

    for reference in references:

        result = verify_reference(
            reference
        )

        total_risk += result[
            "risk_score"
        ]

        status = result[
            "status"
        ]

        if status == "verified":
            verified += 1

        elif status == "possible_match":
            possible += 1

        elif status == "weak_match":
            weak += 1

        elif status == "suspicious":
            suspicious += 1

        risk_level = result[
            "risk_level"
        ]

        if risk_level == "high":

            high_risk += 1

            flagged.append({
                "reference": reference,
                "risk_score": result[
                    "risk_score"
                ],
                "flags": result[
                    "risk_flags"
                ]
            })

        elif risk_level == "medium":
            medium_risk += 1

        else:
            low_risk += 1

    total = len(references)

    average_risk = (
        total_risk / total
        if total > 0
        else 100
    )

    integrity_score = round(
        max(
            0,
            100 - average_risk
        ),
        2
    )

    return {
        "file": filepath,
        "total": total,
        "verified": verified,
        "possible_matches": possible,
        "weak_matches": weak,
        "suspicious": suspicious,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "integrity_score": integrity_score,
        "flagged": flagged
    }


def print_report(report):

    print()
    print("=" * 60)

    print(
        f"FILE: {report['file']}"
    )

    print("=" * 60)

    print(
        f"References: {report['total']}"
    )

    print(
        f"Verified: {report['verified']}"
    )

    print(
        f"Possible: {report['possible_matches']}"
    )

    print(
        f"Weak: {report['weak_matches']}"
    )

    print(
        f"Suspicious: {report['suspicious']}"
    )

    print()

    print(
        f"Integrity Score: "
        f"{report['integrity_score']}"
    )

    print()

    print(
        f"High Risk: {report['high_risk']}"
    )

    print(
        f"Medium Risk: {report['medium_risk']}"
    )

    print(
        f"Low Risk: {report['low_risk']}"
    )

    if report["flagged"]:

        print()
        print("FLAGGED REFERENCES")

        for item in report[
            "flagged"
        ]:

            print()

            print(
                f"- {item['reference']}"
            )

            print(
                f"  Risk: "
                f"{item['risk_score']}"
            )

            print(
                f"  Flags: "
                f"{', '.join(item['flags'])}"
            )


if __name__ == "__main__":

    files = [

        "test_data/real_bibliography.txt",

        "test_data/mixed_bibliography.txt",

        "test_data/fake_bibliography.txt"
    ]

    for filepath in files:

        if Path(filepath).exists():

            report = evaluate_file(
                filepath
            )

            print_report(
                report
            )

        else:

            print()

            print(
                f"Missing: {filepath}"
            )
