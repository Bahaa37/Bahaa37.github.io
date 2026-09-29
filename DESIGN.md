---
name: The Annual Report — Ledger Green
description: The career presented as an audited annual report — a strict grid, ruled key-figures, masthead-scale grotesk, and one ledger-green accent on rag paper.
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
  line: "rgba(20, 38, 30, .16)"
  edge-silver: "#b8ab8c"
  glass-bg: "var(--sheet-solid)"
  glass-line: "var(--edge-silver)"
  pill-line: "rgba(20, 38, 30, .24)"
  pill-bg: "rgba(255, 252, 242, .7)"
  wash: "rgba(20, 38, 30, .05)"
  # Values above are the LIGHT canon. Dark values are equally canonical and live in
  # src/Cv.Web/wwwroot/css/app.css, written TWICE (the prefers-color-scheme block
  # guarded by :not([data-theme="light"]), and the :root[data-theme="dark"] rule).
  # .impeccable/design.json carries darkCanonical per color.
typography:
  display:
    fontFamily: "Archivo, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(2.7rem, 1.4rem + 6vw, 6rem)"
    fontWeight: 860
    fontStretch: "116%"
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Archivo, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(1.55rem, 1.1rem + 2.1vw, 2.35rem)"
    fontWeight: 750
    fontStretch: "110%"
    lineHeight: 1.06
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Archivo, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(1.55rem, 1.1rem + 2.1vw, 2.35rem)"
    fontWeight: 750
    lineHeight: 1.06
  body:
    fontFamily: "Spectral, Georgia, 'Times New Roman', serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.62
  small:
    fontFamily: "Spectral, Georgia, 'Times New Roman', serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.55
  meta:
    fontFamily: "Fragment Mono, ui-monospace, 'Cascadia Mono', Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Fragment Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "0.72rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.1em"
    textTransform: "uppercase"
  micro:
    fontFamily: "Fragment Mono, ui-monospace, monospace"
    fontSize: "0.64rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.1em"
    textTransform: "uppercase"
rounded:
  pill: "999px"
  sheet: "10px"
  md: "8px"
  sm: "6px"
  stamp: "3px"
spacing:
  gutter: "1.25rem"
  stack: "1.6rem"
  measure: "66ch"
  page: "1120px"
components:
  button-primary:
    backgroundColor: "{colors.action-bg}"
    textColor: "{colors.action-ink}"
    rounded: "{rounded.pill}"
    padding: "0.55rem 1.3rem"
    height: "44px"
    typography: "0.78rem Fragment Mono, uppercase, letter-spacing .07em"
  button-ghost:
    backgroundColor: "{colors.sheet-solid}"
    textColor: "{colors.ink}"
    borderColor: "{colors.edge-silver}"
    rounded: "{rounded.pill}"
    padding: "0.55rem 1.3rem"
    height: "44px"
  chip:
    backgroundColor: "{colors.sheet-bg}"
    textColor: "{colors.ink-soft}"
    borderColor: "{colors.sheet-line}"
    rounded: "{rounded.pill}"
    height: "32px"
  chip-evidenced:
    backgroundColor: "{colors.accent-wash}"
    textColor: "{colors.ink}"
    borderColor: "{colors.accent}"
    fontWeight: 600
  metric-chip:
    backgroundColor: "{colors.gold-wash}"
    textColor: "{colors.gold}"
    borderColor: "{colors.gold}"
    rounded: "{rounded.stamp}"
    typography: "0.7rem Fragment Mono, tabular numerals"
  key-figures-strip:
    layout: "auto-fit grid, min 9.5rem columns"
    ruleTop: "1px solid {colors.ink}"
    ruleBottom: "1px solid {colors.line}"
    columnRule: "1px solid {colors.line}"
    figureTypography: "1.35rem Fragment Mono, tabular numerals"
    labelTypography: "0.68rem Fragment Mono, {colors.ink-faint}"
  header-band:
    backgroundColor: "{colors.paper}"
    borderBottom: "1px solid {colors.line} + inset double rule"
    wordmark: "Archivo 800 uppercase 1.02rem"
