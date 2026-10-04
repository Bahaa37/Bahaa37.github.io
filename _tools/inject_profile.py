"""Fill the contact placeholders in cv.json from environment variables.

The repository is public, so personal contact details are not stored in it. cv.json
carries ${NAME} placeholders; CI runs this before tests and publish with the values
supplied as GitHub Actions secrets. A missing value fails the build rather than
publishing a placeholder.

Usage:  python _tools/inject_profile.py
"""

import json
import os
import re
import sys
from pathlib import Path

CV_JSON = Path(__file__).resolve().parent.parent / "src" / "Cv.Web" / "wwwroot" / "data" / "cv.json"
PLACEHOLDER = re.compile(r"^\$\{([A-Z0-9_]+)\}$")


def main() -> int:
    document = json.loads(CV_JSON.read_text(encoding="utf-8"))
    profile = document["profile"]
    missing = []

    for key, value in profile.items():
        match = PLACEHOLDER.match(value) if isinstance(value, str) else None
        if not match:
            continue
        name = match.group(1)
        secret = os.environ.get(name, "").strip()
        if not secret:
            missing.append(name)
            continue
        profile[key] = secret

    if missing:
        print("FAIL  Missing environment values for: " + ", ".join(missing), file=sys.stderr)
        return 1

    CV_JSON.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("OK    Contact placeholders filled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
