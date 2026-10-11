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
from urllib.parse import urlparse

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
    # Full-bleed markup injected ahead of the measured .prerendered document —
    # the home route's hero and marquee, which must escape the 46rem column.
    pre_body: str = ""
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
# and the source link points at whichever exists — LinkedIn first, labelled by its own
# host so it can never claim more than the URL does.
def _testimonial_meta(testimonial: dict) -> str | None:
    parts = [
        testimonial[key]
        for key in ("role", "company")
        if testimonial.get(key)
    ]
    return ", ".join(parts) or None


def _testimonial_link(testimonial: dict) -> str | None:
    return testimonial.get("linkedIn") or testimonial.get("gitHub")


def _host(link: str) -> str:
    """The link's own host, minus www — the label claims exactly what the URL is."""
    host = urlparse(link).netloc or link
    return host[4:] if host.startswith("www.") else host


def testimonial_figure(testimonial: dict) -> str:
    name = testimonial["name"]
    link = _testimonial_link(testimonial)
    meta = _testimonial_meta(testimonial)
    source = (
        f'<a class="testimonial__source" href="{e(link)}" rel="noopener noreferrer">'
        f"{e(_host(link))}</a>"
        if link else ""
    )
    by_meta = f'<span class="testimonial__meta">{e(meta)}</span>' if meta else ""

    return (
        '<figure class="hl-card testimonial">'
        '<blockquote class="testimonial__quote">'
        f'<p class="hl-lead">{e(testimonial["text"])}</p>'
        "</blockquote>"
        '<figcaption class="testimonial__by">'
        f'<span class="testimonial__name">{e(name)}</span>'
        f"{by_meta}"
        f"{source}"
        "</figcaption>"
        "</figure>"
    )


def testimonials_body(testimonials: list[dict], cv: dict) -> str:
    if not testimonials:
        email = cv["profile"]["email"]
        # The empty state mirrors TestimonialsPage.razor: the honest words, plus
        # the data file as a console — one line, an empty array. Change both.
        return f"""
      <section class="sheet"><div class="shell">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>
        <span aria-hidden="true">/</span><a href="/testimonials">Testimonials</a></nav>
      <h1 class="sheet__title">No recommendations yet</h1>
      <p class="sheet__lede">Recommendations from people I have worked with appear here
         as they are written. If we have worked together and you would like to add one,
         <a href="mailto:{e(email)}">get in touch</a> — yours will be the first.</p>
      <div class="hl-window testimonials__empty">
      <div class="hl-window__bar">
      <div class="hl-window__dots"><i></i><i></i><i></i></div>
      <span class="hl-window__title">testimonials.json</span></div>
      <div class="hl-window__log testimonials__empty-log">
      <p class="hl-window__line hl-window__line--cmd">testimonials.json → []</p>
      </div></div>
      </div></section>
    """

    figures = "".join(testimonial_figure(t) for t in testimonials)
    return f"""
      <article class="testimonials"><div class="shell">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>
        <span aria-hidden="true">/</span><a href="/testimonials">Testimonials</a></nav>
      <header class="testimonials__head">
      <h1 class="hl-h2 testimonials__title"><span class="hl-dim">What people</span> say</h1>
      <p class="hl-lead testimonials__lede">Recommendations from colleagues and collaborators,
         each one attributed to the person who actually wrote it.</p>
      </header>
      <div class="testimonials__grid">{figures}</div>
      </div></article>
    """


# The static mirror of Hero.razor's console and figures. Like the shell header,
# this is deliberate duplication: the same content renders here (pre-boot,
# crawler-visible, no-JS) and from Blazor after boot, so a markup change must land
# in both places. The four console lines and the two derived figures follow the
# same derivation Hero.razor carries (its anchor phrases are pinned by
# RealCvDocumentTests), read from the same cv.json.


def _ordered_studies(cv: dict) -> list[dict]:
    return sorted(cv.get("caseStudies", []), key=lambda s: s.get("displayOrder", 0))


def _study_url(study: dict) -> str:
    return study.get("writeupUrl") or f"/work/{study['slug']}"


def _first_sentence(summary: str) -> str:
    """The situation in one line: everything up to the first period, kept."""
    cut = summary.find(". ")
    return summary[: cut + 1] if cut >= 0 else summary


def _first_containing(values: list[str], needle: str) -> str:
    return next((value for value in values if needle.lower() in value.lower()), "")


