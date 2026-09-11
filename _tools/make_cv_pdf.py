"""Print the live /cv route to the PDF that gets emailed to employers.

The PDF used to be produced by hand, from a browser's print dialog. That works once and
then rots: every edit to cv.json moved the site while the downloadable file stayed where
it was, so the copy a recruiter received disagreed with the copy they were looking at.

Rendering it from the published build makes that impossible — the file is a projection
of the same cv.json as the page, produced by the same renderer, on every deploy.

Chromium is used rather than a PDF library on purpose: PrintCv.razor and print.css are
already the CV's layout, and reimplementing them in a second toolchain would give two
documents to keep in step instead of one.

Usage:  python _tools/make_cv_pdf.py <publish-dir> <output.pdf> [--port 5211]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def serve(publish_dir: Path, port: int) -> subprocess.Popen:
    process = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "_tools" / "serve_publish.py"), str(port), str(publish_dir)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"http://localhost:{port}/index.html", timeout=2):
                return process
        except (urllib.error.URLError, ConnectionError, OSError):
            time.sleep(0.25)

    process.terminate()
    raise SystemExit("make_cv_pdf: the static server never came up.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("publish_dir", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, default=5211)
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("make_cv_pdf: playwright is not installed (pip install playwright).", file=sys.stderr)
        return 1

    server = serve(args.publish_dir, args.port)

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://localhost:{args.port}/cv", wait_until="networkidle")

            # Wait for Blazor to replace the prerendered body with the real CV. Without
            # this the PDF captures the boot state, which is the failure this whole
            # script exists to make impossible.
            page.wait_for_selector("article.cv", timeout=60_000)
            page.wait_for_selector("article.cv h2", timeout=60_000)

            page.emulate_media(media="print")

            args.output.parent.mkdir(parents=True, exist_ok=True)
            page.pdf(
                path=str(args.output),
                format="A4",
                print_background=False,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )

            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)

    size_kb = args.output.stat().st_size / 1024
    print(f"make_cv_pdf: wrote {args.output} ({size_kb:,.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
