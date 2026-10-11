"""Render the site's icons — favicon, install icons, Apple touch icon — from one drawing.

The icons used to be the Blazor template's purple flame, which made the browser tab and an
installed app look like every other unconfigured Blazor project. The mark here is a
terminal prompt, `>B` and a block cursor, in the Hairline palette: the same near-black and
mint as the hero console, so the icon and the page it opens read as one thing.

Every size comes from the same SVG rather than from downscaling one PNG, because the
variants are not the same picture:

  * "any" icons keep rounded corners — desktop shelves show them as drawn.
  * the maskable icon is full-bleed with the mark scaled into the central 80% safe zone,
    because Android crops it to whatever shape the launcher uses.
  * the Apple touch icon is square and full-bleed — iOS rounds it itself, and a
    pre-rounded icon gets black corners.
  * the favicon drops the prompt: at 16–32 px three glyphs smear, two stay legible.

Chromium (via Playwright, already a publish dependency) draws it so the glyphs are real
Geist Mono, fetched from Google Fonts at render time. That needs network once, here —
the PNGs are committed and the site never depends on it. Re-run after changing the mark.

Usage:  python _tools/make_icons.py
"""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

WWWROOT = Path(__file__).resolve().parent.parent / "src" / "Cv.Web" / "wwwroot"

FONT = "https://fonts.googleapis.com/css2?family=Geist+Mono:wght@800&display=block"


def mark_svg(corner_radius: int, scale: float, with_prompt: bool) -> str:
    """The mark on a 512 canvas, drawn around the centre so `scale` shrinks it in place."""
    # Without the prompt glyph the B and cursor shift left to stay optically centred.
    shift = -28 if with_prompt else -92
    prompt = (
        '<text x="-150" y="76" font-family="Geist Mono" font-weight="800" font-size="210" '
        'fill="#6ee7a0" fill-opacity=".55">&gt;</text>'
        if with_prompt
        else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<defs>
  <radialGradient id="glow" cx=".28" cy=".18" r="1.05">
    <stop offset="0" stop-color="#103324"/><stop offset=".55" stop-color="#050709"/>
  </radialGradient>
  <linearGradient id="mint" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#81ffb6"/><stop offset="1" stop-color="#31fbb8"/>
  </linearGradient>
</defs>
<rect width="512" height="512" rx="{corner_radius}" fill="url(#glow)"/>
<g transform="translate(256 256) scale({scale}) translate({shift} 0)">
  {prompt}
  <text x="-24" y="76" font-family="Geist Mono" font-weight="800" font-size="210" fill="#f2f6f8">B</text>
  <rect x="110" y="-78" width="92" height="156" rx="8" fill="url(#mint)"/>
</g>
</svg>"""


# file name -> (pixel size, corner radius on the 512 canvas, mark scale, with prompt)
ICONS = {
    "icon-192.png": (192, 112, 1.0, True),
    "icon-512.png": (512, 112, 1.0, True),
    "icon-maskable-512.png": (512, 0, 0.8, True),
    "apple-touch-icon.png": (180, 0, 0.9, True),
    "favicon.png": (32, 112, 1.15, False),
}


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, (size, radius, scale, with_prompt) in ICONS.items():
            page = browser.new_page(viewport={"width": size, "height": size})
            page.set_content(
                f'<html><head><link rel="stylesheet" href="{FONT}">'
                "<style>html,body{margin:0;background:transparent}"
                "svg{display:block;width:100vw;height:100vh}</style></head>"
                f"<body>{mark_svg(radius, scale, with_prompt)}</body></html>",
                wait_until="networkidle",
            )
            if not page.evaluate("document.fonts.check('800 210px \"Geist Mono\"')"):
                print("Geist Mono did not load; refusing to render with a fallback font.")
                return 1
            page.screenshot(path=str(WWWROOT / name), omit_background=True)
            page.close()
            print(f"wrote {name} ({size}x{size})")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
