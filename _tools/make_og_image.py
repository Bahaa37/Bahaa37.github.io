"""Capture wwwroot/og.html as og-preview.png at exactly 1200x630.

The Open Graph tags in index.html are inert without this file: a client-rendered page
shows link crawlers nothing but the shell, and a pasted link is how this site actually
reaches a recruiter. Regenerate whenever og.html changes.

Usage:  python _tools/make_og_image.py
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "Cv.Web" / "wwwroot" / "og.html"
TARGET = ROOT / "src" / "Cv.Web" / "wwwroot" / "og-preview.png"

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


def find_chrome() -> Path | None:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate

    found = shutil.which("chrome") or shutil.which("google-chrome")
    return Path(found) if found else None


def main() -> int:
    if not SOURCE.exists():
        print(f"FAIL  source page not found: {SOURCE}")
        return 1

    chrome = find_chrome()
    if chrome is None:
        print("FAIL  Chrome not found.")
        return 1

    if TARGET.exists():
        TARGET.unlink()

    # A dedicated profile directory is required: headless Chrome silently produces
    # nothing when an interactive Chrome already holds the default profile.
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [
                str(chrome),
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--no-first-run",
                f"--user-data-dir={profile}",
                "--window-size=1200,630",
                "--default-background-color=00000000",
                "--hide-scrollbars",
                f"--screenshot={TARGET}",
                SOURCE.as_uri(),
            ],
            check=False,
            capture_output=True,
        )

    if not TARGET.exists():
        print("FAIL  no image produced.")
        return 1

    print(f"OK    {TARGET.name} written ({TARGET.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
