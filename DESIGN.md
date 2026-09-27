---
name: Legal Tender — Bahaa Aldeen Mohamed
description: The portfolio as an engraved banknote — rag-paper ground, intaglio ink, one banknote-green accent, bronze reserved for recognition, engine-turned line geometry as structure.
colors:
  ink: "#14261e"
  ink-soft: "#3d5347"
  ink-faint: "#5d7263"
  paper: "#f3eede"
  sheet-bg: "rgba(255, 252, 242, .92)"
  sheet-solid: "#faf6ea"
  sheet-line: "rgba(20, 38, 30, .2)"
  accent: "#0c5a45"
  accent-bright: "#0a6b52"
  accent-wash: "#e4e9d6"
  action-bg: "#0c5a45"
  action-bg-hover: "#094a38"
  action-ink: "#f6f1e2"
  gold: "#7a4a2b"
  gold-wash: "#f0e4d2"
  alarm: "#a03d28"
  alarm-wash: "#f2e3dc"
  stage-legacy: "#5d7263"
  stage-lead: "#0a6b52"
  edge-metal: "#b8ab8c"
  edge-silver: "#b8ab8c"
  glass-bg: "#faf6ea"
  glass-line: "#b8ab8c"
  dock-bg: "#faf6ea"
  line: "rgba(20, 38, 30, .16)"
  wash: "rgba(20, 38, 30, .05)"
  # Values above are the LIGHT canon. Dark values are equally canonical and live in
  # src/Cv.Web/wwwroot/css/app.css, written TWICE (the prefers-color-scheme block
  # guarded by :not([data-theme="light"]), and the :root[data-theme="dark"] rule).
  # .impeccable/design.json carries darkCanonical per color.
  # --gold is bronze in this world; --glass-bg/--glass-line/--dock-bg RESOLVE to
  # --sheet-solid/--edge-silver in code (this world spends no blur) — the hexes here
  # are their resolved values; --glass-highlight: none and --glass-blur: 0px.
typography:
  display:
    fontFamily: "Bodoni Moda, Didot, 'Bodoni MT', 'Times New Roman', serif"
    fontSize: "clamp(2.5rem, 1.4rem + 4.6vw, 4.3rem)"
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Bodoni Moda, Didot, 'Bodoni MT', 'Times New Roman', serif"
    fontSize: "clamp(1.65rem, 1.1rem + 2.3vw, 2.55rem)"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Spectral, Georgia, 'Times New Roman', serif"
    fontSize: "clamp(1.2rem, 1.05rem + 0.7vw, 1.5rem)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Spectral, Georgia, 'Times New Roman', serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.62
    letterSpacing: "normal"
  small:
    fontFamily: "Spectral, Georgia, 'Times New Roman', serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  meta:
    fontFamily: "Fragment Mono, ui-monospace, 'Cascadia Mono', Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.02em"
  label:
    fontFamily: "Fragment Mono, ui-monospace, 'Cascadia Mono', Consolas, monospace"
    fontSize: "0.76rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.12em"
  micro:
    fontFamily: "Fragment Mono, ui-monospace, 'Cascadia Mono', Consolas, monospace"
    fontSize: "0.7rem"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.1em"
rounded:
  pill: "999px"
  sheet: "10px"
  md: "8px"
  sm: "6px"
  stamp: "3px"
  node: "50%"
spacing:
  gutter: "1.25rem"
  stack: "1.6rem"
  measure: "66ch"
  page: "1120px"
  header-band: "3.4rem"
