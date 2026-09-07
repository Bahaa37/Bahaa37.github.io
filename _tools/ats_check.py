"""ATS gate for the generated CV PDF.

An applicant tracking system reads the PDF's text layer, not its appearance. If the
text does not come out clean and in reading order, the CV is filtered out before a
human ever sees it. This script is the acceptance criterion for the print renderer.

Usage:  python _tools/ats_check.py [path-to-pdf]
"""

import sys
from pathlib import Path

from pypdf import PdfReader

DEFAULT_PDF = Path(__file__).resolve().parent.parent / "output" / "Bahaa-Aldeen-Mohamed-CV.pdf"

# Section headings that must survive extraction.
REQUIRED_HEADINGS = [
    "PROFESSIONAL SUMMARY",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "AWARDS AND RECOGNITION",
    "EDUCATION",
    "CERTIFICATIONS",
]

# Facts a recruiter or parser must be able to read.
REQUIRED_FACTS = [
    "Bahaa Aldeen Mohamed",
    "Andalusia Business Solutions",
    "PS Digital",
    "MEEM Development",
    "BahaaMohamed37@gmail.com",
    "+20 105 555 3796",
    "github.com/Bahaa37",
    "linkedin.com/in/bahaamohamed-dev",
    # The portfolio URL is the CV's only route to the case studies and diagrams. If it
    # does not extract, it is as broken as an unreadable phone number.
    "bahaa37.github.io",
    "5-7 working days reduced to a maximum of 3",
    "9 countries",
]

MAX_PAGES = 2


def main() -> int:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF

    if not pdf_path.exists():
        print(f"FAIL  PDF not found: {pdf_path}")
        return 1

    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages)
    # Normalise the dashes and non-breaking spaces a PDF renderer introduces.
    flat = " ".join(text.replace("–", "-").replace("—", "-").replace("\xa0", " ").split())

    failures: list[str] = []
    warnings: list[str] = []

    print(f"PDF:   {pdf_path.name}")
    print(f"Pages: {len(reader.pages)}")
    print(f"Chars extracted: {len(text):,}")
    print()

    if len(text.strip()) < 1500:
        failures.append(
            f"Only {len(text.strip())} characters extracted — the text layer is missing or the "
            "content was rendered as graphics."
        )

    if len(reader.pages) > MAX_PAGES:
        warnings.append(f"{len(reader.pages)} pages; the target is {MAX_PAGES}.")

    print("Section headings")
    for heading in REQUIRED_HEADINGS:
        ok = heading.lower() in flat.lower()
        print(f"  {'OK  ' if ok else 'MISS'}  {heading}")
        if not ok:
            failures.append(f"Heading not extractable: {heading}")

    print()
    print("Required facts")
    for fact in REQUIRED_FACTS:
        needle = " ".join(fact.replace("–", "-").split()).lower()
        ok = needle in flat.lower()
        print(f"  {'OK  ' if ok else 'MISS'}  {fact}")
        if not ok:
            failures.append(f"Fact not extractable: {fact}")

    print()
    print("Reading order")
    # Headings must appear in the same order the document presents them. Multi-column or
    # float-based layouts scramble this, which is the classic way a CV parses wrongly.
    positions = [(h, flat.lower().find(h.lower())) for h in REQUIRED_HEADINGS]
    found = [(h, i) for h, i in positions if i >= 0]
    ordered = all(found[i][1] < found[i + 1][1] for i in range(len(found) - 1))
    print(f"  {'OK  ' if ordered else 'FAIL'}  headings appear in document order")
    if not ordered:
        failures.append("Headings extract out of order — layout is not linear.")

    print()
    if warnings:
        for warning in warnings:
            print(f"WARN  {warning}")
        print()

    if failures:
        print(f"RESULT: FAIL ({len(failures)} issue{'s' if len(failures) != 1 else ''})")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("RESULT: PASS — the PDF is machine-readable and in reading order.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
