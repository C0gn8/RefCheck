from pathlib import Path
import sys

from evaluate import (
    evaluate_file,
    print_report,
    export_csv,
    export_html
)


def print_usage():

    print()
    print("RefCheck v0.1")
    print()
    print("Usage:")
    print(
        "python refcheck.py "
        "<bibliography_file>"
    )
    print()
    print("Optional flags:")
    print("--csv")
    print("--html")
    print()

    sys.exit(1)


def main():

    if len(sys.argv) < 2:

        print_usage()

    filepath = sys.argv[1]

    csv_mode = (
        "--csv" in sys.argv
    )

    html_mode = (
        "--html" in sys.argv
    )

    if not Path(filepath).exists():

        print()
        print(
            f"File not found: "
            f"{filepath}"
        )

        sys.exit(1)

    print()
    print("=" * 60)
    print("RefCheck v0.1")
    print("=" * 60)

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

    if html_mode:

        export_html(
            report
        )

    print()
    print("=" * 60)
    print("Analysis Complete")
    print("=" * 60)


if __name__ == "__main__":

    main()