components:
  button-primary:
    backgroundColor: "{colors.action-bg}"
    textColor: "{colors.action-ink}"
    rounded: "{rounded.pill}"
    padding: "0.55rem 1.3rem"
    height: "44px"
    typography: "0.78rem Fragment Mono, uppercase, 0.07em tracking"
  button-primary-hover:
    backgroundColor: "{colors.action-bg-hover}"
  button-ghost:
    backgroundColor: "{colors.sheet-solid}"
    textColor: "{colors.ink}"
    borderColor: "{colors.edge-silver}"
    rounded: "{rounded.pill}"
    padding: "0.55rem 1.3rem"
    height: "44px"
    typography: "0.78rem Fragment Mono, uppercase, 0.07em tracking"
  chip:
    backgroundColor: "{colors.sheet-bg}"
    textColor: "{colors.ink-soft}"
    borderColor: "{colors.sheet-line}"
    rounded: "{rounded.pill}"
    padding: "0.28rem 0.8rem"
    typography: "0.88rem Spectral, weight 400"
  chip-evidenced:
    backgroundColor: "{colors.accent-wash}"
    textColor: "{colors.ink}"
    borderColor: "{colors.accent}"
    rounded: "{rounded.pill}"
    typography: "0.88rem Spectral, weight 600"
  metric-chip:
    backgroundColor: "{colors.gold-wash}"
    textColor: "{colors.gold}"
    borderColor: "{colors.gold}"
    rounded: "{rounded.stamp}"
    padding: "0.08rem 0.5rem"
    typography: "0.7rem Fragment Mono, tabular-nums"
  header-capsule:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    height: "3.4rem band; nav links 36px pills, 0.72rem Fragment Mono caps"
  theme-toggle:
    kind: "medallion switch (role=switch, same iOS-style mechanics as before, new metal)"
    track: "46x26px pill, ink at 14% + aged-brass hairline; inset shadow"
    knob: "20px brass circle (light #f8f3e6->#d9cdb0; dark #35473b->#1b2a21), 12px sun/moon glyph; transform-based travel"
    hitArea: "44px (2.75rem button wraps the track)"
    states: "knob left + sun = light; knob right + moon = dark — pure CSS state, twice-written selectors"
  contact-dock:
    backgroundColor: "{colors.sheet-solid}"
    textColor: "{colors.ink-soft}"
    borderColor: "{colors.edge-silver}"
    rounded: "{rounded.pill}"
    height: "44px per action"
    position: "fixed; bottom-right desktop, centred ≤720px; opaque, no blur"
  back-to-top:
    kind: "44px circular runtime chrome, parked above the contact dock"
    backgroundColor: "{colors.sheet-solid}"
    borderColor: "{colors.edge-silver}"
    textColor: "{colors.ink-soft}; {colors.accent} on hover"
    shadow: "--shadow-float at rest; --shadow-lift on hover"
    states: "display:none at rest; motion.js's .is-shown past one viewport of scroll"
  award-tile:
    backgroundColor: "{colors.gold-wash}"
    textColor: "{colors.gold}"
    borderColor: "{colors.gold}"
    rounded: "{rounded.md}"
    padding: "1.1rem 1.2rem"
    note: "medallion: inner ring via inset shadows (3px sheet-solid, 4px gold) inside the border"
---

# Design System: Legal Tender

## Overview