def _number_after(text: str, anchor: str) -> int:
    match = re.search(re.escape(anchor) + r"\s*(\d+)", text, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def _number_before(text: str, anchor: str) -> int:
    match = re.search(r"(\d+)\s*" + re.escape(anchor), text, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def _console_run_lines(study: dict) -> str:
    """One console run: command, situation, stack trail, outcome plus the link.

    The static mirror of CaseStudyConsole.RunLines (src/Cv.Web/Components/Showcase/
    CaseStudyConsole.cs). Change both together.
    """
    info = " → ".join(e(tech) for tech in (study.get("stack") or [])[:4])
    outcome = e((study.get("outcomes") or [""])[0])
    return (
        f'<p class="hl-window__line hl-window__line--cmd">open {e(study["slug"])}</p>\n'
        f'<p class="hl-window__line hl-window__line--muted">{e(_first_sentence(study.get("summary", "")))}</p>\n'
        f'<p class="hl-window__line hl-window__line--info">{info}</p>\n'
        f'<p class="hl-window__result">◆ {outcome} '
        f'<a href="{e(_study_url(study))}">Read the case study →</a></p>'
    )


def _hero_figures(cv: dict) -> list[tuple[str, int]]:
    studies = _ordered_studies(cv)
    summaries = [s.get("summary", "") for s in studies]
    outcomes = [o for s in studies for o in s.get("outcomes", [])]

    markets = _number_after(_first_containing(summaries, "9 countries"), "across")
    gateways = _number_before(_first_containing(outcomes, "payment gateways"), "payment gateways")
    upgrade_days = _number_after(_first_containing(outcomes, "5-7 working days"), "maximum of")
    decision_records = _number_before(
        _first_containing(outcomes, "architecture decision records"),
        "architecture decision records",
    )
    awards = len(cv.get("awards", []))

    return [
        (f"countries on one payment API, {gateways} gateways behind it", markets),
        ("days per upgrade cycle, down from 5–7, after the AI-guided workflow", upgrade_days),
        ("architecture decision records behind my multi-tenant SaaS", decision_records),
        ("company awards, for that workflow and for AI training", awards),
    ]


def _figure_cell(label: str, value: int) -> str:
    return (
        '<div class="hl-cell hero__fact">'
        f'<dt class="hero__fact-label">{e(label)}</dt>'
        f'<dd class="hero__fact-value"><span data-count-to="{value}" aria-hidden="true">{value}</span>'
        f'<span class="visually-hidden">{value}</span></dd>'
        "</div>"
    )


def _hero_console(studies: list[dict]) -> str:
    if not studies:
        return ""

    # Chip labels are the studies' slugs (Hero.razor's grammar): the command the
    # console's own "open {slug}" line runs. The human title rides in the attributes.
    chips = "".join(
        f'<a class="hl-chip" href="{e(_study_url(s))}" data-hl-run="{e(s["slug"])}"'
        f' title="{e(s.get("shortTitle") or s["title"])}" aria-label="Run: {e(s.get("shortTitle") or s["title"])}">'
        f'<span class="hl-chip__label">{e(s["slug"])}</span></a>'
        for s in studies
    )
    templates = "".join(
        f'<template data-hl-run-id="{e(s["slug"])}">{_console_run_lines(s)}</template>'
        for s in studies
    )
    # The static log ships the first study's run COMPLETED, so the no-JS page shows
    # a finished run; hairline.js (when it runs) marks chip #1 and takes over.
    return (
        '<div class="hl-window hl-enter hl-enter--scene hero__console" '
        'style="--hl-enter-delay:350ms" data-hl-console data-hl-interval="6000">'
        '<div class="hl-window__bar">'
        '<div class="hl-window__dots"><i></i><i></i><i></i></div>'
        '<span class="hl-window__title">bahaa · case-studies.run</span></div>'
        f'<div class="hl-window__log" aria-live="off">{_console_run_lines(studies[0])}</div>'
        '<div class="hl-window__status">'
        '<span class="hl-dot" aria-hidden="true"></span><span>Tap a study to run it</span></div>'
        f'<div class="hl-window__chips">{chips}</div>'
        f"{templates}</div>"
    )


def _tech_marquee(studies: list[dict]) -> str:
    union: list[str] = []
    for study in studies:
        for tech in study.get("stack") or []:
            if tech not in union:
                union.append(tech)

    items = "".join(f'<li class="tech-marquee__item">{e(tech)}</li>' for tech in union)
    return (
        '<div class="hl-marquee tech-marquee" data-hl-marquee data-hl-speed="40" '
        'aria-label="Technologies used across the case studies">'
        f'<ul class="hl-marquee__track">{items}</ul></div>'
    )


# --------------------------------------------------------------------------------------
# The skills tabs, mirrored
# --------------------------------------------------------------------------------------
# The static markup mirror of SkillMatrix.razor: the kit's autoplaying tabs, built from
# the same evidence SkillEvidence.cs computes for the booted page. The matcher below is
# a line-for-line port of that C# (word-boundary text match, tag containment, the alias
# table) — CHANGE BOTH. A drift shows different evidence in the static copy than after
# boot, which is exactly the kind of silent divergence this file exists to prevent.
#
# Why the tabs are mirrored at all: the kit's engine (hairline.js) runs without Blazor,
# so a data-saver or 2G visitor who never downloads the runtime still gets the whole
# section — tab strip, autoplay, ring. Without script, every panel renders stacked and
# the whole matrix reads top to bottom.

_SKILL_ALIASES: dict[str, list[str]] = {
    "ASP.NET MVC": ["MVC"],
    "Entity Framework Core": ["Entity Framework"],
    "AI-guided development workflows": ["AI skills"],
    "Autonomous agent development": ["autonomous"],
    "Project templating & rule authoring": ["project template"],
    "Workflow Orchestration (Temporal.io)": ["Temporal"],
    "Solution architecture documents": ["solution architecture documentation"],
    "Microsoft Copilot Studio": ["Copilot Studio"],
    "Microsoft Azure": ["Azure"],
    "Mermaid diagramming": ["Mermaid"],
    "Payment gateway integration": ["payment"],
    "AI training & curriculum design": ["AI training"],
    "API documentation": ["API endpoints"],
}

_LEAD_CATEGORIES = ["Architecture & Patterns", "Cloud, Delivery & AI Engineering"]


def _contains_word(text: str, term: str) -> bool:
    """Substring match with letter/digit guards, so 'Git' never hits 'digital'."""
    low, tlow = text.lower(), term.lower()
    idx = low.find(tlow)
    while idx >= 0:
        before_ok = idx == 0 or not low[idx - 1].isalnum()
        after = idx + len(tlow)
        after_ok = after >= len(low) or not low[after].isalnum()
        if before_ok and after_ok:
            return True
        idx = low.find(tlow, idx + 1)
    return False


def _mentions(highlight: dict, skill: str) -> bool:
    text = highlight.get("text") or ""
    tags = highlight.get("tags") or []
    if _contains_word(text, skill):
        return True
    if any(skill.lower() in (tag or "").lower() for tag in tags):
        return True
    for alias in _SKILL_ALIASES.get(skill, []):
        if _contains_word(text, alias):
            return True
        if any(alias.lower() in (tag or "").lower() for tag in tags):
            return True
    return False


def _employers_using(skill: str, experience: list[dict]) -> list[str]:
    """Distinct employers whose record mentions the skill, in experience order."""
    seen: list[str] = []
    for entry in experience:
        if any(_mentions(h, skill) for h in entry.get("highlights", [])):
            if entry["company"].lower() not in [c.lower() for c in seen]:
                seen.append(entry["company"])
    return seen


def _slugify(category: str) -> str:
    slug = "".join(c if c.isalnum() else "-" for c in category.lower())
    return slug.strip("-")


def _evidence(used_at: list[str]) -> str:
    """'First employer +N', the compact form the booted rows carry."""
    return f"{used_at[0]} +{len(used_at) - 1}" if len(used_at) > 1 else used_at[0]


def _skills_tabs(cv: dict) -> str:
    groups = list(cv.get("skillGroups", []))
    experience = cv.get("experience", [])
    ordered = (
        [g for g in groups if g["category"] in _LEAD_CATEGORIES]
        + [g for g in groups if g["category"] not in _LEAD_CATEGORIES]
    )

    def panel(group: dict) -> str:
        slug = _slugify(group["category"])
        cited: list[tuple[str, list[str]]] = []
        listed: list[str] = []
        for skill in group.get("skills", []):
            used_at = _employers_using(skill, experience)
            cited.append((skill, used_at)) if used_at else listed.append(skill)

        # The cited-row arrow svg mirrors SkillMatrix.razor's (the dock icons'
        # stroke language); the evidence window's cell mirrors its wrapper.
        arrow = (
            '<span class="skills-row__arrow" aria-hidden="true">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span>'
        )
        rows = "".join(
            f'<li class="skills-row" title="{e(" · ".join(used_at))}">'
            f"{arrow}"
            f'<span class="skills-row__name">{e(skill)}</span>'
            f'<span class="skills-row__where">{e(_evidence(used_at))}</span>'
            f'<span class="visually-hidden">, used at {e(", ".join(used_at))}</span>'
            "</li>"
            for skill, used_at in cited
        )
        also = (
            f'<p class="skills-also">{e(" · ".join(listed))}</p>' if listed else ""
        )

        counts: list[list] = []  # [employer, count], first-seen order
        for _, used_at in cited:
            for employer in used_at:
                for pair in counts:
                    if pair[0].lower() == employer.lower():
                        pair[1] += 1
                        break
                else:
                    counts.append([employer, 1])

        window = ""
        if cited:
            lines = "".join(
                f'<p class="hl-window__line hl-window__line--muted">'
                f"{e(employer)} · {count}</p>"
                for employer, count in counts
            )
            window = (
                '<div class="skills-panel__evidence">'
                '<span class="hl-glow skills-panel__glow" aria-hidden="true"></span>'
                '<div class="hl-window skills-panel__window">'
                '<div class="hl-window__bar">'
                '<div class="hl-window__dots"><i></i><i></i><i></i></div>'
                f'<span class="hl-window__title">evidence · {e(slug)}.log</span></div>'
                '<div class="hl-window__log skills-window__log">'
                f"{lines}"
                f'<p class="hl-window__result">◆ {len(cited)} skills cited '
                f"across {len(counts)} employers</p>"
                "</div></div></div>"
            )

        cited_rows = f'<ul class="skills-rows">{rows}</ul>' if rows else ""

        return (
            f'<section class="hl-tabs__panel" data-hl-panel="{e(slug)}">'
            '<div class="skills-panel__copy">'
            f'<h3 class="hl-h3">{e(group["category"])}</h3>'
            f"{cited_rows}{also}</div>{window}</section>"
        )

    tabs = "".join(
        f'<button class="hl-tabs__tab" type="button" data-hl-tab="{_slugify(g["category"])}">'
        f'{e(g["category"])}</button>'
        for g in ordered
    )
    panels = "".join(panel(g) for g in ordered)

    return (
        '<section class="section" id="skills">'
        '<div class="hl-container section__frame">'
        '<header class="section__head" data-hl-reveal>'
        '<h2 class="hl-h2"><span class="hl-dim">Skills,</span> with the work that backs them</h2>'
        '<p class="hl-lead">Anyone can list a technology. Where a skill shows up in the '
        "achievement record, the employers are named beside it.</p>"
        "</header>"
        '<div class="hl-tabs skills-tabs" data-hl-tabs data-hl-autoplay="7000">'
        f'<div class="hl-tabs__list" hidden>{tabs}</div>'
        f"{panels}"
        '<div class="hl-tabs__controls" hidden>'
        '<div class="hl-ring">'
        '<svg viewBox="0 0 40 40" aria-hidden="true">'
        '<circle class="hl-ring__track" cx="20" cy="20" r="17"></circle>'
        '<circle class="hl-ring__bar" cx="20" cy="20" r="17" pathLength="100"></circle>'
        "</svg>"
        '<button class="hl-ring__btn" type="button" aria-label="Pause autoplay">'
        '<svg class="hl-ring__icon hl-ring__icon--pause" viewBox="0 0 12 12" aria-hidden="true">'
        '<rect x="2" y="1.5" width="3" height="9" rx="1" fill="currentColor"/>'
        '<rect x="7" y="1.5" width="3" height="9" rx="1" fill="currentColor"/></svg>'
        '<svg class="hl-ring__icon hl-ring__icon--play" viewBox="0 0 12 12" aria-hidden="true" '
        'hidden><path d="M3.5 1.5v9l7-4.5z" fill="currentColor"/></svg>'
        "</button></div>"
        f'<span class="hl-tabs__count">1 / {len(ordered)}</span>'
        "</div></div></div></section>"
    )


# --------------------------------------------------------------------------------------
# /styleguide — the kit, mirrored
# --------------------------------------------------------------------------------------
# The static mirror of Pages/StyleGuide.razor: the same sections, the same sg-*
# classes (app.css styles both copies) and the same real content read from cv.json.
# Like the shell header this is deliberate duplication — the page renders here for
# the no-runtime visitor, and from Blazor after boot; change both. The token lists
# and easing constants mirror StyleGuide.razor's static arrays, which mirror the
# vendored kit's tokens: when the kit is re-synced, keep all of them in step.

SG_COLOR_TOKENS = [
    "--hl-bg", "--hl-surface-1", "--hl-surface-2", "--hl-surface-3", "--hl-surface-4",
    "--hl-line", "--hl-line-soft", "--hl-line-faint",
    "--hl-text-1", "--hl-text-2", "--hl-text-3", "--hl-text-4", "--hl-text-5",
    "--hl-accent", "--hl-accent-bright", "--hl-accent-teal", "--hl-accent-wash", "--hl-accent-edge",
    "--hl-info", "--hl-warn", "--hl-warn-wash", "--hl-gold", "--hl-violet",
    "--hl-action-bg", "--hl-action-ink", "--hl-header-bg", "--hl-veil", "--hl-raise", "--hl-edge-bright", "--hl-ghost-bg",
]

SG_GRADIENT_TOKENS = [
    "--hl-glow-accent", "--hl-glow-gold", "--hl-glow-violet", "--hl-wash-top",
    "--hl-lit-x", "--hl-lit-y", "--hl-lit-compare", "--hl-sheen", "--hl-hero-mesh",
]

SG_EASES = [
    ("--hl-ease-standard", 0.4, 0.0, 0.2, 1.0),
    ("--hl-ease-out", 0.0, 0.0, 0.2, 1.0),
    ("--hl-ease-reveal", 0.2, 0.8, 0.2, 1.0),
    ("--hl-ease-expo", 0.22, 1.0, 0.36, 1.0),
    ("--hl-ease-pop", 0.2, 0.9, 0.3, 1.2),
]

SG_SPACES = [4, 6, 8, 10, 12, 16, 20, 24, 40, 56, 80]

SG_RADII = [
    ("--hl-r-pill", "9999px"),
    ("--hl-r-window", "16px"),
    ("--hl-r-card", "12px"),
    ("--hl-r-panel", "10px"),
    ("--hl-r-chip-sq", "6px"),
    ("--hl-r-xs", "3px"),
]

SG_SHADOWS = ["--hl-shadow-deep", "--hl-shadow-window", "--hl-glow-lift", "--hl-glow-chip", "--hl-glow-dot"]

SG_ENTRANCES = [
    ("sg-kf-rise", "sg-kf--rise", "hl-rise", "700ms · reveal ease"),
    ("sg-kf-scene", "sg-kf--scene", "hl-scene-in", "800ms · expo ease"),
    ("sg-kf-line", "sg-kf--line", "hl-line-in", "300ms · out ease"),
    ("sg-kf-pop", "sg-kf--pop", "hl-pop-in", "500ms · pop ease"),
]


def _sg_swatch(token: str, gradient: bool = False) -> str:
    chip = (
        f'<span class="sg-swatch__chip sg-swatch__grad" style="background-image: var({token})"></span>'
        if gradient
        else f'<span class="sg-swatch__chip" style="background: var({token})"></span>'
    )
    # The value <small> is filled by js/styleguide.js once the runtime boots; the
    # swatch itself is the var(), so it always renders — in both themes, no JS.
    return f'<div class="sg-swatch">{chip}<code>{token}</code><small data-sg-token="{token}"></small></div>'


def _sg_ease_path(x1: float, y1: float, x2: float, y2: float) -> str:
    """The curve as SVG path points — 41 samples, y flipped, one decimal."""
    def bez(a: float, b: float, t: float) -> float:
        return 3 * (1 - t) ** 2 * t * a + 3 * (1 - t) * t**2 * b + t**3

    points = []
    for i in range(41):
        t = i / 40
        points.append(f"{bez(x1, x2, t) * 100:.1f},{100 - bez(y1, y2, t) * 100:.1f}")
    return " L ".join(points)


def _month_abbr(year_month: str) -> str:
    """'2024-11' -> 'Nov 2024' — DateRange.ToShortDisplayString's static half."""
    year, month = year_month.split("-")
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[int(month) - 1]} {year}"


def _short_period(period: dict) -> str:
    end = _month_abbr(period["end"]) if period.get("end") else "Present"
    return f"{_month_abbr(period['start'])} – {end}"


def _sg_tabs(cv: dict) -> str:
    """Two real skill groups in the kit's tabs contract, evidence rows included."""
    groups = list(cv.get("skillGroups", []))[:2]
    experience = cv.get("experience", [])

    def panel(group: dict) -> str:
        slug = _slugify(group["category"])
        cited: list[tuple[str, list[str]]] = []
        listed: list[str] = []
        for skill in group.get("skills", []):
            used_at = _employers_using(skill, experience)
            cited.append((skill, used_at)) if used_at else listed.append(skill)

        # The same authored arrow the skills section's rows carry (SkillMatrix's).
        arrow = (
            '<span class="skills-row__arrow" aria-hidden="true">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></span>'
        )
        rows = "".join(
            f'<li class="skills-row" title="{e(" · ".join(used_at))}">'
            f"{arrow}"
            f'<span class="skills-row__name">{e(skill)}</span>'
            f'<span class="skills-row__where">{e(_evidence(used_at))}</span>'
            "</li>"
            for skill, used_at in cited
        )
        cited_rows = f'<ul class="skills-rows">{rows}</ul>' if rows else ""
        also = f'<p class="skills-also">{e(" · ".join(listed))}</p>' if listed else ""

        return (
            f'<section class="hl-tabs__panel" data-hl-panel="{e(slug)}">'
            '<div class="skills-panel__copy">'
            f'<h3 class="hl-h3">{e(group["category"])}</h3>'
            f"{cited_rows}{also}</div></section>"
        )

    tabs = "".join(
        f'<button class="hl-tabs__tab" type="button" data-hl-tab="{_slugify(g["category"])}">'
        f'{e(g["category"])}</button>'
        for g in groups
    )
    panels = "".join(panel(g) for g in groups)

    return (
        '<div class="hl-tabs" data-hl-tabs data-hl-autoplay="7000">'
        f'<div class="hl-tabs__list" hidden>{tabs}</div>'
        f"{panels}"
        '<div class="hl-tabs__controls" hidden>'
        '<div class="hl-ring">'
        '<svg viewBox="0 0 40 40" aria-hidden="true">'
        '<circle class="hl-ring__track" cx="20" cy="20" r="17"></circle>'
        '<circle class="hl-ring__bar" cx="20" cy="20" r="17" pathLength="100"></circle>'
        "</svg>"
        '<button class="hl-ring__btn" type="button" aria-label="Pause autoplay">'
        '<svg class="hl-ring__icon hl-ring__icon--pause" viewBox="0 0 12 12" aria-hidden="true">'
        '<rect x="2" y="1.5" width="3" height="9" rx="1" fill="currentColor"/>'
        '<rect x="7" y="1.5" width="3" height="9" rx="1" fill="currentColor"/></svg>'
        '<svg class="hl-ring__icon hl-ring__icon--play" viewBox="0 0 12 12" aria-hidden="true" '
        'hidden><path d="M3.5 1.5v9l7-4.5z" fill="currentColor"/></svg>'
        "</button></div>"
        f'<span class="hl-tabs__count">1 / {len(groups)}</span>'
        "</div></div>"
    )


def styleguide_body(cv: dict) -> str:
    """The static /styleguide page: StyleGuide.razor's sections, class for class."""
    profile = cv["profile"]
    studies = _ordered_studies(cv)
    first = studies[0] if studies else None
    second = studies[1] if len(studies) > 1 else None
    roles = sorted(
        cv.get("experience", []),
        key=lambda entry: entry["period"]["start"],
        reverse=True,
    )

    colors = "".join(_sg_swatch(t) for t in SG_COLOR_TOKENS)
    gradients = "".join(_sg_swatch(t, gradient=True) for t in SG_GRADIENT_TOKENS)

    def typerow(token: str, sample: str, sample_class: str = "") -> str:
        cls = f' class="{sample_class}"' if sample_class else ""
        return f'<div class="sg-typerow"><code>{token}</code><span{cls}>{e(sample)}</span></div>'

    short_title = (first.get("shortTitle") or first["title"]) if first else ""
    typerows = (
        typerow("--hl-type-display", "I make the architecture decisions, then I write the code.", "hl-display")
        + typerow("--hl-type-h2", "Selected work, in depth", "hl-h2")
        + typerow("--hl-type-h3", cv["skillGroups"][0]["category"] if cv.get("skillGroups") else "", "hl-h3")
        + typerow("--hl-type-h4", short_title, "hl-h4")
        + typerow(
            "--hl-type-lead",
            "Anyone can list a technology. Where a skill shows up in the achievement "
            "record, the employers are named beside it.",
            "hl-lead",
        )
        + typerow("--hl-type-body", _first_sentence(first.get("summary", "")) if first else "", "hl-body")
        + typerow("--hl-type-label", _short_period(roles[0]["period"]) if roles else "", "hl-label")
        + typerow("--hl-type-term", f"open {first['slug']}" if first else "", "sg-term")
        + typerow("--hl-type-cta", "Read the CV", "sg-cta")
    )

    spaces = "".join(
        '<div class="sg-space">'
        f'<span class="sg-space__bar" style="width: var(--hl-space-{px})"></span>'
        f'<code class="sg-mono">--hl-space-{px} · {px}px</code></div>'
        for px in SG_SPACES
    )

    radii = "".join(
        f'<div class="sg-swatch"><span class="sg-radius" style="border-radius: var({token})"></span>'
        f"<code>{token}</code><small>{value}</small></div>"
        for token, value in SG_RADII
    )

    shadows = "".join(
        "<div class=\"sg-shadow\">"
        + (
            '<span class="hl-dot sg-shadow__dot"></span>'
            if token == "--hl-glow-dot"
            else f'<span class="sg-shadow__cast" style="box-shadow: var({token})"></span>'
        )
        + f'<code class="sg-mono">{token}</code></div>'
        for token in SG_SHADOWS
    )

    eases = "".join(
        f'<div class="sg-ease" data-sg-ease="{token}">'
        '<svg viewBox="0 0 100 100" aria-hidden="true">'
        '<rect x="0" y="0" width="100" height="100" fill="none" stroke="var(--hl-line)" '
        'stroke-width="1" vector-effect="non-scaling-stroke"></rect>'
        f'<path d="M {_sg_ease_path(x1, y1, x2, y2)}" fill="none" stroke="var(--hl-accent)" '
        'stroke-width="2" vector-effect="non-scaling-stroke"></path>'
        "</svg>"
        f"<code>{token}<br />cubic-bezier({x1}, {y1}, {x2}, {y2})</code>"
        "</div>"
        for token, x1, y1, x2, y2 in SG_EASES
    )

    entrances = "".join(
        f'<div class="sg-kf"><div class="sg-kf__stage">'
        f'<div class="sg-kf__box {box_class} is-anim" id="{element_id}"></div></div>'
        f'<button class="hl-chip" type="button" data-sg-replay data-sg-target="{element_id}" '
        f'data-sg-class="is-anim">Replay</button>'
        f'<p class="sg-kf__caption"><b>{name}</b>{meta}</p></div>'
        for element_id, box_class, name, meta in SG_ENTRANCES
    )

    buttons = (
        '<div class="sg-row" data-hl-reveal">'
        '<a class="hl-btn hl-btn--primary" href="/cv">Read the CV</a>'
        '<a class="hl-btn hl-btn--ghost" href="/#work">See the work</a>'
        '<a class="hl-btn hl-btn--primary hl-btn--sm" href="/cv">CV</a>'
        '<a class="hl-btn hl-btn--ghost hl-btn--sm" href="/testimonials">Testimonials</a>'
        '<button class="hl-btn hl-btn--primary" type="button" aria-disabled="true">Disabled</button>'
        '<button class="hl-btn hl-btn--ghost" type="button" aria-disabled="true">Disabled ghost</button>'
        "</div>"
    )

    # The badge carries the vendored commit post-boot (StyleGuide.razor reads
    # kit/VERSION over HTTP); statically it claims only "kit", never a guess.
    chips = ""
    compare = ""
    cards = ""
    console = ""
    if first:
        display = first.get("shortTitle") or first["title"]
        second_display = (second.get("shortTitle") or second["title"]) if second else display
        chips = (
            f'<div class="sg-row" data-hl-reveal">'
            f'<a class="hl-chip" href="{e(_study_url(first))}" data-hl-run="{e(first["slug"])}" '
            f'title="{e(display)}" aria-label="Run: {e(display)}">'
            f'<span class="hl-chip__label">{e(first["slug"])}</span></a>'
            f'<span class="hl-chip is-active" aria-pressed="true"><span class="hl-chip__label">{e(display)}</span></span>'
            f'<span class="hl-chip" aria-disabled="true"><span class="hl-chip__label">{e(second_display)}</span></span>'
            '<span class="hl-badge">kit</span>'
            '<span class="hl-badge"><span class="hl-dot" aria-hidden="true"></span> live</span>'
            "</div>"
        )
        cards = (
            '<div class="sg-cards" data-hl-reveal">'
            f'<div class="hl-card"><h4 class="hl-h4">{e(display)}</h4>'
            f'<p class="hl-body">{e(first.get("summary", ""))}</p></div>'
            + (
                f'<div class="hl-card hl-card--featured"><h4 class="hl-h4">{e(second_display)}</h4>'
                f'<p class="hl-body">{e(second.get("summary", ""))}</p></div>'
                if second
                else ""
            )
            + "</div>"
        )
        compare = (
            '<div class="hl-compare" data-hl-reveal>'
            '<div class="hl-compare__from"><h4 class="hl-h4">The problem</h4>'
            f'<p class="hl-body">{e(first.get("problem", ""))}</p></div>'
            '<div class="hl-compare__to"><h4 class="hl-h4">The outcome</h4>'
            f'<p class="hl-body">{e((first.get("outcomes") or [""])[0])}</p></div>'
            "</div>"
        )
        # The trimmed console reuses the hero mirror verbatim, fed two studies.
        console = f'<div class="sg-console">{_hero_console(studies[:2])}</div>'

    facts = [
        ("Timezone", profile.get("timezone")),
        ("Availability", profile.get("availability")),
        ("Working arrangement", profile.get("relocation")),
        ("Languages", " · ".join(profile.get("languages", [])) or None),
    ]
    facts_grid = (
        '<dl class="hl-grid sg-facts" data-hl-reveal>'
        + "".join(
            f'<div class="hl-cell"><dt class="hl-label">{e(label)}</dt><dd>{e(value)}</dd></div>'
            for label, value in facts
            if value
        )
        + "</dl>"
    )

    rails = "".join(
        '<div class="hl-rail" data-hl-reveal>'
        '<span class="hl-rail__bar" aria-hidden="true"></span>'
        f'<p class="hl-label"><span class="hl-key">{e(_short_period(role["period"]))}</span> · '
        f'{e(role["company"])}</p>'
        f'<p class="hl-body">{e(role["role"])}</p>'
        "</div>"
        for role in roles[:2]
    )

    def sub(title: str) -> str:
        return f'<h3 class="hl-h3 sg-sub">{title}</h3>'

    def section(rest: str, *inner: str) -> str:
        return (
            '<section class="section">'
            '<div class="hl-container section__frame">'
            f'<header class="section__head" data-hl-reveal>'
            f'<h2 class="hl-h2"><span class="hl-dim">The</span> {rest}</h2>'
            "</header>"
            + "".join(inner)
            + "</div></section>"
        )

    return (
        # The intro statically omits the commit clause — StyleGuide.razor reads
        # kit/VERSION at runtime; at prerender time there is nothing to read.
        '<section class="section"><div class="hl-container section__frame">'
        '<header class="section__head" data-hl-reveal>'
        '<h1 class="hl-display"><span class="hl-dim">Hairline,</span> as this site uses it</h1>'
        '<p class="hl-lead">The tokens and components on this page come from Hairline, a design '
        "kit that lives in its own repository and is vendored into this one.</p>"
        '<a class="hl-btn hl-btn--ghost sg-back" href="/">Back to the portfolio</a>'
        "</header></div></section>"
        + section("colour", f'<div class="sg-grid" data-hl-reveal>{colors}</div>')
        + section("gradients and glows", f'<div class="sg-grid" data-hl-reveal>{gradients}</div>')
        + section("type", f"<div data-hl-reveal>{typerows}</div>")
        + section(
            "space, radius and shadow",
            sub("Space") + f'<div class="sg-stack" data-hl-reveal>{spaces}</div>',
            sub("Radius") + f'<div class="sg-grid sg-grid--tight" data-hl-reveal>{radii}</div>',
            sub("Shadow") + f'<div class="sg-grid sg-grid--tiles" data-hl-reveal>{shadows}</div>',
        )
        + section(
            "motion",
            sub("Easing") + f'<div class="sg-eases" data-hl-reveal>{eases}</div>',
            sub("Entrances") + f'<div class="sg-kfs" data-hl-reveal>{entrances}</div>',
        )
        + section(
            "components",
            sub("Buttons") + buttons,
            sub("Chips, badge, live dot") + chips,
            sub("Cards") + cards,
            sub("Ruled grid") + facts_grid,
            sub("Compare") + compare,
            sub("Rail") + f'<div class="sg-rails">{rails}</div>',
            sub("Tabs") + _sg_tabs(cv),
            sub("Console") + console,
        )
        + section(
            "events",
            '<div class="sg-eventlog" id="sg-eventlog" data-hl-reveal>'
            '<p class="sg-eventlog__line" data-sg-log-placeholder>waiting for events…</p>'
            "</div>",
        )
    )


def home_pre_body(cv: dict) -> str:
    """The home route's full-bleed hero and marquee, mirroring Hero.razor + Home.razor."""
    studies = _ordered_studies(cv)
    figures_data = _hero_figures(cv)
    figures = "".join(_figure_cell(label, value) for label, value in figures_data)

    # The pitch is Hero.razor's, with the two derived figures interpolated the same way.
    markets, upgrade_days = figures_data[0][1], figures_data[1][1]
    pitch = (
        f"I designed and wrote the payment middleware behind Texas Chicken in {markets} countries, "
        "led the re-architecture that unfroze a legacy .NET estate — with an AI-guided workflow "
        f"that cut its upgrade cycle from 5–7 days to {upgrade_days} — and I am building a "
        "multi-tenant SaaS whose every structural decision is written down first."
    )

    return (
        '<section class="hero" aria-label="Introduction">'
        '<span class="hl-glow hero__glow" aria-hidden="true"></span>'
        '<div class="hl-container hero__grid">'
        '<div class="hero__main">'
        '<h1 class="hl-display hero__headline">'
        '<span class="hl-enter" style="--hl-enter-delay:0ms"><span class="hl-dim">I make the</span> '
        '<span class="hl-key">architecture decisions</span>,</span>'
        '<span class="hl-enter" style="--hl-enter-delay:90ms"><span class="hl-dim">then I write</span> the code.</span>'
        "</h1>"
        f'<p class="hl-lead hero__pitch hl-enter" style="--hl-enter-delay:200ms">{e(pitch)}</p>'
        '<div class="hero__actions hl-enter" style="--hl-enter-delay:300ms">'
        '<a class="hl-btn hl-btn--primary" href="/cv">Read the CV</a>'
        f'<a class="hl-btn hl-btn--ghost" href="/{CV_PDF_NAME}" target="_blank" rel="noopener" download>'
        "Download CV (PDF)</a>"
        '<a class="hl-btn hl-btn--ghost" href="/#work">See the work</a>'
        "</div>"
        f'<dl class="hl-grid hero__figures hl-enter" style="--hl-enter-delay:400ms" aria-label="Key figures">{figures}</dl>'
        "</div>"
        f"{_hero_console(studies)}"
        "</div></section>"
        f"{_tech_marquee(studies)}"
        f"{_skills_tabs(cv)}"
    )


def home_body(cv: dict, testimonials: list[dict] | None = None) -> str:
    profile = cv["profile"]

    # The hero mirror (home_pre_body) carries the name, the pitch, the figures, the
    # console AND the skills tabs (hairline.js drives the tabs without Blazor), so the
    # measured document below starts at the facts a recruiter asks for — no second h1,
    # no repeated pitch, no duplicated skills.

    # Section ids match the booted page's anchors, so the nav's /#work and /#timeline
    # links land somewhere real before the runtime exists too.
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

    education = "".join(
        f"<li>{e(entry['credential'])} — {e(entry['institution'])}, "
        f"{e(period_text(entry['period']))}</li>"
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

    # The booted page's contact cell joins the timezone and the working-overlap
    # with " — " (Home.razor); the static fact mirrors the same joined string.
    timezone = profile.get("timezone") or None
    if timezone and profile.get("workingOverlap"):
        timezone = f"{timezone} — {profile['workingOverlap']}"

    facts = [
        ("Location", profile.get("location")),
        ("Timezone", timezone),
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
            '<section id="testimonials"><h2>Testimonials</h2>'
            '<p><a href="/testimonials">Read them all</a>.</p>'
            f'<div class="testimonials__grid">{figures}</div></section>'
        )

    return f"""
      <dl>{fact_list}</dl>
      <section id="work"><h2>Selected work</h2>{case_studies}</section>
      <section id="timeline"><h2>Experience</h2>{experience}</section>
      <section id="credentials"><h2>Awards and Recognition</h2><ul>{awards}</ul>
      <h2>Education</h2><ul>{education}</ul>
      <h2>Certifications</h2><ul>{certifications}</ul></section>
      {testimonials_band}
      <section id="contact"><h2>Contact</h2>
      <p><a href="mailto:{e(profile['email'])}">{e(profile['email'])}</a></p></section>
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
      {evidence_list(study)}
    """


def evidence_list(study: dict) -> str:
    """The study's third-party corroboration, as plain links a crawler can follow."""
    links = study.get("evidence") or []
    if not links:
        return ""
    items = "".join(
        f'<li><a href="{e(link["url"])}" rel="noopener">{e(link["label"])}</a></li>' for link in links
    )
    return f"<h2>Check it yourself</h2><ul>{items}</ul>"


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
            # The hero and marquee are full-bleed; they ride ahead of the measured
            # document so the static first viewport matches the booted one.
            pre_body=home_pre_body(cv),
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
    # studies, so publishing a testimonial publishes its place here with no new code.
    # While the file is empty the page still exists (a stale link must not 404) but is
    # noindex and left out of sitemap.xml and llms.txt: absence is neutral, an
    # advertised "no recommendations yet" is not.
    entries = sorted(testimonials or [], key=lambda t: t.get("displayOrder", 0))
    routes.append(
        Route(
            path="testimonials",
            title=f"Testimonials — {name}",
            description=(
                f"Recommendations for {name} from colleagues and collaborators, "
                "each attributed to the person who wrote it."
            ),
            body=testimonials_body(entries, cv),
            json_ld=[breadcrumbs(base_url, [("Home", ""), ("Testimonials", "testimonials")])],
            indexable=bool(entries),
        )
    )

    # The live style guide. noindex on purpose: it is a working reference for
    # building the site (linked from the footer), not a route a recruiter or a
    # crawler needs — so it stays out of sitemap.xml and llms.txt while remaining
    # directly reachable. The body rides in pre_body like the home hero: kit
    # markup needs the full ruled column, not the measured .prerendered document
    # styles (the empty .prerendered div still hides the loading spinner).
    routes.append(
        Route(
            path="styleguide",
            title=f"Style guide · {name}",
            description=(
                "The design tokens and components this site is built from, "
                "shown live with this site's own content."
            ),
            pre_body=styleguide_body(cv),
            indexable=False,
        )
    )

    routes.append(
        Route(
            path="404",
            title=f"Page not found — {name}",
            description="That page does not exist on this site.",
            # The router console mirrors NotFound.razor with one difference: at
            # prerender time there is no requested path to show, so the open
            # line carries a generic placeholder instead. Change both together.
            body=(
                "<h1>Page not found</h1>"
                "<p>Nothing lives at this address. Try the "
                '<a href="/">home page</a> or the <a href="/cv">CV</a>.</p>'
                '<div class="hl-window notfound__window">'
                '<div class="hl-window__bar">'
                '<div class="hl-window__dots"><i></i><i></i><i></i></div>'
                '<span class="hl-window__title">router</span></div>'
                '<div class="hl-window__log notfound__log">'
                '<p class="hl-window__line hl-window__line--cmd">open &lt;this page&gt;</p>'
                '<p class="hl-window__line notfound__warn">route not found</p>'
                '<p class="hl-window__line hl-window__line--accent">◆ try one of these</p>'
                '<p class="hl-window__line notfound__route"><a href="/">/</a></p>'
                '<p class="hl-window__line notfound__route"><a href="/#work">/#work</a></p>'
                '<p class="hl-window__line notfound__route"><a href="/cv">/cv</a></p>'
                "</div></div>"
            ),
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
    "kit/hairline.css",
    "kit/hairline.js",
    "css/app.css",
    "css/print.css",
    "Cv.Web.styles.css",
    "favicon.png",
    "apple-touch-icon.png",
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
# at the other. The classes (site-header, site-nav, theme-toggle) are styled by app.css
# and the kit's .hl-* classes by hairline.css, both inlined into the same pages, so the
# chrome looks identical before and after boot — and Blazor replaces the whole block
# when it takes over.
NAV_LINKS = (
    ("/#work", "Work"),
    ("/#skills", "Skills"),
    ("/#timeline", "Timeline"),
    ("/#credentials", "Credentials"),
    ("/testimonials", "Testimonials"),
    ("/cv", "CV"),
)

# The nav renders the same link MainLayout.razor renders: only while a quote exists.
# A screening recruiter's one speculative click must not land on an empty page.
NAV_LINKS_WITHOUT_TESTIMONIALS = tuple(
    link for link in NAV_LINKS if link[0] != "/testimonials"
)


def static_shell_header(cv: dict, include_testimonials: bool) -> str:
    """
    The pre-boot chrome, duplicated from MainLayout.razor (see the note above):
    the kit's fixed .hl-header bar with the wordmark (name + short title), nav,
    theme switch and the CV pill inside .hl-container.

    The theme control is the same switch: tap toggles (delegated click in the shell's
    inline script), drag is added by that script after first paint. aria-checked is
    painted by paintStaticThemeButtons in index.html; the knob's side and icon are
    pure CSS state in app.css, so this markup and the Blazor render stay identical on
    the one control that switches the whole palette. The skip link lands on #main,
    which render() puts on the prerendered block.
    """
    links = NAV_LINKS if include_testimonials else NAV_LINKS_WITHOUT_TESTIMONIALS
    # The CV item is the bar's one primary pill; every other item is a plain link.
    nav = "".join(
        f'<a class="hl-btn hl-btn--primary hl-btn--sm site-nav__cta" href="{href}">{e(label)}</a>'
        if href == "/cv"
        else f'<a href="{href}">{e(label)}</a>'
        for href, label in links
    )
    # The wordmark's quiet companion: the discipline half of the title, before the
    # em dash — the same split MainLayout.razor's ShortTitle makes.
    title = cv["profile"]["title"]
    short_title = title.split("—")[0].strip() if title else ""
    return (
        '<a class="skip-link" href="#main">Skip to content</a>'
        '<header class="site-header hl-header">'
        '<div class="hl-container header-capsule">'
        f'<a class="site-header__name" href="/">{e(cv["profile"]["name"])}'
        f'<span class="site-header__title">{e(short_title)}</span></a>'
        '<button type="button" class="theme-toggle" role="switch" aria-checked="false" '
        'data-static-theme-toggle aria-label="Switch theme" title="Switch theme">'
        '<span class="theme-toggle__track" aria-hidden="true">'
        '<span class="theme-toggle__knob">'
        '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="12" cy="12" r="4"></circle>'
        '<path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2'
        'M4.93 19.07l1.41-1.41m11.32-11.32 1.41-1.41"></path></svg>'
        '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
        "</span></span></button>"
        f'<nav class="site-nav">{nav}</nav>'
        "</div></header>"
    )


def static_contact_dock(cv: dict) -> str:
    """
    The pre-boot contact dock, duplicated from MainLayout.razor (see its comment):
    the kit's .hl-dock — a full-width fixed bar at the viewport's foot, ghost pills
    for the channels and the CV as the one primary pill. No script, so it works for
    every visitor the WebAssembly runtime never reaches. The tel: href carries the
    digits (Profile.PhoneHref's C# equivalent: keep the leading +, drop everything
    else) without printing the number as text anywhere.
    """
    phone = cv["profile"]["phone"]
    tel = "".join(c for c in phone if c.isdigit() or c == "+")
    # Profile.WhatsAppHref's equivalent: wa.me wants bare digits, no "+".
    whatsapp = "https://wa.me/" + "".join(c for c in phone if c.isdigit())
    mail = e(cv["profile"]["email"])
    return (
        '<nav class="contact-dock hl-dock" aria-label="Contact">'
        f'<a class="contact-dock__action" href="tel:{tel}">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 '
        '19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 '
        '2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 '
        '2.81.7A2 2 0 0 1 22 16.92z"></path></svg>'
        "<span>Call</span></a>"
        f'<a class="contact-dock__action" href="{whatsapp}" target="_blank" rel="noopener">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"></path>'
        '</svg>'
        "<span>WhatsApp</span></a>"
        f'<a class="contact-dock__action" href="mailto:{mail}">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="2" y="4" width="20" height="16" rx="2"></rect>'
        '<path d="m22 6-10 7L2 6"></path></svg>'
        "<span>Email</span></a>"
        f'<a class="contact-dock__action contact-dock__action--cv" href="/{CV_PDF_NAME}" '
        'target="_blank" rel="noopener" download>'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M12 3v12m-5-5 5 5 5-5M5 21h14"></path></svg>'
        "<span>CV</span></a></nav>"
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
KIT_CSS_LINK_RE = re.compile(r'<link rel="stylesheet" href="kit/hairline\.css[^"]*" />')
PRINT_CSS_LINK_RE = re.compile(r'<link rel="stylesheet" href="(css/print\.css[^"]*)" />')
COMPONENT_CSS_LINK_RE = re.compile(r'<link href="(Cv\.Web\.styles\.css[^"]*)" rel="stylesheet" />')


def inline_first_paint_css(page: str, app_css: str, kit_css: str = "") -> str:
    """Apply the three-way stylesheet split to one rendered page."""
    # A "</style" inside the CSS would terminate the inline block early and mangle the
    # page. Verified absent today; this makes the failure loud if that ever changes.
    if "</" in kit_css:
        raise SystemExit("prerender: kit/hairline.css contains '</'; it cannot be inlined safely.")
    if "</" in app_css:
        raise SystemExit("prerender: app.css contains '</'; it cannot be inlined safely.")

    # The kit is inlined first: its :root tokens must be parsed before app.css's
    # aliases read them, exactly like the link order in the shell.
    page, count = KIT_CSS_LINK_RE.subn(
        lambda _: f"<style>\n{kit_css}</style>", page, count=1
    )
    if count == 0:
        raise SystemExit('prerender: could not find the kit/hairline.css link to inline.')

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
    contact_dock: str = "",
    sw_registration: str = "",
    kit_css: str = "",
) -> str:
    url = route.url.format(base=base_url)
    page = version_asset_urls(shell, versions or {})
    page = inline_first_paint_css(page, app_css, kit_css)

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
    # in the shell is kept ahead of it. Everything sits in a <main id="main"> — the
    # same element MainLayout.razor renders — so the fixed-header offset in app.css
    # applies to the static copy exactly as it does after boot; the home route's
    # full-bleed hero (pre_body) rides ahead of the measured .prerendered document.
    if route.body or route.pre_body:
        def replace_app(match: re.Match[str]) -> str:
            return (
                f"{match.group(1)}{match.group(2)}"
                f"{shell_header}"
                f'\n<main id="main">{route.pre_body}'
                # id="main" is the skip link's target: the static shell carries the
                # same link MainLayout.razor does, and this block is its destination
                # until Blazor's own <main id="main"> replaces everything here.
                f'<div class="prerendered">{route.body}</div></main>'
                # The dock is position:fixed, so its DOM home is arbitrary; it rides
                # inside #app because Blazor replaces that block wholesale on boot.
                f"{contact_dock}"
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

    # The vendored kit rides the same contract: its stylesheet is inlined into
    # first paint and its script is referenced from the shell by bare path. A
    # publish missing half the kit would serve pages referencing a file GitHub
    # Pages answers with its 404 page — the link does not break visibly, it just
    # quietly stops being the kit. Fatal for both files, never a silent skip.
    kit_css_path = publish / "kit" / "hairline.css"
    kit_js_path = publish / "kit" / "hairline.js"
    for kit_file in (kit_css_path, kit_js_path):
        if not kit_file.exists():
            print(
                f"FAIL  No {kit_file.relative_to(publish).as_posix()} in {publish} — "
                "a missing kit file must never silently ship.",
                file=sys.stderr,
            )
            return 1
    kit_css = kit_css_path.read_text(encoding="utf-8")

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

    shell_header = static_shell_header(cv, include_testimonials=bool(testimonials))
    contact_dock = static_contact_dock(cv)
    routes = build_routes(cv, base_url, testimonials)

    for route in routes:
        page = render(route, shell, base_url, versions, preloads, app_css, shell_header, contact_dock, sw_registration, kit_css)

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
