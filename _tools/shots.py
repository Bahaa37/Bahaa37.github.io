"""Screenshot tool for visual verification — the check CI cannot do.

Captures the PUBLISHED site (serve it first:
    python _tools/serve_publish.py 5217 publish/wwwroot
) at mobile 390x844 and desktop 1440x900, in both themes, into
.impeccable/review/shots-<stamp>/.

Pages scroll through once before capture so motion.js's additive reveal classes are
applied to everything below the fold (otherwise a full-page shot shows un-revealed
sections at their hidden state, which is what the motion rules guarantee will never
reach a reader but what a naive capture absolutely will show).

Gotcha that cost a debugging round: element crops of content near the viewport top
bleed the off-screen fixed chrome (header capsule, contact dock) into the crop,
because those elements are fixed relative to the viewport, not the page. Scrolling
back up by ~180px before the capture moves them out of the cropped region.

Usage: python _tools/shots.py <base-url> [out-dir]
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip("/")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else (
    Path(".impeccable/review") / f"shots-{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')}"
)
out.mkdir(parents=True, exist_ok=True)

VIEWPORTS = {"desktop": (1440, 900), "mobile": (390, 844)}
PAGES = [
    ("home", "/"),
    ("cv", "/cv"),
    ("study-legacy-modernization", "/work/legacy-modernization"),
    ("testimonials", "/testimonials"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        for name, width in VIEWPORTS.items():
            page = browser.new_page(viewport={"width": width[0], "height": width[1]})
            for route_name, route in PAGES:
                page.goto(base + route, wait_until="networkidle")
                page.evaluate(f"localStorage.setItem('theme', '{theme}')")
                page.reload(wait_until="networkidle")

                # Scroll through once so every .reveal section fires (threshold 0,
                # leading edge), then settle back near the top so fixed chrome sits
                # where a reader arriving at the page would see it.
                page.evaluate(
                    """async () => {
                        const step = window.innerHeight * 0.8;
                        for (let y = 0; y <= document.body.scrollHeight; y += step) {
                            window.scrollTo(0, y);
                            await new Promise(r => setTimeout(r, 60));
                        }
                        window.scrollTo(0, 0);
                    }"""
                )
                page.wait_for_timeout(700)

                page.screenshot(path=str(out / f"{route_name}-{theme}-{name}.png"), full_page=True)
            page.close()
    browser.close()

print(f"done: {out}")
