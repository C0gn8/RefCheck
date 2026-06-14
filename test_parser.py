from pathlib import Path
from bibliography_parser import split_references

text = Path(
    "test_data/real_bibliography.txt"
).read_text(
    encoding="utf-8"
)

refs = split_references(text)

print(
    f"References found: {len(refs)}"
)

for i, ref in enumerate(refs[:10], start=1):

    print()
    print(i)
    print(ref[:200])