**Creative North Star: "Legal Tender"** — the whole-portfolio world replacement shipped 2026-09-27, chosen on the impeccable decision page (answer: model-pick — Impeccable's Pick, no steer, buildPath code; seed key `aaa7f143`). It replaces the Frosted Keynote / Sky Aluminum world (the anti-reference) and beats the roll's assigned direction ("The Annual Report") on audience identification; that card's disciplines carried in as craft, not as its look. The old hero before/after diagram is deleted at the user's word; its argument lives in the flagship case study.

The site behaves like an engraved banknote. The solo-built payment gateway earns the denomination: the hero is a note face — a "9" at banknote scale filled with engine-turned line geometry, serialled with real figures (9 markets · 7 gateways · 491 tests), beside the legend lettering "Nine countries. / One gateway. / Built / alone." and the plate legend "BUILT ALONE · END TO END". Content floats as a plate series: every sheet is a solid paper plate carrying a banknote border — an outer edge, an inner rule inset 7px, and a machined quarter-dot seated on each corner of that inner rule. Where every other portfolio shows screenshots, this one shows intaglio: the craft of printing value, held by the engineer who built payment rails for nine markets. It refuses the category-default project grid and the old aluminum world alike.

The dosage law governs everything: **intaglio is flat ink.** No `backdrop-filter` is spent anywhere — the world's glass tokens (`--glass-bg`, `--glass-line`, `--glass-blur`, `--glass-highlight`) resolve to flat paper, a hairline, `0px`, and `none`, so scoped stylesheets from the previous world keep resolving without importing blur. The header is an opaque paper band under a double rule; the contact dock is an opaque seal strip. Depth comes from a two-step paper-lift shadow, never from a halo, and never from anything moving behind the content (the still-ground rule). One accent — banknote green — owns action, links, focus, the timeline spine, and the engraving itself; bronze is the one warm metal and it marks recognition only.

Motion is additive and once-only. `motion.js` adds `.js-motion` and is the only thing that gates a hidden state; without the script nothing is hidden. The signature interaction is "the plate press": the denomination's line field prints in one damped pass (~1s soft clip wipe) on a visitor's proved first look, and sections enter with a single press-settle (rise 10px from visible). The printed CV sits outside this system entirely (ATS-plain by product rule) — plain where machines read, engraved where humans look.

**Key Characteristics:**

- Still rag-paper ground (`html` carries `--paper`) — nothing layered, nothing animated behind the content, zero backdrop elements to survive the boot boundary.
- Plate frames everywhere: sheets carry the double-rule banknote border with corner quarter-dots; plate titles sit under a double rule; the sticky header band is opaque paper under a double rule.
- One green accent for action, links, focus, the engraving, and the security-thread progress bar; bronze spent on recognition only (medallions, award metric chips, the hero award figure); no blur anywhere.
- Bodoni Moda for display and plate titles (the engraved didone), Spectral for document prose, Fragment Mono for serials, labels, and every figure in tabular numerals.
- Squared 3px "registry stamps" (badges, metric chips, stack tags) against full pills on all interactive chrome; controls are capsules, data is stamped.
- Reduced motion restores every hidden state; the static layer is the contract — every figure ships its final value in markup.

## Colors

Warm rag paper and aged-cream ink on one ground, a green-black intaglio ink ramp, one banknote green, and a bronze medallion metal — flat, engraved, exact. In dark the ground becomes a deep green-black intaglio plate (`#0d1712`, not gray) and the ink becomes aged cream.

### Primary
- **Banknote Green** (`--accent` #0c5a45 / dark #4ba583; `--accent-bright` #0a6b52 / dark #63bd97): the one accent — links (`--accent`, brightening to `--accent-bright` on hover), focus rings, the timeline spine and node dots, group labels, the hero legend and the italic accent line of the headline, and the engine-turned fill of the denomination. `--accent-wash` #e4e9d6 (dark #182b22) tints evidenced chips, outcome blocks, the "on CV" pill, and the denomination's corner wash.
- **Action Fill** (`--action-bg` #0c5a45 / dark #2e7d5f, `--action-bg-hover` #094a38 / dark #276b50): the primary seal button and the nav's `.is-current` mark, carrying `--action-ink` #f6f1e2 (dark #f2eede) — aged-cream ink on green, not white. Fill and text link split as before because a fill and a link need different contrast solutions.

### Tertiary
- **Medal Bronze** (`--gold` #7a4a2b / dark #c98a4b, `--gold-wash` #f0e4d2 / dark #292117): the one warm metal — the token kept its old *name* (`--gold`) and changed its metal. Spent on recognition: award medallions, the bronze metric chip on award-earning achievements, and the hero's company-awards figure. The "Returned" badge is a trajectory marker, not recognition — it takes the accent, never the bronze. Two non-award surfaces borrow the wash only (the Blazor error bar, the write-up's pull-quote tile); bronze ink and bronze borders never touch action, links, focus, or badges.
- **Alarm** (`--alarm` #a03d28 / dark #e5806a, `--alarm-wash` #f2e3dc / dark #2c1a15): reserved alert note. The old diagram that consumed it is gone; the token is defined but currently unconsumed — a reserve, not a license.

### Neutral
- **Ink** (`--ink` #14261e; dark #e6dcc2): headings and primary text — green-black like intaglio on rag. **Ink Soft** (`--ink-soft` #3d5347; dark #c0bda3): body prose and ledes. **Ink Faint** (`--ink-faint` #5d7263; dark #9a9574): the smallest text — held at or above 4.5:1 on the plate face; also the colour of the frame's corner quarter-dots.
- **Rag Ground** (`--paper` #f3eede / dark #0d1712): the `html` background — one flat, still surface. Dark is the intaglio plate: green-black, deliberately not gray.
- **Plate faces** (`--sheet-solid` #faf6ea / dark #122019 — the opaque face every sheet, dock, ghost button, and back-to-top uses; `--sheet-bg` rgba(255,252,242,.92) / dark rgba(19,33,26,.92) — the translucent-without-blur chip fill) with **Sheet Hairline** (`--sheet-line` rgba(20,38,30,.2) / dark rgba(230,220,194,.18)): chip and tag borders, denomination plate rings, case-section separators.
- **Hairline** (`--line` rgba(20,38,30,.16) / dark rgba(230,220,194,.15)) and **Wash** (`--wash` rgba(20,38,30,.05) / dark rgba(230,220,194,.06)): the inner rules of every frame and double rule, and the quiet fill of diagram canvases and code blocks.
- **Aged-Brass Hairline** (`--edge-silver` #b8ab8c / dark #56685a): the single-tone rule on fixed chrome — header band, dock, back-to-top, ghost buttons, the theme switch. `--edge-metal` collapses to the same value: no gradient metal in this world.
- **Glass, resolved flat** (`--glass-bg` → `--sheet-solid`; `--glass-line` → `--edge-silver`; `--glass-highlight: none`; `--glass-blur: 0px`; `--dock-bg` → `--sheet-solid`): kept as names so scoped stylesheets resolve unchanged, re-pointed to flat paper because intaglio spends no blur. Never re-introduce a blur behind these tokens.

### Permitted derivatives
Alpha tints of a documented hue and `color-mix()` results against a documented hue are accepted as long as the parent hue is on this page (the write-up's ink-tinted code blocks work this way). The selection tint is the accent at a 26% mix; the timeline's node pulse is the dark-theme accent at 40%. What requires a palette entry is a **new hue** — a colour whose parent is not already documented here. The syntax-highlighting hexes in the write-up's code blocks (#8250df/#953800/#0a7c62 and their dark twins) are grandfathered fixed values, twice-written like the tokens.

### Named Rules
**The Twice-Written Rule.** Dark tokens are written twice in `app.css` — inside `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]` — because plain CSS cannot share one declaration list between them without breaking the guard. Any token change is made in both places, always. The two blocks must stay byte-identical.

**The Bronze Is Recognition-Only Rule.** Bronze (`--gold`) is spent on exactly one subject — recognition: medallions, award metric chips, the award figure. Its rarity is what makes the medal land. Trajectory markers ("Now", "Returned") take the accent, never bronze.

## Typography

**Display Font:** Bodoni Moda (with Didot, "Bodoni MT", Times New Roman fallbacks)
**Body Font:** Spectral (with Georgia, Times New Roman fallbacks)
**Label/Mono Font:** Fragment Mono (with ui-monospace, Cascadia Mono, Consolas fallbacks)

**Character:** The engraved didone for voice, the document serif for prose, the registry mono for data — a banknote's three voices. Bodoni carries the denomination-scale display and every plate title; Spectral carries every word of argument like a specimen document; Fragment Mono carries serials, labels, buttons, and all figures in tabular numerals, so data reads as engraved data. All three load non-blocking from Google Fonts (`display=swap`, stylesheet swapped in onload, `<noscript>` fallback) so the font stylesheet never delays first paint.

### Hierarchy
- **Display** (Bodoni 600, clamp(2.5rem, 1.4rem + 4.6vw, 4.3rem), 1.04, −0.02em): the hero headline only — four clipped lines, one of which ("One gateway.") is italic in Banknote Green.
- **Headline** (Bodoni 600, clamp(1.65rem, 1.1rem + 2.3vw, 2.55rem), 1.08, −0.01em): plate titles (`.sheet__title`), each sitting under its double rule.
- **Title** (Spectral 700, clamp(1.2rem, 1.05rem + 0.7vw, 1.5rem), −0.015em): case-study titles and write-up headings; the write-up's page title steps up to clamp(2rem, 1.4rem + 2.6vw, 3rem).
- **Body** (Spectral 400, 16px, 1.62): all prose, capped at the 66ch measure; ledes at 1.02–1.06rem in Ink Soft; the write-up's long-form runs 1.72 leading.
- **Small** (Spectral 400, 0.92–0.98rem): card-level prose — timeline bullets, cert names, summaries. The floor for anything that reads as a sentence.
- **Meta** (Fragment Mono 400, 0.68–0.82rem): serials, attributions, dates, issuers, org lines, the hero facts row (0.8rem, strong values in `--ink`, `tabular-nums` throughout) — always Ink Faint except where a figure is the subject.
- **Label** (Fragment Mono, uppercase, 0.72–0.78rem, letter-spacing 0.1–0.12em): group titles (Banknote Green), section subs and breadcrumbs (Ink Faint), nav links (0.72rem, tracked caps), dock actions (0.72rem).
- **Micro** (Fragment Mono 700, 0.62–0.7rem, 0.1em): badges and the "on CV" pill. The denomination's serial lines sit at 0.56rem / 0.14em tracking — a plate inscription, not reading text.

### Named Rules
**The No-Kicker Rule.** Nothing sits above a heading — no kickers, no eyebrows, no numbered wayfinding. A plate opens with its title; the plate legend ("BUILT ALONE · END TO END") and every byline go *below* the title, in tracked mono.

**The Serials Rule.** Every figure on the note is real and derived, never typed: the serial plate reads 9 markets · 7 gateways · 491 tests, the hero's count-up figures are extracted from the case-study record (`Hero.razor`), and final values ship in the markup. A banknote with a made-up serial is counterfeit.

## Layout

A single 1120px page column (`--page`) on the rag ground, entered with `min(100% - 2.5rem, var(--page))` — the 1.25rem gutter doubled. Content floats as a plate series: sheets are solid faces stacked 1.6rem apart, padded `clamp(1.8rem, 1.2rem + 3vw, 3.4rem)` block / `clamp(1.3rem, 3.5vw, 3rem)` inline. The hero plate runs wider — `calc(var(--page) + 5rem)` — so the denomination and the legend share one viewport. Long-form prose sizes to the measure (`--measure` 66ch). Inner grids use `repeat(auto-fit, minmax(280–300px, 1fr))` (skill groups, awards, facts) so wrapping is intrinsic; case rows are hairline-separated index rows, two-up on wide screens.

The header is a sticky opaque paper band (`--header-band` 3.4rem) under a double rule — border-bottom plus an inset second rule — not a floating capsule. Wordmark left in Bodoni; the nav is a tracked-mono-caps strip with 36px pill links (`margin-inline-start: auto` at ≥721px). Anchor navigation is token-driven: `.sheet[id], .case[id]` clear the band by `calc(var(--header-band) + 1.3rem)` on desktop.

Breakpoints, and what changes at each:
- **430px**: the nav strip tightens (0.5rem padding, 0.64rem labels, 0.06em tracking) so every link — CV last, the recruiter's destination — stays inside the mask instead of clipping.
- **720px**: the header band wraps to two rows and `--header-band` rises to 6rem, which drives the mobile scroll margin (`calc(var(--header-band) + 1rem)`); the contact dock centres in the thumb zone and `main` grows a 7rem bottom pad; the hero takes a 4.6rem bottom clear zone so the note face never sets type under the dock.
- **900px**: the hero grid stacks; the denomination plate centres at max-width 240px and the headline steps down.
- **940px**: timeline entries gain the 10.5rem right-aligned period column (below it the period sits above the body with a tight 0.7rem rail gutter); certifications flow into two balanced columns, featured set first, entries never splitting across a column.

### Named Rules
**The Dock Clear-Zone Rule.** On a phone the note face's first viewport is never masked by the seal strip: the hero carries 4.6rem of bottom clear zone, `main` carries 7rem, and the dock itself stays unprinted (`.js-motion .contact-dock:not(.is-shown)`) until the visitor has moved. The gate sits behind `.js-motion`, so no-JS and reduced-motion visitors always have the dock.

## Elevation & Depth

Depth is one flat ground under solid plates — never drop shadows on inline elements, nothing layered behind the content. The ground lives on `html` (`--paper`) as a plain colour; there is no backdrop element in the DOM at all, so the prerender fill and the Blazor boot have nothing to preserve.

**The No-Blur Rule.** This world spends no `backdrop-filter` anywhere — intaglio is flat ink on paper. The inherited `--glass-*` tokens resolve flat (`--glass-bg` → `--sheet-solid`, `--glass-line` → `--edge-silver`, `--glass-highlight: none`, `--glass-blur: 0px`), so the header band and the contact dock are opaque and no page ever holds a live GPU blur. Any new surface asking for glass gets paper instead.

**The still-ground rule:** nothing behind the content animates, ever. All movement lives inside the content (the plate press, the spine draw), and all depth lives on the plates themselves. The theme switch's one short-lived pulse (`WAAPI`, transform + opacity, outside `#app`) is the only exception, and it is user-initiated and gone in 620ms.

**The security thread:** the reading-progress bar is a 2px fixed `body::before` in solid accent across the top, driven by `animation-timeline: scroll()` — no script, no markup — inside `@supports`, hidden in print.

### Shadow Vocabulary
- **Plate shadow** (`--shadow-sheet`: `0 1px 2px rgba(20,38,30,.05), 0 14px 36px rgba(20,38,30,.09)`; dark: `0 1px 2px rgba(0,0,0,.3), 0 16px 40px rgba(0,0,0,.35)`): every content sheet — one crisp contact step, one wide paper lift. Two steps, never three; a paper lift, not a halo.
- **Float shadow** (`--shadow-float`: `0 2px 6px rgba(20,38,30,.08), 0 12px 26px rgba(20,38,30,.13)`; dark: black-based): the header band's chrome, the contact dock, back-to-top, and the primary seal at rest.
- **Hover lift** (`--shadow-lift`: `0 8px 20px rgba(20,38,30,.15)`; dark: black-based): the single response shadow under buttons, chips, and back-to-top on hover. No coloured glow — emphasis comes from elevation, not light.

### Named Rules
**The No-Blur Rule.** No `backdrop-filter` on any surface, ever. Fixed chrome is opaque paper under a brass hairline; content plates are solid. A blur under a long read is GPU cost for nothing behind an opaque face — and in this world, fuzz is the opposite of engraving.

## Shapes

Three form families and a rule system. **Pills (999px):** anything interactive — buttons, nav links, chips, the dock, back-to-top, the skip link, the theme switch. **Plates (10px, `--radius-sheet`):** content sheets, with the inner frame rule at 5px; inner tiles (outcome blocks, code blocks, diagrams, medallions) at 8px (`--radius`); small elements at 6px (`--radius-sm`). **Stamps (3px):** the squared registry marks — badges, the bronze metric chip, stack tags — data stamped flat, against rounded controls. Timeline node dots are circles (14px, `border-radius: 50%`).

The frame language is the signature: every sheet carries the banknote border — a 1px `--sheet-line` edge, then the inner rule (`::before`, inset 7px, 5px radius), then the four corner quarter-dots (`::after`, 2.4px `--ink-faint` discs seated on the inner rule's corners). Double rules recur at every hierarchy beat: the header band's bottom edge, the plate title's top edge (1px rule plus a second 3px below), the denomination's inset ring (inset shadows at 4px/5px), the medallion's inner ring (inset 3px sheet-solid, 4px bronze). Dashed 1px `--line` hairlines separate education and certification entries and mark disclosed tails. Focus is a 2px `--accent-bright` outline, offset 3px, 2px radius, on `:focus-visible` only.

## Components

### Buttons — the seal and the ruled ghost
- **Shape:** capsule (999px), min-height 44px (2.75rem) — the tap floor; mono uppercase tracked labels (0.78rem, 0.07em).
- **Primary (the intaglio seal):** `--action-bg` fill, `--action-ink` text, a 1px inset cream ring (`rgba(246,241,226,.32)`) inside the border — the engraved stamp's bevel — plus `--shadow-float`. Hover deepens to `--action-bg-hover`, lifts 1px, takes `--shadow-lift`; `:active` returns.
- **Ghost (the ruled ghost):** `--sheet-solid` face, `--edge-silver` border, ink text. Hover takes the accent border and accent text. The PDF link is `target="_blank"` so Blazor's router never claims it.
- **Motion:** transitions at .18s; hover lifts on `transform: translateY(-1px)`.

### Chips — cited seals
- **Style:** small pills (0.88rem Spectral, 0.28rem 0.8rem padding) bordered `--sheet-line`, `--sheet-bg` fill, ink-soft text — scannable objects, not list rows.
- **Evidenced variant:** `--accent-wash` fill, accent border, ink at 600 — an evidenced skill outranks an unevidenced one; each carries its backing employer in `--chip__where` mono (0.62rem, Ink Faint).
- **Hover:** lift 1px, accent border, `--shadow-lift`. A chip never widens the page (`max-width: 100%`).
- **Bronze metric chip:** the squared 3px stamp (mono 0.7rem, tabular) inline after an award-earning achievement — the only warm mark in running text.

### Header Band & Navigation
Opaque `--paper` band, sticky, z-40, closed by a double rule (border + inset shadow). Wordmark left in Bodoni 600 1.08rem; nav links are tracked mono caps (0.72rem, 0.1em) in ink-soft, hovering to ink on a 8% ink wash; the current section takes the green seal (`.is-current`: `--action-bg` fill, `--action-ink` text) — scroll state set by `motion.js`, additive like every marker. Below 721px the nav becomes a horizontal scroll strip on row two of the band (hidden scrollbar); below 430px the labels tighten so nothing clips. The markup is mirrored byte-for-byte by `_tools/prerender.py`'s `static_shell_header` — change them together. The Testimonials link renders only while a real quote exists.

### Theme Toggle — the medallion switch
Same proven mechanics as the previous world, restruck in new metal: a 46×26 track (ink at 14%, brass hairline, inset shadow) in a 44px button; the 20px knob is aged brass in light (`#f8f3e6→#d9cdb0`) and green-black in dark (`#35473b→#1b2a21`), travelling by `transform` for the old-WebView review browser; knob side and sun/moon glyph are pure CSS state written twice (guarded `prefers-color-scheme` and `[data-theme="dark"]`), so control and palette can never disagree. Tap toggles; drag past the midpoint commits through `el.click()` so Blazor's aria stays in sync; commits fire the one-shot inside-out ground pulse (`PULSE_GROUNDS`, WAAPI, outside `#app`) and View Transitions cross-dissolve the swap where supported. Reduced motion: instant swap, no pulse. The static shell mirrors the switch (`data-static-theme-toggle`) and theming works with JavaScript disabled.

### Contact Dock — the seal strip
One opaque capsule (`--sheet-solid`, `--edge-silver` rim, `--shadow-float`) fixed bottom-right — Call and Email as plain anchors (`tel:` digits-only href from `Profile.PhoneHref`, number never printed as text; `mailto:` from the profile email), mono caps 0.72rem, 44px hit floors, hover taking accent on an 8% ink wash. Centred in the thumb zone ≤720px, safe-area aware; mobile-only, it stays hidden behind `.js-motion` until first movement (see The Dock Clear-Zone Rule) and reduced-motion/no-JS visitors always have it. Mirrored by `prerender.py`'s `static_contact_dock`; `display: none` in print.

### Back-to-Top
A real 44px circular `<button aria-label="Back to top">`, parked above the dock (`bottom: calc(3.6rem + safe-area + 4.2rem)`, z-39 under the dock's 40). Solid face, brass rim, float shadow; `display: none` at rest, `motion.js`'s `.is-shown` past one viewport of scroll. Hover: accent border and glyph, `--shadow-lift`. Click smooth-scrolls to top — instant under reduced motion. Runtime chrome with no static-shell copy on purpose; the footer's `#main` link is the no-script path. Hidden in print.

### The Denomination (signature)
The hero's note face, left column: an inset plate (`--radius` 8px, inner ring via inset shadows, one quiet `--accent-wash` wash at 30% 15%) holding an SVG "9" — Bodoni at font-size 250 in a 220×260 viewBox, printed three times: a faint solid underlay (accent at 17% opacity) that keeps the hairline strokes inked, the engine-turned interlace fill (a 12×7 tile of two counterphased sine waves, stroke 1, opacities .9/.55 — the field reads as woven curves, never a straight hatch), and the fine diagonal hatch (3×3 tile, rotated −45°, stroke .7 at .45). Under it, the serial plate: three mono lines at 0.56rem/0.14em — `PLATE NO. 9 · 7 · 491`, `9 MARKETS · 7 GATEWAYS · 491 TESTS`, `ALEXANDRIA · EET · BUILT ALONE` — every figure real. The print-in plays once (see Motion), guarded; the SVG re-inks with the theme because its patterns stroke `var(--accent)`.

### Plate Frames & Case Sections
Five case studies live inside one work sheet as **flat hairline-separated sections** — no cards in a card, no accent rails, no hover lift on a section the reader is not navigating to. The one tinted moment is the outcome block (`--accent-wash`, 8px radius): what actually changed is where a skim stops. The home case index is hairline rows, not cards — title (Bodoni 1.16rem), org line (tracked mono caps), one-line summary, outcome chip on `--accent-wash`; two-up on wide screens.

### Timeline
A 2px rail (`--line`) with 14px node dots — paper fill, 2px accent border, z-lifted above the spine so the dot is never bisected. The accent spine draws down entry by entry on reveal (`draw-y` .85s, `calc(var(--i) * 130ms + 120ms)`); without the script it is simply already drawn. The current role's node is the only thing still moving (2.6s pulse in the accent). Badges: "Now" in accent-bright, "Returned" in accent wash — both accent, never bronze (The Bronze Is Recognition-Only Rule). The stack byline under the company line is mono Ink Faint, derived from the role's own record.

### Medallions & Credentials
Award tiles are struck as medallions: `--gold-wash` face, bronze border, and the inner ring (inset 3px `--sheet-solid`, 4px `--gold`) — banknote border language in bronze; the Bodoni title in bronze. Education and certifications separate by dashed hairlines; the five certs that also appear on the printed CV are weighted up and carry the accent "on CV" pill. Certifications balance into two columns ≥940px, featured set flowing first, entries never splitting.

### System Surfaces
Selection tinted 26% accent; caret accent; a 12px rounded scrollbar thumb in brass on paper. `#blazor-error-ui` is hidden until a real runtime error, then a full-width bronze-wash bar (`--gold-wash` face, ink text) — the fake crash report above the fold of trust is fixed; the world's wash borrows bronze's ground without spending bronze ink. Diagram canvases and code blocks sit on `--wash` fills behind hairlines; the write-up's syntax colours are fixed hexes, twice-written for dark.

### Motion — the plate press
- **The print-in:** the denomination prints once — `denomination-print` 1s `cubic-bezier(.16, 1, .3, 1)` (soft clip wipe, `inset(6% 2%)` → 0, with opacity), the legend settling in after (`legend-settle` .7s, rise 8px, beats at 0/.18s/.3s/.42s). It runs only under `.js-motion .hero.is-playing`, which `motion.js` arms only on a proved first look: not scrolled past the threshold, not played this session (`sessionStorage.heroPlayed`), booted within the deadline. Any miss means never armed — the note renders fully printed, never armed-but-invisible.
- **Reveals:** sections settle from visible — rise 10px, .6s `cubic-bezier(.22, .8, .3, 1)`, 55ms per index — every hiding rule behind `.js-motion` from `motion.js` and nowhere else.
- **Reduced motion:** every hidden state restored in app.css's reduced-motion block plus Hero.razor.css's own; animations collapsed to .01ms; the note is simply printed.

## Do's and Don'ts

### Do:
- **Do** write any dark token change in both places — the guarded `prefers-color-scheme` block and the `[data-theme="dark"]` rule, byte-identical (The Twice-Written Rule).
- **Do** keep bronze on recognition only — medallions, award metric chips, the award figure; "Now"/"Returned" badges take the accent (The Bronze Is Recognition-Only Rule).
- **Do** keep every surface opaque: fixed chrome is paper under a brass hairline; `--glass-*` stays resolved flat; if a style asks for blur, it is a bug (The No-Blur Rule).
- **Do** frame new content plates with the banknote border — inner rule inset 7px plus the corner quarter-dots — and put plate titles under a double rule.
- **Do** gate every hiding rule behind `.js-motion` from motion.js, restore every hidden state in the reduced-motion and print blocks, and arm the print-in only through the proved first-look guard.
- **Do** keep the prerendered `<div class="prerendered">` a direct child of `#app`, mirror header/dock changes in `prerender.py` (`static_shell_header` / `static_contact_dock`), and carry final values in markup for anything a script counts.
- **Do** keep 44px tap floors on buttons, dock actions, and the toggle; keep figures in Fragment Mono with `tabular-nums`, real and derived only.
- **Do** verify both themes at 390×844 and desktop width before calling anything done.

### Don't:
- **Don't** put kickers or eyebrows above headings, and don't add border-left accent stripes — both stay below the craft floor (The No-Kicker Rule stands in this world).
- **Don't** use `backdrop-filter`, frosted fills, or `color-mix()`-dependent tints without a solid fallback — the review browser is an old Edge WebView, and this world is flat ink by doctrine.
- **Don't** put anything animated or tinted behind the content — the ground is one flat, still surface (the still-ground rule).
- **Don't** spend bronze on navigation, action, links, badges, or decoration — and don't spend the accent's green on recognition; each metal has one subject.
- **Don't** invent a figure: no fabricated serials, no invented quotes (testimonials render only from real, attributed submissions in `testimonials.json`), no un-derived numbers on the note.
- **Don't** rebuild the before/after diagram — it was deleted at the user's word; the payment argument lives in the flagship case study.
- **Don't** print the design: header band, dock, back-to-top, and cv-actions drop out in print, below-fold reveals force-restore, and the printed CV (`/cv` document, `PrintCv.razor.css`, EmptyLayout) stays deliberately ATS-plain outside this system — only its on-page chrome wears the world.
- **Don't** print the phone number as visible text on the showcase — it travels in the dock's `tel:` href only.