---

# Design System: The Annual Report — Ledger Green

## Overview

**Creative North Star: "The Annual Report"** — Ledger Green revision (2026-09-27, user-pinned after recruiter feedback on the Legal Tender banknote world; the roll's originally assigned direction, seed key `aaa7f143` lineage).

The career is presented as an **audited annual report**: the grid is the authority, every figure carries its source, and the masthead claims the viewport. The hero is a report masthead — *"Nine countries. One gateway. Built alone."* set in Archivo Expanded Black — over the **ruled key-figures strip**, a tabular row under a heavy ink rule (9 markets · 3-day cycle · 3.5+ years · 2 awards), every figure derived from the case-study record by `Hero.razor`'s anchor-phrase extraction, never typed into markup. Content floats as report sections on rag paper; every section opens under a heavy ink rule; the hero facts sit in a ruled table row.

The discipline laws, carried and enforced: **no backdrop-filter anywhere** (the inherited `--glass-*` tokens resolve flat — a hairline, `0px`, `none`; intaglio restraint survived the world change); **nothing animated behind the content** (the still-ground rule); **hiding is additive-only** behind `.js-motion` from `js/motion.js`; **bronze marks recognition only** (award medallions and the awarded metric chip — never timeline badges, never decoration); **the No-Kicker Rule stands** (nothing above a heading; the deck line is a byline beneath the masthead); **dark tokens are written twice** (the guarded `prefers-color-scheme` block and the `[data-theme="dark"]` rule).

**Key Characteristics:**

- Rag-paper light (`#f3eede` — kept from the previous world by the user's choice) / intaglio-plate dark (`#0d1712`, green-black — not gray).
- One accent: ledger green, owning action, links, focus, and the masthead's accent line. Bronze is the medallion metal.
- Archivo (weights 100–900, width axis) is the report voice: masthead at Expanded Black, section titles at 750/110%; Spectral carries document prose; Fragment Mono carries every figure in tabular numerals.
- Sheets are solid paper faces with a 3px ink bar at the head; section titles sit under a 3px ink rule. No inner frames, no rosettes — the banknote's ornament retired with its world.
- Registry styling for data: squared 3px stamps for metrics and badges, mono caps for labels, ruled rows for the case index.
- Reduced motion restores every hidden state; the printed CV stays ATS-plain outside this system.

## Colors

Cool, machined, financial: green-black ink steps on rag paper or an intaglio plate, one ledger green, bronze spent on recognition alone.

### Primary
- **Action Green** (`--accent` #0c5a45 / dark #4ba583; `--action-bg` #0c5a45 light, #2e7d5f dark with `--action-ink` #f6f1e2/#f2eede): links, focus, the masthead accent line, and the seal button. Split fill/link as before (AA on both grounds).
- **Ink** (`--ink` #14261e / dark #e6dcc2 aged cream): headings and primary text. **Ink Soft** (#3d5347 / #c0bda3): prose. **Ink Faint** (#5d7263 / #9a9574): the smallest text, held ≥4.5:1 on its face.
- **Grounds**: rag paper `--paper` #f3eede (light) / intaglio plate #0d1712 (dark); sheet faces `--sheet-solid` #faf6ea / #122019.

### Secondary
- **Bronze** (`--gold` #7a4a2b / dark #c98a4b, `--gold-wash`): **The Bronze Is Recognition-Only Rule** — award medallions (border + inset inner ring) and the awarded metric chip. Timeline badges take the accent, never bronze.
- **Wash** (`--accent-wash` #e4e9d6 / #182b22): evidenced chips, outcome blocks, avatars, the "Current"/"Returned" badges.
- **Alarm** (`--alarm`): reserved; carries no current consumer (documented reserve).

### Neutral
- Hairlines `--line`; the brass edge `--edge-silver` (#b8ab8c / #56685a) borders chrome; `--wash` is the neutral tint fill.
- **The No-Blur Rule:** `--glass-bg` resolves to the sheet face, `--glass-blur` is `0px`, `--glass-highlight` is `none`. Any new chrome asking for glass is refused — this world's ink is flat.

### Permitted derivatives
Alpha tints of documented hues, `color-mix()`-free (the user's review browser lacks it — solid rgba fallbacks only), and ink-derived shadow colors are accepted without entries. New hues require a palette entry.

### Named Rules
**The Bronze Is Recognition-Only Rule.** Bronze on medallions and the awarded metric; nowhere else.
**The Twice-Written Rule.** Dark tokens live in both the guarded `prefers-color-scheme` block and the `[data-theme="dark"]` rule; change both, always.
**The Serials Rule.** Every figure on the page is real and derived, never typed. An audited report with an invented figure is fraudulent.

## Typography

**Display Font:** Archivo (variable: wght 100–900, wdth 62–125; masthead sets 860 at 116% width)
**Body Font:** Spectral (document prose)
**Label/Mono Font:** Fragment Mono (figures, labels, serials — tabular numerals everywhere)

Loaded non-blocking from Google Fonts (`display=swap`, print-media swap-onload); the font stylesheet never delays first paint.

### Hierarchy
- **Display** (860, Expanded 116%, clamp(2.7rem, 1.4rem + 6vw, 6rem), 0.98, −0.035em): the masthead statement only; four lines, the middle line in the accent.
- **Headline** (750, Expanded 110%, clamp(1.55rem, 1.1rem + 2.1vw, 2.35rem), −0.025em): section titles, each under the 3px ink rule.
- **Body** (Spectral 400, 16px, 1.62): prose, capped at the 66ch measure; ledes 1.02rem in Ink Soft.
- **Meta** (Fragment Mono, 0.78–0.88rem, tabular numerals): key figures, attributions, dates — always Ink Faint unless the figure is the subject.
- **Label** (Fragment Mono caps, 0.72rem, +0.1em): group titles (Accent), group headers, nav.

### Named Rules
**The No-Kicker Rule.** Nothing above a heading. The masthead's deck line ("Built alone · End to end", tracked mono caps) sits *beneath* the statement as a byline.

## Layout

Single 1120px column (`--page`), 1.25rem gutters; the hero sheet runs wider (`--page + 5rem`) so the masthead breathes. Content sections are solid sheets stacked 1.6rem apart, padded `clamp(1.8rem, 1.2rem + 3vw, 3.4rem)` / `clamp(1.3rem, 3.5vw, 3rem)`, each carrying the 3px ink bar at its head. Inner grids: `repeat(auto-fit, minmax(300px, 1fr))` (skill groups, contact facts, awards), the key-figures strip `minmax(9.5rem, 1fr)`.

Breakpoints:
- **430px**: the nav strip tightens (smaller pads, .64rem) so all five links — CV last — fit a 390px screen without clipping.
- **720px**: header capsule wraps to two rows (name+toggle / nav strip, ~98px — scroll-margin follows at `--header-band + 1rem`); figures strip goes 2-up with dashed inner rules; hero gains a bottom clear zone for the fixed dock.
- **900px**: hero figures grid adjusts; masthead steps down.

Anchor navigation compensated: `.sheet[id]`, `.case[id]` carry scroll-margin-top tokens tied to `--header-band`.

## Elevation & Depth

Depth is the flat ground under floating paper: the three-stage shadow (`--shadow-sheet`) on plates, `--shadow-float` on chrome, `--shadow-lift` as the hover response. No colored halos, no blur, nothing layered behind the content. The reading-progress bar (2px accent, `animation-timeline: scroll()`, inside `@supports`) survives as the report's ruled margin-line.

## Shapes

Capsules (999px) for all interactive controls; sheets at 10px; tiles at 8px; **registry stamps at 3px** (metric chips, badges — data, not action). Focus is a 2px `--accent-bright` outline, offset 3px, on `:focus-visible` only. Selection tinted accent; scrollbar and caret themed.

## Components

### Buttons
- **Seal (primary):** action-green fill, paper-cream label in mono caps, an inset paper hairline (`inset 0 0 0 1px rgba(246,241,226,.32)`) giving the intaglio edge; hover deepens + lifts 1px.
- **Ghost:** paper face, brass border; hover takes accent border/text + lift.

### Header Band
Opaque paper, sticky, `border-bottom` + inset second rule (the double rule). Wordmark in Archivo 800 caps; nav links are mono-caps 44px taps; the current section wears the green seal. The theme toggle is the 46×26 medallion switch (knob: polished paper in light, deep plate-green in dark; exactly one glyph per state). Markup mirrored byte-for-byte by `prerender.py`'s `static_shell_header`.

### Key-Figures Strip
The hero's ruled table row: heavy ink rule above, hairline below, column hairlines between; figures in 1.35rem tabular mono over registry labels; the awarded figure in bronze. Count-ups animate damped from markup-carried finals.

### Scroll-Spy & Motion
`motion.js` owns every hiding class. Reveals rise 10px and settle (55ms stagger); the masthead settle plays once under the existing never-replay guard (`sessionStorage.heroPlayed`, scroll threshold, boot deadline) — static under reduced motion, on replay, and for late boots. The mobile dock reveals only after 160px of scroll (`.is-shown` from `initDockReveal`), gated behind `.js-motion`, restored always-on under reduced motion. Scroll-spy is state (runs regardless of reduced motion).

### Contact Dock & Back-to-Top
The dock: opaque seal strip, fixed bottom-right (centred ≤720px), `tel:`/`mailto:` anchors, phone never printed as text. Back-to-top: 44px paper circle above the dock's baseline. Both `display:none` in print. The dock markup is mirrored by `prerender.py`'s `static_contact_dock` — change together.

### Timeline
The rail + draw-y accent spine + node dots carried over, token-driven; the current role's node pulses (damped, 2.6s); "Current" takes the accent seal, "Returned" the accent wash (bronze refused).

### Case Sections & Index
The featured study tells problem→approach→outcome with the outcome block in accent wash; the index is **ruled registry rows** — Archivo 750 titles left, org/summary/registry-line outcome right — full-width at every breakpoint (the scoped `Home.razor.css` grid that collapsed the 800px columns was removed; app.css owns these rows).

### Awards, Education, Certifications
Medallions: bronze border + inset inner ring on the wash face. Education and certifications separate by dashed hairlines; featured certs carry the "on CV" stamp.

### Browser Surfaces
Selection tinted accent, caret accent, themed scrollbar, `:focus-visible` ring — the report is themed past its own edges.

## Do's and Don'ts

### Do:
- **Do** write dark tokens twice; verify both themes at 390×844 and desktop before calling anything done.
- **Do** gate every hiding rule behind `.js-motion`; restore all states under reduced motion and print.
- **Do** derive hero figures from the case-study record (`Hero.razor` anchor extraction) — the Serials Rule.
- **Do** keep bronze recognition-only, green the only accent, mono for every figure.
- **Do** mirror header/dock changes in `prerender.py` (`static_shell_header` / `static_contact_dock`) and keep the prerendered div a direct child of `#app`.
- **Do** keep the font stylesheet non-blocking and figures in tabular numerals.

### Don't:
- **Don't** reintroduce blur, guilloche/engraving devices, plate frames, rosettes, or denomination scales — they belong to the retired world and the user rejected them.
- **Don't** add kickers/eyebrows above headings or border-left accent stripes (The No-Kicker Rule; craft floor).
- **Don't** use `color-mix()` or the individual `translate` property (the user's review browser lacks both) — transform + solid fallbacks.
- **Don't** build a stat-card band — the facts are the ruled strip.
- **Don't** clip the nav: below 430px the labels tighten so CV never leaves the strip.
- **Don't** print the design: chrome drops out, reveals restore, the printed CV stays ATS-plain by product rule.
