from pathlib import Path
import csv
import sys

from bibliography_parser import split_references
from verifier import verify_reference


def evaluate_file(filepath):

    text = Path(filepath).read_text(
        encoding="utf-8"
    )

    references = split_references(text)

    print()
    print(f"Processing: {filepath}")
    print(f"Found {len(references)} references")

    verified = 0
    possible = 0
    weak = 0
    suspicious = 0
    grey_literature = 0

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    total_risk = 0

    flagged = []

    verified_refs = []
    possible_refs = []

    all_results = []

    for i, reference in enumerate(
        references,
        start=1
    ):

        print(
            f"Checking {i}/{len(references)}",
            end="\r"
        )

        result = verify_reference(
            reference
        )

        all_results.append({
            "reference": reference,
            "result": result
        })

        total_risk += result[
            "risk_score"
        ]

        status = result[
            "status"
        ]

        if status == "verified":

            verified += 1

            verified_refs.append({
                "reference": reference,
                "result": result
            })

        elif status == "possible_match":

            possible += 1

            possible_refs.append({
                "reference": reference,
                "result": result
            })

        elif status == "weak_match":

            weak += 1

        elif status == "suspicious":

            suspicious += 1

        elif status == "grey_literature":

            grey_literature += 1

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
        "grey_literature": grey_literature,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "integrity_score": integrity_score,
        "flagged": flagged,
        "verified_refs": verified_refs,
        "possible_refs": possible_refs,
        "all_results": all_results
    }


def export_csv(report):

    filename = "refcheck_results.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "reference",
            "status",
            "confidence",
            "risk_score",
            "risk_level"
        ])

        for item in report[
            "all_results"
        ]:

            result = item["result"]

            writer.writerow([
                item["reference"],
                result["status"],
                result["confidence"],
                result["risk_score"],
                result["risk_level"]
            ])

    print()
    print(
        f"CSV exported: {filename}"
    )


def print_report(report):

    print()
    print("=" * 60)
    print(f"FILE: {report['file']}")
    print("=" * 60)

    print(f"References: {report['total']}")
    print(f"Verified: {report['verified']}")
    print(f"Possible: {report['possible_matches']}")
    print(f"Weak: {report['weak_matches']}")
    print(f"Suspicious: {report['suspicious']}")
    print(
        f"Grey Literature: "
        f"{report['grey_literature']}"
    )

    print()
    print(
        f"Integrity Score: "
        f"{report['integrity_score']}"
    )

    print()
    print(
        f"High Risk: "
        f"{report['high_risk']}"
    )

    print(
        f"Medium Risk: "
        f"{report['medium_risk']}"
    )

    print(
        f"Low Risk: "
        f"{report['low_risk']}"
    )


if __name__ == "__main__":

    csv_mode = (
        "--csv" in sys.argv
    )

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

            if csv_mode:

                export_csv(
                    report
                )

        else:

            print(
                f"Missing: {filepath}"
            )
