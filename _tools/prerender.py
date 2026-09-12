"""Write a real, crawlable HTML page for every route.

The app is client-rendered WebAssembly, so `view-source` on the published site shows an
empty shell. Google can execute JavaScript, but WASM is heavier and not guaranteed, and
the crawlers behind ChatGPT, Perplexity and Claude largely do not execute it at all —
which is precisely the audience a CV needs to reach in 2026.

Worse, the previous approach copied `index.html` verbatim to each route, so `/cv` and
`/work/windoor-wizard-builder` served the *same* title, the same description and an
`og:url` pointing at `/`. To a crawler the site was three copies of one page.

This script replaces that copy step. For each route it writes an `index.html` carrying:

  * a title and description written for that route,
  * matching Open Graph tags with the route's own canonical URL,
  * JSON-LD describing what the route actually is, and
  * the route's real text content inside `<div id="app">`.

That last point is the one that matters most. Blazor replaces the contents of `#app`
when it boots, so markup placed there is what a non-executing crawler reads and what a
person sees before the runtime arrives — and it costs the app nothing.

Everything is derived from cv.json, so the prerendered text cannot drift from the CV.

Usage:  python _tools/prerender.py <publish-dir> [--base-url https://example.com]
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = "https://bahaa37.github.io"


@dataclass
class Route:
    """One crawlable URL and everything that distinguishes it from the others."""

    path: str  # "" for the site root, otherwise "cv", "work/slug", ...
    title: str
    description: str
    body: str = ""
    json_ld: list[dict] = field(default_factory=list)
    # Excluded from sitemap.xml and marked noindex. Used for 404.
    indexable: bool = True

    @property
    def url(self) -> str:
        return f"{{base}}/{self.path}" if self.path else "{base}/"


# --------------------------------------------------------------------------------------
# Content helpers
# --------------------------------------------------------------------------------------


def e(value: str) -> str:
    return html.escape(value or "", quote=True)


def month_name(year_month: str | None) -> str:
    """'2024-11' -> 'November 2024'. None means the role is current."""
    if not year_month:
        return "Present"
    names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    year, month = year_month.split("-")
    return f"{names[int(month) - 1]} {year}"


def period_text(period: dict) -> str:
    return f"{month_name(period.get('start'))} – {month_name(period.get('end'))}"


def bullets(items: list[str]) -> str:
    return "".join(f"<li>{e(item)}</li>" for item in items)


# --------------------------------------------------------------------------------------
# Per-route bodies
# --------------------------------------------------------------------------------------


# The static markup mirror of TestimonialCard.razor. Like the shell header, this is a
# deliberate duplication: the same quote renders here (pre-boot, crawler-visible) and
# from Blazor after boot, so a markup change must land in both places. The class names
# are styled by app.css, which both copies share.
#
# The identity rule lives with the data: every entry carries a LinkedIn or GitHub URL,
# and the name links to whichever exists — LinkedIn first.
def _testimonial_meta(testimonial: dict) -> str | None:
    parts = [
        testimonial[key]
        for key in ("role", "company")
        if testimonial.get(key)
    ]
    return ", ".join(parts) or None


def _testimonial_link(testimonial: dict) -> str | None:
    return testimonial.get("linkedIn") or testimonial.get("gitHub")


def _initials(name: str) -> str:
    parts = [part for part in name.split() if part]
    return "".join(part[0] for part in parts[:2]).upper() if parts else "?"


def testimonial_figure(testimonial: dict) -> str:
    name = testimonial["name"]
    link = _testimonial_link(testimonial)
    who = (
        f'<a href="{e(link)}" rel="noopener noreferrer">{e(name)}</a>'
        if link else e(name)
    )
    meta = _testimonial_meta(testimonial) or "Colleague"

    return (
        '<figure class="testimonial">'
        '<blockquote class="testimonial__quote">'
        f"<p>{e(testimonial['text'])}</p>"
        "</blockquote>"
        '<figcaption class="testimonial__by">'
        f'<span class="testimonial__avatar" aria-hidden="true">{e(_initials(name))}</span>'
        '<span class="testimonial__who">'
        f'<span class="testimonial__name">{who}</span>'
        f'<span class="testimonial__meta">{e(meta)}</span>'
        "</span>"
        "</figcaption>"
        "</figure>"
    )


def testimonials_body(testimonials: list[dict]) -> str:
    if not testimonials:
        return """
      <section class="band"><div class="shell">
      <p class="eyebrow">Testimonials</p>
      <h1 class="band__title">No recommendations yet</h1>
      <p class="band__lede">Recommendations from people I have worked with appear here
         as they are written. If we have worked together and you would like to add one,
         get in touch — yours will be the first.</p>
      </div></section>
    """

    figures = "".join(testimonial_figure(t) for t in testimonials)
    return f"""
      <article class="testimonials"><div class="shell">
      <header class="testimonials__head">
      <p class="eyebrow">Testimonials</p>
      <h1 class="testimonials__title">What people say</h1>
      <p class="testimonials__lede">Recommendations from colleagues and collaborators,
         each one attributed to the person who actually wrote it.</p>
      </header>
      <div class="testimonials__grid">{figures}</div>
      </div></article>
    """


def home_body(cv: dict, testimonials: list[dict] | None = None) -> str:
    profile = cv["profile"]

    skills = "".join(
        f"<section><h3>{e(group['category'])}</h3><p>{e(', '.join(group['skills']))}</p></section>"
        for group in cv.get("skillGroups", [])
    )

    experience = "".join(
        f"<article><h3>{e(entry['role'])} — {e(entry['company'])}</h3>"
        f"<p>{e(period_text(entry['period']))}"
        + (f" · {e(entry['location'])}" if entry.get("location") else "")
        + "</p>"
        f"<ul>{bullets([h['text'] for h in entry.get('highlights', [])])}</ul></article>"
        for entry in cv.get("experience", [])
    )

    case_studies = "".join(
        f"<article><h3>{e(study['title'])}</h3><p>{e(study.get('summary', ''))}</p></article>"
        for study in sorted(cv.get("caseStudies", []), key=lambda s: s.get("displayOrder", 0))
    )

    facts = [
        ("Location", profile.get("location")),
        ("Timezone", profile.get("timezone")),
        ("Availability", profile.get("availability")),
        ("Working arrangement", profile.get("relocation")),
        ("Languages", "; ".join(profile.get("languages", [])) or None),
    ]
    fact_list = "".join(
        f"<dt>{e(label)}</dt><dd>{e(value)}</dd>" for label, value in facts if value
    )

    # Mirrors the home page's testimonials band in Home.razor: three highlights, an
    # honest absence when the data file is empty.
    highlights = (testimonials or [])[:3]
    testimonials_band = ""
    if highlights:
        figures = "".join(testimonial_figure(t) for t in highlights)
        testimonials_band = (
            '<section><h2>Testimonials</h2>'
            '<p><a href="/testimonials">Read them all</a>.</p>'
            f'<div class="testimonials__grid">{figures}</div></section>'
        )

    return f"""
      <h1>{e(profile['name'])}</h1>
      <p>{e(profile['title'])}</p>
      <p>{e(cv['summary'])}</p>
      <dl>{fact_list}</dl>
      <h2>Skills</h2>{skills}
      <h2>Experience</h2>{experience}
      <h2>Selected work</h2>{case_studies}
      {testimonials_band}
      <h2>Contact</h2>
      <p><a href="mailto:{e(profile['email'])}">{e(profile['email'])}</a></p>
    """


def cv_body(cv: dict) -> str:
    profile = cv["profile"]

    education = "".join(
        f"<article><h3>{e(entry['credential'])} — {e(entry['institution'])}</h3>"
        f"<p>{e(period_text(entry['period']))}</p>"
        f"<ul>{bullets(entry.get('details', []))}</ul></article>"
        for entry in cv.get("education", [])
    )

    certifications = "".join(
        f"<li>{e(cert['name'])} — {e(cert['issuer'])}</li>"
        for cert in cv.get("certifications", [])
    )

    awards = "".join(
        f"<li>{e(award['title'])} — {e(award['issuer'])}. {e(award.get('description', ''))}</li>"
        for award in cv.get("awards", [])
    )

    experience = "".join(
        f"<article><h3>{e(entry['role'])} — {e(entry['company'])}</h3>"
        f"<p>{e(period_text(entry['period']))}</p>"
        f"<ul>{bullets([h['text'] for h in entry.get('highlights', [])])}</ul></article>"
        for entry in cv.get("experience", [])
    )

    return f"""
      <h1>{e(profile['name'])}</h1>
      <p>{e(profile['title'])}</p>
      <p>{e(profile['location'])} | {e(profile['email'])} | {e(profile.get('linkedIn', ''))}</p>
      <h2>Professional Summary</h2>
      <p>{e(cv.get('summaryExtended') or cv['summary'])}</p>
      <h2>Professional Experience</h2>{experience}
      <h2>Awards and Recognition</h2><ul>{awards}</ul>
      <h2>Education</h2>{education}
      <h2>Certifications</h2><ul>{certifications}</ul>
    """


def case_study_body(study: dict) -> str:
    return f"""
      <h1>{e(study['title'])}</h1>
      <p>{e(study.get('summary', ''))}</p>
      <h2>Problem</h2><p>{e(study.get('problem', ''))}</p>
      <h2>Approach</h2><p>{e(study.get('approach', ''))}</p>
      <h2>Outcomes</h2><ul>{bullets(study.get('outcomes', []))}</ul>
      <p>{e(', '.join(study.get('stack', [])))}</p>
    """


# --------------------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------------------


def person_schema(cv: dict, base_url: str) -> dict:
    """The block that lets a search engine — and an LLM — answer "who is this person".

    Search engines have read this for years. It now also feeds the assistants people ask
    instead of searching, which is the single highest-return item on a personal site.
    """
    profile = cv["profile"]

    same_as = [url for url in (profile.get("linkedIn"), profile.get("gitHub")) if url]

    knows_about = [skill for group in cv.get("skillGroups", []) for skill in group["skills"]]

    alumni = [
        {"@type": "EducationalOrganization", "name": entry["institution"]}
        for entry in cv.get("education", [])
    ]

    current = next(
        (entry for entry in cv.get("experience", []) if not entry["period"].get("end")),
        None,
    )

    schema = {
        "@type": "Person",
        "@id": f"{base_url}/#person",
        "name": profile["name"],
        "jobTitle": profile["title"],
        "description": cv["summary"],
        "email": f"mailto:{profile['email']}",
        "url": base_url + "/",
        "image": f"{base_url}/og-preview.png",
        "address": {"@type": "PostalAddress", "addressLocality": profile["location"]},
        "sameAs": same_as,
        # Deduplicated with order preserved: dict.fromkeys is the idiom for that.
        "knowsAbout": list(dict.fromkeys(knows_about)),
        "alumniOf": alumni,
        # schema.org wants the language, not the proficiency: "Arabic", not
        # "Arabic — native". The proficiency stays on the page and in llms.txt.
        "knowsLanguage": [
            language.split("—")[0].strip() for language in profile.get("languages", [])
        ],
        "award": [award["title"] for award in cv.get("awards", [])],
    }

    if current:
        schema["worksFor"] = {"@type": "Organization", "name": current["company"]}

    return schema


def breadcrumbs(base_url: str, trail: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": f"{base_url}/{path}".rstrip("/") if path else base_url + "/",
            }
            for index, (name, path) in enumerate(trail, start=1)
        ],
    }


# --------------------------------------------------------------------------------------
# Route table — the single source for prerendering, the sitemap and llms.txt
# --------------------------------------------------------------------------------------


def build_routes(
    cv: dict,
    base_url: str,
    testimonials: list[dict] | None = None,
) -> list[Route]:
    profile = cv["profile"]
    name = profile["name"]

    routes = [
        Route(
            path="",
            title=f"{name} — .NET Architecture & Modernization",
            description=cv["summary"],
            body=home_body(cv, testimonials),
            json_ld=[
                person_schema(cv, base_url),
                {
                    "@type": "ProfilePage",
                    "@id": f"{base_url}/#profilepage",
                    "name": f"{name} — portfolio",
                    "mainEntity": {"@id": f"{base_url}/#person"},
                },
            ],
        ),
        Route(
            path="cv",
            title=f"{name} — CV",
            description=(
                f"The printable, ATS-readable CV for {name}: {profile['title']}. "
                "Experience, skills, education, certifications and awards."
            ),
            body=cv_body(cv),
            json_ld=[breadcrumbs(base_url, [("Home", ""), ("CV", "cv")])],
        ),
    ]

    # Every case study has a page. Derived from cv.json rather than listed by hand, so
    # adding one adds its route, its sitemap entry and its llms.txt line in a single edit.
    #
    # Where a hand-written long-form write-up exists, its URL is the canonical page for
    # that work and the generated /work/{slug} route is not emitted separately — the app
    # routes the same path to the write-up component, because Blazor matches a literal
    # segment ahead of a parameter. Two URLs for one piece of work would split its
    # ranking and give a reader a choice with no right answer.
    for study in sorted(cv.get("caseStudies", []), key=lambda s: s.get("displayOrder", 0)):
        path = (study.get("writeupUrl") or f"/work/{study['slug']}").strip("/")

        # Case study titles are written as full sentences for the page heading, which is
        # too long for a <title>: a search result truncates at roughly sixty characters,
        # and the name is the part that must survive. shortTitle is the written-down
        # version of that, rather than a truncation that reads like a mistake.
        short_title = study.get("shortTitle") or study["title"]

        routes.append(
            Route(
                path=path,
                title=f"{short_title} — {name}",
                description=study.get("summary", "")[:300],
                body=case_study_body(study),
                json_ld=[
                    breadcrumbs(
                        base_url,
                        [("Home", ""), ("Selected work", ""), (study["title"], path)],
                    ),
                    {
                        "@type": "TechArticle",
                        "headline": study["title"],
                        "description": study.get("summary", ""),
                        "author": {"@id": f"{base_url}/#person"},
                    },
                ],
            )
        )

    # One page for every recommendation. Derived from the data file like the case
    # studies, so publishing a testimonial publishes its place here with no new code —
    # and an empty file still gets a page that says so honestly.
    entries = sorted(testimonials or [], key=lambda t: t.get("displayOrder", 0))
    routes.append(
        Route(
            path="testimonials",
            title=f"Testimonials — {name}",
            description=(
                f"Recommendations for {name} from colleagues and collaborators, "
                "each attributed to the person who wrote it."
            ),
            body=testimonials_body(entries),
            json_ld=[breadcrumbs(base_url, [("Home", ""), ("Testimonials", "testimonials")])],
        )
    )

    routes.append(
        Route(
            path="404",
            title=f"Page not found — {name}",
            description="That page does not exist on this site.",
            body=f"<h1>Page not found</h1><p><a href=\"/\">Go to {e(name)}'s portfolio</a>.</p>",
            indexable=False,
        )
    )

    return routes


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

# The shell's own tags, which every route replaces with its own.
TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
DESCRIPTION_RE = re.compile(r'<meta\s+name="description"[^>]*>')
OG_TITLE_RE = re.compile(r'<meta\s+property="og:title"[^>]*>')
OG_DESCRIPTION_RE = re.compile(r'<meta\s+property="og:description"[^>]*>')
OG_URL_RE = re.compile(r'<meta\s+property="og:url"[^>]*>')
# The shell's #app contains the loading spinner and a loading-text div before its own
# closing tag. A non-greedy `.*?</div>` here would stop at the loading-text div's
# closing tag instead of #app's, nesting the prerendered content INSIDE the loading
# indicator — which `#app:has(.prerendered) .loading-progress-text { display: none }`
# then hides. Every route would ship its content pre-hidden: a blank page until
# WebAssembly boots, which is precisely the blank second this script exists to remove
# and precisely the invisible-content class of bug this repository keeps a rule about.
# So the match runs to #app's own closing tag, and render() re-checks the result.
APP_DIV_RE = re.compile(
    r'(<div id="app">)(.*?<div class="loading-progress-text"></div>)(\s*</div>)',
    re.DOTALL,
)

# The nesting defect the regex above once produced, detectable in the output text:
# the prerendered block as the first thing inside the loading-text div.
BAD_NESTING_RE = re.compile(
    r'<div class="loading-progress-text">[^<]*<div class="prerendered"'
)


# Assets referenced from index.html by bare path. The framework's own script already
# carries a fingerprint; nothing else did, which is the bug this fixes.
VERSIONED_ASSETS = [
    "css/app.css",
    "css/print.css",
    "Cv.Web.styles.css",
    "favicon.png",
    "manifest.webmanifest",
    "js/boot.js",
    "service-worker.js",
]


# The nav, as markup, exactly as MainLayout.razor renders it. The prerendered shell
# must carry this header because booting the runtime is deferred (wwwroot/js/boot.js):
# until WebAssembly arrives — possibly never, on a data-saver connection — these links
# and the theme button are the only site chrome a reader has.
#
# This is the one deliberate duplication between C# and this script. When the layout's
# nav or theme button changes, change them here too; both sides carry comments pointing
# at the other. The classes (site-header, site-nav, theme-toggle) are styled by app.css,
# which is inlined into the same pages, so the chrome looks identical before and after
# boot — and Blazor replaces the whole block when it takes over.
NAV_LINKS = (
    ("/#skills", "Skills"),
    ("/#timeline", "Experience"),
    ("/#work", "Selected work"),
    ("/#credentials", "Credentials"),
    ("/testimonials", "Testimonials"),
    ("/cv", "CV"),
)


def static_shell_header(cv: dict) -> str:
    profile_name = cv["profile"]["name"]
    links = "".join(f'<a href="{href}">{e(label)}</a>' for href, label in NAV_LINKS)
    return (
        '<header class="site-header">'
        '<div class="shell site-header__inner">'
        f'<a class="site-header__name" href="/">{e(profile_name)}</a>'
        f'<nav class="site-nav">{links}</nav>'
        '<button type="button" class="theme-toggle" data-static-theme-toggle '
        'aria-label="Switch theme" title="Switch theme">'
        '<span aria-hidden="true">☾</span></button>'
        "</div></header>"
    )


def asset_versions(publish: Path) -> dict[str, str]:
    """Map each versionable asset to a short hash of its own contents.

    Hashing the content rather than stamping the build is the point: an asset that did
    not change keeps its URL and stays cached, so a deploy only invalidates what it
    actually touched.
    """
    versions: dict[str, str] = {}

    for asset in VERSIONED_ASSETS:
        path = publish / asset
        if path.exists():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
            versions[asset] = digest

    return versions


# The two heaviest files in the boot payload, by far: the WebAssembly runtime and the
# base class library. Together they are most of what a cold visit downloads. The Blazor
# loader only requests them after it has been discovered, fetched, parsed and run —
# measured at well over a second after navigation on the published site — and every
# millisecond before that is a millisecond the connection sits idle. Preloading them
# from the document starts the transfer as soon as the HTML is parsed.
BOOT_PRELOAD_PREFIXES = ("dotnet.native.", "System.Private.CoreLib.")


def boot_preloads(publish: Path) -> list[str]:
    """Fingerprinted URLs of the heaviest framework files, for <link rel=preload>."""
    framework = publish / "_framework"
    if not framework.is_dir():
        return []

    preloads = []

    for prefix in BOOT_PRELOAD_PREFIXES:
        matches = sorted(framework.glob(f"{prefix}*.wasm"))
        if matches:
            # `crossorigin` must match how the loader fetches (CORS mode), or the
            # preload is not reused and the file downloads twice.
            name = matches[0].name
            preloads.append(f'<link rel="preload" href="_framework/{name}" as="fetch" crossorigin />')

    return preloads


def version_asset_urls(page: str, versions: dict[str, str]) -> str:
    """Append ?v=<hash> to every versioned asset reference in the page.

    Without this a returning browser runs new HTML and new WebAssembly against a cached
    stylesheet and a cached cv.json — which is not a cosmetic problem on a document whose
    entire purpose is being current. It showed up as a theme button rendering unstyled
    and a footer displaying a job title that had been replaced.
    """
    for asset, digest in versions.items():
        # Match the asset only as a complete href/src value, so "css/app.css" cannot also
        # rewrite a longer path that happens to start with it.
        page = re.sub(
            rf'((?:href|src)=")({re.escape(asset)})(")',
            rf"\g<1>\g<2>?v={digest}\g<3>",
            page,
        )

    return page


# --------------------------------------------------------------------------------------
# First-paint CSS
#
# The site's own bar is that content is visible in under a second on a cold visit. A
# render-blocking stylesheet is the last thing standing between the HTML arriving and
# the first pixel, because the browser paints nothing until CSS it has been told is
# render-blocking has been fetched — one more same-origin round trip on a fast
# connection, several hundred milliseconds on a bad one.
#
# The split below follows what each stylesheet is actually needed for:
#
#   * app.css styles the prerendered content inside #app, the loading indicator and
#     the long-form layout — everything a person sees before WebAssembly boots. It is
#     inlined into every page, so first paint needs no round trip at all. Gzip merges
#     most of the cost: the bytes were being downloaded anyway, just as a second file.
#   * Cv.Web.styles.css is Blazor's CSS-isolation bundle — component-owned looks that
#     cannot apply until components exist, i.e. until the runtime has booted, seconds
#     after first paint. It loads asynchronously (the same media="print" swap used for
#     the Google Fonts stylesheet) instead of being inlined, which would have made
#     every page carry its ~15 KB gz for nothing a first-paint reader sees.
#   * print.css is only consulted when printing, so it is marked media="print" and
#     never blocks a screen render.
#
# All three are derived from the published output at build time, so they cannot drift
# from what the app itself loads.
# --------------------------------------------------------------------------------------

CRITICAL_CSS_LINK_RE = re.compile(r'<link rel="stylesheet" href="css/app\.css[^"]*" />')
PRINT_CSS_LINK_RE = re.compile(r'<link rel="stylesheet" href="(css/print\.css[^"]*)" />')
COMPONENT_CSS_LINK_RE = re.compile(r'<link href="(Cv\.Web\.styles\.css[^"]*)" rel="stylesheet" />')


def inline_first_paint_css(page: str, app_css: str) -> str:
    """Apply the three-way stylesheet split to one rendered page."""
    # A "</style" inside the CSS would terminate the inline block early and mangle the
    # page. Verified absent today; this makes the failure loud if that ever changes.
    if "</" in app_css:
        raise SystemExit("prerender: app.css contains '</'; it cannot be inlined safely.")

    page, count = CRITICAL_CSS_LINK_RE.subn(
        lambda _: f"<style>\n{app_css}</style>", page, count=1
    )
    if count == 0:
        raise SystemExit('prerender: could not find the css/app.css link to inline.')

    page, count = PRINT_CSS_LINK_RE.subn(
        lambda m: f'<link rel="stylesheet" href="{m.group(1)}" media="print" />', page, count=1
    )
    if count == 0:
        raise SystemExit('prerender: could not find the css/print.css link to defer.')

    def defer_component_css(match: re.Match[str]) -> str:
        href = match.group(1)
        return (
            f'<link rel="preload" href="{href}" as="style" />\n'
            f'    <link rel="stylesheet" href="{href}" media="print" onload="this.media=\'all\'" />\n'
            f'    <noscript><link rel="stylesheet" href="{href}" /></noscript>'
        )

    page, count = COMPONENT_CSS_LINK_RE.subn(defer_component_css, page, count=1)
    if count == 0:
        raise SystemExit('prerender: could not find the Cv.Web.styles.css link to defer.')

    return page


def render(
    route: Route,
    shell: str,
    base_url: str,
    versions: dict[str, str] | None = None,
    preloads: list[str] | None = None,
    app_css: str = "",
    shell_header: str = "",
    sw_registration: str = "",
) -> str:
    url = route.url.format(base=base_url)
    page = version_asset_urls(shell, versions or {})
    page = inline_first_paint_css(page, app_css)

    page = TITLE_RE.sub(lambda _: f"<title>{e(route.title)}</title>", page, count=1)
    page = DESCRIPTION_RE.sub(
        lambda _: f'<meta name="description" content="{e(route.description)}" />', page, count=1
    )
    page = OG_TITLE_RE.sub(
        lambda _: f'<meta property="og:title" content="{e(route.title)}" />', page, count=1
    )
    page = OG_DESCRIPTION_RE.sub(
        lambda _: f'<meta property="og:description" content="{e(route.description)}" />',
        page,
        count=1,
    )
    page = OG_URL_RE.sub(lambda _: f'<meta property="og:url" content="{e(url)}" />', page, count=1)

    head_additions = (preloads or []) + [f'<link rel="canonical" href="{e(url)}" />']
    if not route.indexable:
        head_additions.append('<meta name="robots" content="noindex" />')

    # Cloudflare Web Analytics: cookieless, so no consent banner is required.
    #
    # The token is not a credential — Cloudflare serves it in the page source of every
    # site that uses it — so it lives in the workflow rather than in a secret. It is read
    # from the environment anyway so that CI builds, which set nothing, never report
    # traffic from a test run as if it were a real visit.
    #
    # The tag matches the snippet Cloudflare issues, type="module" included.
    if token := os.environ.get("CF_ANALYTICS_TOKEN", "").strip():
        head_additions.append(
            "<!-- Cloudflare Web Analytics -->"
            '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
            f"data-cf-beacon='{{\"token\": \"{e(token)}\"}}'></script>"
        )

    if route.json_ld:
        graph = {"@context": "https://schema.org", "@graph": route.json_ld}
        # No HTML escaping inside a script block; guard only the sequence that could
        # close it early.
        payload = json.dumps(graph, ensure_ascii=False, indent=2).replace("</", "<\\/")
        head_additions.append(f'<script type="application/ld+json">{payload}</script>')

    page = page.replace("</head>", "    " + "\n    ".join(head_additions) + "\n</head>", 1)

    # Blazor clears #app on boot, so this content is what a non-executing crawler reads
    # and what a person sees before the runtime arrives. The loading indicator already
    # in the shell is kept ahead of it.
    if route.body:
        def replace_app(match: re.Match[str]) -> str:
            return (
                f"{match.group(1)}{match.group(2)}"
                f"{shell_header}"
                f'\n<div class="prerendered">{route.body}</div>'
                f"{match.group(3)}"
            )

        page, count = APP_DIV_RE.subn(replace_app, page, count=1)
        if count == 0:
            raise SystemExit('prerender: could not find <div id="app"> in the shell.')
        if BAD_NESTING_RE.search(page):
            raise SystemExit(
                "prerender: the prerendered block was nested inside the loading "
                "indicator, which CSS then hides. The #app regex and the shell have "
                "drifted apart; real readers would see a blank page until boot."
            )

    if sw_registration:
        page = page.replace("</body>", f"{sw_registration}</body>", 1)

    return page


def write_sitemap(routes: list[Route], base_url: str, out: Path) -> None:
    today = date.today().isoformat()
    entries = "\n".join(
        f"  <url><loc>{e(route.url.format(base=base_url))}</loc>"
        f"<lastmod>{today}</lastmod></url>"
        for route in routes
        if route.indexable
    )
    out.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n",
        encoding="utf-8",
    )


def write_robots(base_url: str, out: Path) -> None:
    out.write_text(
        "# Everything here is meant to be found — it is a CV.\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {base_url}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_llms_txt(cv: dict, routes: list[Route], base_url: str, out: Path) -> None:
    """A plain-text brief for the assistants people now ask instead of searching."""
    profile = cv["profile"]

    pages = "\n".join(
        f"- [{route.title}]({route.url.format(base=base_url)}): {route.description}"
        for route in routes
        if route.indexable
    )

    # The timezone value carries its own parentheses — "EET (UTC+2)" — so it is joined
    # with a dash rather than wrapped again.
    location = profile["location"]
    if profile.get("timezone"):
        location += f" — {profile['timezone']}"

    contact = [
        f"- Location: {location}",
        f"- Email: {profile['email']}",
    ]
    for label, key in (("LinkedIn", "linkedIn"), ("GitHub", "gitHub")):
        if profile.get(key):
            contact.append(f"- {label}: {profile[key]}")
    for label, key in (("Availability", "availability"), ("Working arrangement", "relocation")):
        if profile.get(key):
            contact.append(f"- {label}: {profile[key]}")
    if profile.get("languages"):
        contact.append(f"- Languages: {'; '.join(profile['languages'])}")

    out.write_text(
        f"# {profile['name']}\n\n"
        f"> {profile['title']}. {cv['summary']}\n\n"
        "## Pages\n\n"
        f"{pages}\n\n"
        "## Contact\n\n"
        + "\n".join(contact)
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("publish_dir", type=Path, help="The published wwwroot to rewrite in place.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    publish = args.publish_dir

    shell_path = publish / "index.html"
    if not shell_path.exists():
        print(f"FAIL  No index.html in {publish}", file=sys.stderr)
        return 1

    shell = shell_path.read_text(encoding="utf-8")

    # This script both reads publish/index.html as the shell and writes the home route
    # back over it. Run twice without a fresh publish in between, it would inject its
    # canonical links, boot preloads and prerendered body into an already-processed
    # page — every check would still pass while the home route silently carried
    # duplicated markup. Refuse instead.
    if '<link rel="canonical"' in shell or 'class="prerendered"' in shell:
        print(
            "FAIL  The shell is already prerendered — most likely a previous run of "
            "this script, whose output MSBuild's incremental publish then declined to "
            "overwrite. Restore a clean shell (delete publish/wwwroot/index.html, or "
            "publish with --no-incremental) and run this script again.",
            file=sys.stderr,
        )
        return 1

    cv = json.loads((publish / "data" / "cv.json").read_text(encoding="utf-8"))

    # Testimonials are optional the same way: a build must not fail because a
    # supplementary document is absent or empty.
    testimonials_path = publish / "data" / "testimonials.json"
    testimonials = (
        json.loads(testimonials_path.read_text(encoding="utf-8")).get("testimonials", [])
        if testimonials_path.exists()
        else []
    )

    versions = asset_versions(publish)
    preloads = boot_preloads(publish)

    # The stylesheet first paint depends on, read once and inlined into every route.
    # Missing is fatal in the spirit of the PDF check below: a page without its CSS
    # would still look fine to every automated check while rendering unstyled.
    app_css_path = publish / "css" / "app.css"
    if not app_css_path.exists():
        print(f"FAIL  No css/app.css in {publish}", file=sys.stderr)
        return 1
    app_css = app_css_path.read_text(encoding="utf-8")

    # Stamp the service worker before asset_versions hashes it, so the ?v= version
    # covers the worker's source and the exact framework file set of this build. Any
    # change to either produces a new version URL — the browser refetches and replaces
    # the worker, and its activate step deletes the previous version's cache.
    sw_registration = ""
    sw_path = publish / "service-worker.js"
    if sw_path.exists():
        framework_names = sorted(p.name for p in (publish / "_framework").glob("*"))
        stamp_source = sw_path.read_text(encoding="utf-8") + "\n" + "\n".join(framework_names)
        stamp = hashlib.sha256(stamp_source.encode("utf-8")).hexdigest()[:10]
        sw_path.write_text(
            sw_path.read_text(encoding="utf-8").replace("__SW_VERSION__", stamp),
            encoding="utf-8",
        )
        versions = asset_versions(publish)

        sw_registration = (
            "<script>if('serviceWorker' in navigator){"
            "addEventListener('load',function(){"
            "navigator.serviceWorker.register("
            f"'service-worker.js?v={versions['service-worker.js']}');"
            "});}</script>"
        )

    # Testimonials are optional the same way: a build must not fail because a
    # supplementary document is absent or empty.
    testimonials_path = publish / "data" / "testimonials.json"
    testimonials = (
        json.loads(testimonials_path.read_text(encoding="utf-8")).get("testimonials", [])
        if testimonials_path.exists()
        else []
    )

    shell_header = static_shell_header(cv)
    routes = build_routes(cv, base_url, testimonials)

    for route in routes:
        page = render(route, shell, base_url, versions, preloads, app_css, shell_header, sw_registration)

        if route.path == "":
            target = publish / "index.html"
        elif route.path == "404":
            # GitHub Pages serves this for any unknown path; the client router then
            # picks the route up for a person, while a bot gets a real 404 page.
            target = publish / "404.html"
        else:
            target = publish / route.path / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(page, encoding="utf-8")
        print(f"  {target.relative_to(publish)}  ({route.title})")

    write_sitemap(routes, base_url, publish / "sitemap.xml")
    write_robots(base_url, publish / "robots.txt")
    write_llms_txt(cv, routes, base_url, publish / "llms.txt")
    print("  sitemap.xml, robots.txt, llms.txt")

    if versions:
        print("  versioned: " + ", ".join(f"{a}?v={v}" for a, v in versions.items()))

    return verify(routes, publish)


CV_PDF_NAME = "Bahaa-Aldeen-Mohamed-CV.pdf"

# A one-page CV with a text layer does not come out under ~20 KB. Anything smaller is a
# renderer that produced a blank rather than a document.
MIN_PDF_BYTES = 20_000


def verify(routes: list[Route], publish: Path) -> int:
    """Fail the build on the defects that are invisible from the rendered site."""
    failures = verify_routes_are_distinct(routes) + verify_downloads(publish)

    if failures:
        print("\nFAIL  Publish-time checks did not pass:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"\nOK    {len(routes)} routes, each with its own title, description and canonical.")
    return 0


def verify_downloads(publish: Path) -> list[str]:
    """The CV download is linked from two pages; nothing else checks it is really there.

    A missing file is served by GitHub Pages as the 404 page, so the link does not break
    visibly — it just quietly stops being a CV.
    """
    pdf = publish / CV_PDF_NAME

    if not pdf.exists():
        return [f"{CV_PDF_NAME} is not in the published output, but /cv and / both link to it."]

    size = pdf.stat().st_size
    if size < MIN_PDF_BYTES:
        return [f"{CV_PDF_NAME} is only {size:,} bytes, which is too small to be the real CV."]

    return []


def verify_routes_are_distinct(routes: list[Route]) -> list[str]:
    """Fail the build if two routes would look like the same page to a crawler.

    This is the defect this script exists to fix, and it is invisible from the rendered
    site — every page looks right in a browser while the metadata is identical. Checking
    it here is the only place it gets caught.
    """
    failures: list[str] = []

    for field_name in ("title", "description"):
        seen: dict[str, str] = {}
        for route in routes:
            value = getattr(route, field_name)
            if value in seen:
                failures.append(
                    f"{field_name}: /{route.path} and /{seen[value]} share {value!r}"
                )
            seen[value] = route.path

    for route in routes:
        if len(route.title) > 70:
            failures.append(f"title: /{route.path} is {len(route.title)} chars; search results cut at ~60")
        if not route.description.strip():
            failures.append(f"description: /{route.path} is empty")

    return failures


if __name__ == "__main__":
    raise SystemExit(main())
