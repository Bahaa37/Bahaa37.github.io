---
name: Spec Sheet
description: The portfolio as good engineering documentation — cool neutral greys, a graphite (no-hue) accent, Geist and Geist Mono, flat sections separated by hairlines, and nothing shaped like a capsule.
colors:
  paper: "#f7f8fa"          # page ground            dark: #0d1117
  sheet-solid: "#ffffff"    # framed panels          dark: #151b23
  ink: "#111827"            # headings, primary text dark: #e6eaf0
  ink-soft: "#374151"       # prose                  dark: #b4bcc8
  ink-faint: "#5b6472"      # smallest text          dark: #8b95a3
  accent: "#111827"         # links, primary, focus  dark: #f3f4f6
  accent-bright: "#374151"  # hover                  dark: #d1d5db
  accent-wash: "#eef0f3"    # quiet accent fill      dark: #1b222c
  action-bg: "#111827"      # primary button fill    dark: #f3f4f6
  action-ink: "#ffffff"     # text on the fill       dark: #0d1117
  line: "#dce0e6"           # hairlines              dark: #2a323d
  edge-silver: "#858e9c"    # control borders, 3:1   dark: #5e6878
  wash: "#eef0f3"           # tag fill               dark: #1b222c
  # Dark values live in src/Cv.Web/wwwroot/css/app.css, written TWICE (the
  # prefers-color-scheme block guarded by :not([data-theme="light"]) and the
  # :root[data-theme="dark"] rule). Token NAMES are inherited from earlier worlds
  # (--paper, --gold, --edge-silver…) so every scoped stylesheet still resolves;
  # --gold no longer means bronze and resolves to the accent.
typography:
  family: "Geist (UI, headings, body); Geist Mono (dates, figures, tags, data lines)"
  hero: "clamp(2.3rem, 1.4rem + 3.2vw, 3.7rem) / 1.04, weight 650, tracking -0.045em"
  section-title: "clamp(1.6rem, 1.2rem + 1.6vw, 2.25rem) / 1.12, weight 650, tracking -0.03em"
  body: "1.0625rem / 1.65, weight 400"
  mono: "0.75–0.82rem, tabular numerals, sentence case — never tracked uppercase"
rounded:
  sheet: "10px (hero figures panel)"
  panel: "8px (outcomes, awards, study links, dock)"
  control: "6px (buttons, theme switch, skip link)"
  tag: "3px (stack tags)"
  capsule: "none — nothing in this world is 999px"
spacing:
  section: "clamp(2.6rem, 1.8rem + 3vw, 4.5rem) block padding, 1px top hairline"
  measure: "68ch"
  page: "1120px"
---

# Design System: Spec Sheet

Chosen 2026-10-04 after the owner said he did not like the pills or the colours of
the Annual Report world (rag paper, ledger green, bronze), and after two reviews: a
design critique (every section shouted at the same volume from inside a paper card;
about twenty capsule rules; a broken key-figures row) and a hiring-manager read
("Built alone", three times, reads as a solo hero on an architect-track profile).

## Principles

1. **One surface, few frames.** Sections are flat and separated by whitespace and one
   hairline. Only evidence is framed: the hero's key figures, a study's outcomes,
   awards, prev/next links. A frame means "this is the proof".
2. **No hue.** The accent is graphite (2026-10-04: the owner rejected cobalt after
   seeing six options). Near-black marks the primary action, focus, the current nav
   item and the current role; links are always underlined so they never rely on
   colour. Nothing on the page carries a hue except photos and diagrams.
3. **No capsules.** Buttons are 6px rectangles in sentence case; tags are 3px squares
   with no border; status ("Current", "Returned", "In progress") is text with a
   marker; the theme switch is squared off. Skills are cited rows, not chips.
4. **Mono is for data only.** Dates, figures, tags, the stack line, organisation
   bylines — in sentence case. Never tracked uppercase labels.
5. **Every figure is derived.** Hero figures are read from cv.json by anchor phrase
   (`Hero.razor`); `RealCvDocumentTests.TheHeroFiguresStillHaveASourceInTheRecord`
   fails the build if a copy edit removes an anchor.

## Layout

- **Hero:** two columns from 960px (claim + pitch + actions | figures panel, 2×2);
  one column below, figures after the actions so the CTA sits in the first screen.
- **Home order:** hero → selected work (flagship panel + index rows) → skills →
  experience → credentials → contact. Proof before inventory.
- **Case study pages:** long-form styles live in app.css (`.study*`), 68ch measure,
  paragraphs split on blank lines in cv.json, outcomes framed, third-party evidence
  ("Check it yourself") when the study carries `evidence` links.
- **Contact dock:** fixed bar with Call, WhatsApp (wa.me, derived from the phone),
  Email and CV (filled, the PDF). Mirrored in prerender.py's `static_contact_dock`.
- **Disclosures:** outlined buttons with a turning chevron, never bare text.
- **Pre-boot document:** `.prerendered` gets a readable document style — it is the
  whole page for visitors whose runtime never boots.

## Rules carried from earlier worlds (not taste — correctness)

- Dark tokens are written twice; change both.
- No `backdrop-filter`, no `color-mix()`, no individual `translate` property.
- Hiding is additive-only behind `.js-motion` (motion.js); reduced motion restores
  everything; print drops the chrome.
- Header and contact dock markup are mirrored in `_tools/prerender.py`
  (`static_shell_header`, `static_contact_dock`) — change both sides.
- The printed CV (/cv) stays ATS-plain; only its on-page action row follows this world.

## Don't

- Don't reintroduce capsules, cream/paper grounds, a coloured accent or bronze.
- Don't add cards inside sections or shadows on sections.
- Don't type a figure into markup.
