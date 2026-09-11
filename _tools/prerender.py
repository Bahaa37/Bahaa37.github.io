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


def home_body(cv: dict) -> str:
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

    return f"""
      <h1>{e(profile['name'])}</h1>
      <p>{e(profile['title'])}</p>
      <p>{e(cv['summary'])}</p>
      <dl>{fact_list}</dl>
      <h2>Skills</h2>{skills}
      <h2>Experience</h2>{experience}
      <h2>Selected work</h2>{case_studies}
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


def build_routes(cv: dict, base_url: str) -> list[Route]:
    profile = cv["profile"]
    name = profile["name"]

    routes = [
        Route(
            path="",
            title=f"{name} — .NET Architecture & Modernization",
            description=cv["summary"],
            body=home_body(cv),
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
APP_DIV_RE = re.compile(r'(<div id="app">)(.*?)(</div>)', re.DOTALL)


def render(route: Route, shell: str, base_url: str) -> str:
    url = route.url.format(base=base_url)
    page = shell

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

    head_additions = [f'<link rel="canonical" href="{e(url)}" />']
    if not route.indexable:
        head_additions.append('<meta name="robots" content="noindex" />')

    # Cloudflare Web Analytics: cookieless, so it needs no consent banner, and injected
    # only when a token is actually configured. Keeping it out of index.html means the
    # repo never carries a placeholder token that looks live and is not.
    if token := os.environ.get("CF_ANALYTICS_TOKEN", "").strip():
        head_additions.append(
            '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
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
            return f'{match.group(1)}{match.group(2)}\n<div class="prerendered">{route.body}</div>\n{match.group(3)}'

        page, count = APP_DIV_RE.subn(replace_app, page, count=1)
        if count == 0:
            raise SystemExit('prerender: could not find <div id="app"> in the shell.')

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
    cv = json.loads((publish / "data" / "cv.json").read_text(encoding="utf-8"))

    routes = build_routes(cv, base_url)

    for route in routes:
        page = render(route, shell, base_url)

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

    return verify(routes)


def verify(routes: list[Route]) -> int:
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

    if failures:
        print("\nFAIL  Routes are not distinguishable to a crawler:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"\nOK    {len(routes)} routes, each with its own title, description and canonical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
