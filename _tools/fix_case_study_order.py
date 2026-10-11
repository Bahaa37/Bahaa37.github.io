"""One-off: renumber caseStudies.displayOrder and strip any UTF-8 BOM.

A BOM breaks strict JSON parsers, and PowerShell's UTF8 encoding adds one.
"""

import json
from pathlib import Path

path = Path("src/Cv.Web/wwwroot/data/cv.json")

# utf-8-sig tolerates a BOM if present and discards it.
document = json.loads(path.read_text(encoding="utf-8-sig"))

order = [
    "legacy-modernization",
    "ai-enablement",
    "windoor-wizard-builder",
    "payment-gateway-middleware",
    "mvc-to-webapi-rebuild",
]

by_slug = {c["slug"]: c for c in document["caseStudies"]}
missing = [s for s in order if s not in by_slug]
if missing:
    raise SystemExit(f"Unknown slugs in ordering list: {missing}")

for index, slug in enumerate(order, start=1):
    by_slug[slug]["displayOrder"] = index

document["caseStudies"] = [by_slug[s] for s in order]

# Written without a BOM so the browser's fetch and System.Text.Json both parse it.
path.write_text(
    json.dumps(document, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
    newline="\n",
)

for study in document["caseStudies"]:
    print(f"  {study['displayOrder']}  {study['slug']}")
print(f"\nBOM removed, {len(document['caseStudies'])} case studies renumbered.")
