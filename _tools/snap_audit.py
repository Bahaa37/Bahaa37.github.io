"""Capture audit screenshots with a scroll-through pass so reveal sections fire.

Usage: python _tools/snap_audit.py <base-url> <out-dir>
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

base, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

VIEWPORTS = {"desktop": (1280, 900), "mobile": (390, 844)}
SHOTS = [("home", "/", True), ("cv", "/cv", False)]


def scroll_through(page):
    """Walk the page so every IntersectionObserver reveal fires, then return to top."""
    height = page.evaluate("document.body.scrollHeight")
    y = 0
    while y < height:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(220)
        y += 600
        height = page.evaluate("document.body.scrollHeight")
    page.wait_for_timeout(600)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        for vname, (w, h) in VIEWPORTS.items():
            page = browser.new_page(viewport={"width": w, "height": h},
                                    color_scheme=theme, device_scale_factor=2)
            for name, route, full in SHOTS:
                if name == "cv" and vname != "mobile":
                    continue
                page.goto(base + route, wait_until="networkidle")
                page.wait_for_timeout(1600)
                scroll_through(page)
                page.screenshot(path=str(out / f"{name}-{theme}-{vname}.png"), full_page=full)
            page.close()
    browser.close()
print("done:", out)
