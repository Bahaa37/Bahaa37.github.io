---
name: Frosted Keynote — Bahaa Aldeen Mohamed
description: A native-app portfolio — frosted glass chrome and anodized-silver metal edges over solid content sheets on one still Sky Aluminum ground.
colors:
  ink: "#16222e"
  ink-soft: "#44586b"
  ink-faint: "#5c7086"
  paper: "#e8f2ff"
  sheet-bg: "rgba(255, 255, 255, .88)"
  sheet-solid: "#fdfeff"
  sheet-line: "rgba(22, 34, 46, .1)"
  accent: "#0e6398"
  accent-bright: "#0071e3"
  accent-wash: "#e3f1fa"
  action-bg: "#0066cc"
  action-bg-hover: "#0059b3"
  action-ink: "#ffffff"
  gold: "#8a6116"
  gold-wash: "#fbf3e2"
  alarm: "#b0432c"
  alarm-wash: "#fbeae6"
  stage-legacy: "#9aa8b6"
  stage-lead: "#7fc4ff"
  edge-metal: "linear-gradient(135deg, #ffffff, #b9c6d3 38%, #8ea1b2 52%, #c9d5e0 78%, #eef3f8)"
  edge-silver: "#b3c1ce"
  glass-bg: "rgba(255, 255, 255, .58)"
  glass-line: "rgba(255, 255, 255, .75)"
  pill-line: "rgba(22, 34, 46, .24)"
  pill-bg: "rgba(255, 255, 255, .7)"
  line: "rgba(22, 34, 46, .12)"
  # Values above are the LIGHT canon. Dark values are equally canonical and live in
  # src/Cv.Web/wwwroot/css/app.css, written TWICE (the prefers-color-scheme block
  # guarded by :not([data-theme="light"]), and the :root[data-theme="dark"] rule).
  # .impeccable/design.json carries darkCanonical per color.
typography:
  display:
    fontFamily: "Geist, 'Segoe UI', system-ui, sans-serif"
    fontSize: "clamp(2.4rem, 1.1rem + 5.2vw, 4.6rem)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Geist, 'Segoe UI', system-ui, sans-serif"
    fontSize: "clamp(1.85rem, 1.15rem + 2.6vw, 2.9rem)"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-0.028em"
  title:
    fontFamily: "Geist, 'Segoe UI', system-ui, sans-serif"
    fontSize: "clamp(1.9rem, 1.3rem + 3vw, 3rem)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  body:
    fontFamily: "Geist, 'Segoe UI', system-ui, -apple-system, Helvetica, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  small:
    fontFamily: "Geist, 'Segoe UI', system-ui, -apple-system, Helvetica, sans-serif"
    fontSize: "0.94rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  meta:
    fontFamily: "Geist, 'Segoe UI', system-ui, -apple-system, Helvetica, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Geist Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "0.74rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.08em"
  micro:
    fontFamily: "Geist Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "0.68rem"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.05em"
rounded:
  pill: "999px"
  sheet: "16px"
  stage: "14px"
  md: "12px"
  sm: "8px"
  node: "6px"
spacing:
  gutter: "1.25rem"
  stack: "1.4rem"
  measure: "68ch"
  page: "1160px"
components:
  button-primary:
    backgroundColor: "{colors.action-bg}"
    textColor: "{colors.action-ink}"
    rounded: "{rounded.pill}"
    padding: "0.6rem 1.35rem"
    height: "44px"
    typography: "0.95rem Geist, weight 600"
  button-primary-hover:
    backgroundColor: "{colors.action-bg-hover}"
  button-ghost:
    backgroundColor: "{colors.pill-bg}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.6rem 1.35rem"
    height: "44px"
    typography: "0.95rem Geist, weight 600"
  chip:
    backgroundColor: "color-mix(in srgb, {colors.sheet-bg} 80%, transparent)"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.pill}"
    padding: "0.3rem 0.85rem"
    height: "32px"
    typography: "0.88rem Geist, weight 400"
  chip-evidenced:
    backgroundColor: "{colors.accent-wash}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    typography: "0.88rem Geist, weight 600"
  metric-chip:
    backgroundColor: "{colors.gold-wash}"
    textColor: "{colors.gold}"
    rounded: "{rounded.sm}"
    padding: "0.12rem 0.55rem"
    typography: "0.85rem Geist, weight 700"
  header-capsule:
    backgroundColor: "{colors.glass-bg}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    height: "56px"
  theme-toggle:
    kind: "iOS-style switch (role=switch)"
    track: "46x26px pill, ink at 12-20% + hairline; inset shadow"
    knob: "20px polished-aluminum circle (white->#d9e3ec; dark #c7d5e2->#8fa3b5), 12px sun/moon glyph"
    hitArea: "44px min (button wraps the track)"
    states: "knob left + sun = light; knob right + moon = dark — pure CSS state"
    interaction: "tap toggles; drag knob past midpoint switches (shell enhancement); ArrowLeft/Right set a theme"
  contact-dock:
    backgroundColor: "{colors.dock-bg}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.pill}"
    height: "44px per action"
    position: "fixed; bottom-right desktop, bottom-centre ≤720px"
  testimonial-tile:
    backgroundColor: "color-mix(in srgb, {colors.sheet-bg} 70%, {colors.paper})"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "1.5rem 1.5rem 1.25rem"
  award-tile:
    backgroundColor: "{colors.gold-wash}"
    textColor: "{colors.gold}"
    rounded: "{rounded.md}"
    padding: "1.1rem 1.2rem"
---

# Design System: Frosted Keynote

## Overview

**Creative North Star: "Frosted Keynote"** — Sky Aluminum revision (2026-09-13, third re-tint, user-proposed).

The site behaves like a native Apple app: frosted glass for chrome, near-opaque rounded content sheets carrying every dense word, and one still ground behind everything. Direction chosen on the impeccable decision page (answer: model-pick, code-led; seed key `d60cb62c`), first shipped 2026-09-12, re-tinted three times on 2026-09-13: the drifting aurora died first (generated decor), neutral graphite died the same morning (correct but generic), Terminal Green by afternoon (the user's pick from four, rejected on review). The user then proposed the surviving direction themselves: **Sky Aluminum** — Apple's anodized baby-blue aluminum as a design language. Glacier light (#E8F2FF — Apple's iPhone 18 Pro baby blue, exact), blue-slate night (#0D141D), steel-blue ink steps, Apple's own action blue (#0066CC light; #0A84FF with near-black ink in dark, exactly as iOS does it), and the material story the user asked for by name: **anodized-silver gradient edges** (1px border-box gradient composites) on every sheet and the study slab, silver rims on the frosted glass chrome, and gold metal reserved for awards alone — silver everywhere, gold only where recognition is the subject. The diagram stage stays a dark blue-charcoal panel where silver-steel (`--stage-legacy`) marks the legacy estate and sky (`--stage-lead`) marks what replaced it. Sections separate by value, nothing behind the content moves, and the world proves the candidate engineers calm — it refuses the category-default scrolling document and its sticky stat band.

The dosage law governs everything: **glass is chrome, sheets are solid.** `backdrop-filter` is spent exactly twice, on fixed chrome the size of a matchbox — the header capsule and the contact dock; content sheets never blur (`--sheet-solid` faces), so a 6000px page never holds a live GPU blur under the reader and first paint stays under a second — a product rule, not a preference. Depth comes from the three-stage blue-cast sheet shadow and the anodized metal edges over one flat ground, never from layer effects on content or anything moving behind it.

Motion is one orchestrated system on a shared ease-out clock (`cubic-bezier(.16, 1, .3, 1)`): sections settle in as sheets (rise 26px + settle from an already-visible default), items stagger at 50ms per index, and the hero plays a single ~2.6s sequence — but only for qualifying visits (see Components). Hiding is additive-only: every hiding rule is gated behind `.js-motion`, added by `js/motion.js` and nowhere else, so a script failure can never leave content invisible. Reveals animate the individual `translate`/`scale` properties, never `transform` — transform is reserved for hover lifts so the two compose cleanly.

The interface's voice is first-person, precise, engineering-grade: labels are quiet Geist Mono uppercase, attribution reads as a byline under a title (never a label above it), and verified metrics are woven into sentences in tabular mono numerals instead of card grids. Nothing decorative is asserted as fact — no invented numbers, no invented quotes.

**Key Characteristics:**

- Still ground: one flat neutral surface on `html` — nothing layered, nothing animated behind the content, zero backdrop elements to survive the boot boundary.
- Frosted capsule header is the only real glass; sheets are translucent-without-blur slabs (16px radius).
- One blue accent for action, links, and focus; gold spent on exactly one subject (awards); alarm red only for the diagram's blocker; stage hues live only inside the hero diagram stage.
- Geist + Geist Mono; negative tracking on every heading; mono carries all data and labels.
- Capsule radii (999px) for all interactive chrome; hairlines, not boxes, separate content inside a sheet.
- Reduced motion restores every hidden state; the printed CV sits outside this system entirely (ATS-plain by product rule).

## Colors

Cool, machined, precise: steel-blue ink steps on a silvery blue-paper light ground or a blue-slate night ground, Apple's own action blue, and single-use warm and alarm notes. The material story is hardware: anodized-silver metal edges frame the content; gold appears only where recognition is the subject.

### Primary
- **Action Blue** (`--accent` #0e6398 / `--action-bg` #0066cc light): links and text on sheets — split from the button fill because a fill and a text link need different contrast solutions; the fill carries white text at AA (5.6:1), the link sits on a white sheet at AA (6.4:1). `--action-bg-hover` #0059b3; `--accent-bright` #0071e3 — Apple's own blue — is the focus-ring and timeline-spine brightness; `--accent-wash` #e3f1fa — Apple's own Sky Blue finish token — tints evidenced chips, outcome blocks, and avatars. Dark: `--accent` #8ec7f2 (sky, links at 8.7:1), `--accent-bright` #b0d8f7, `--action-bg` #0a84ff with `--action-ink` #071018 — the exact iOS pattern: Apple's blue fill, near-black label, 5.3:1.
- **Selection** is the accent at a 26% mix; the reading-progress bar is solid accent.

### Secondary (stage-local)
- **Stage Legacy** (`--stage-legacy` #9aa8b6 light themes' stage steel / #8496a8 dark) and **Stage Lead** (`--stage-lead` #7fc4ff, sky): the only hues allowed inside the hero's recessed diagram stage. Silver-steel marks the legacy estate, sky marks what replaced it; the bridge gradient performs that transformation. The stage is dark blue-charcoal in both themes; nothing outside the stage uses either hue.

### Tertiary
- **Award Gold** (`--gold` #8a6116, `--gold-wash` #fbf3e2; dark #e0b95f / #2c2413): the one warm metal, spent on awards only — the hero's award fact, metric chips on award-earning achievements, award tiles, and the "returned" badge. In an aluminum world this is the gold watch against the steel: its scarcity is the point. Nowhere else.
- **Blocker Alarm** (`--alarm` #b0432c, `--alarm-wash` #fbeae6; dark #e5806a / #2c1a15): the diagram's blocker colour — dashed border, dissolving node, flag pulse. It earned its own token when it started animating; it does not generalize to "errors" elsewhere.

### Neutral
- **Ink** (`--ink` #16222e; dark #eef4fa): headings and primary text. **Ink Soft** (`--ink-soft` #44586b; dark #c2d0de): body prose and ledes. **Ink Faint** (`--ink-faint` #5c7086; dark #92a4b6): the smallest text — held at or above 4.5:1 on its sheet; every step is steel.
- **Glacier Ground** (`--paper` #e8f2ff — the exact `--finish` token of the iPhone 18 Pro's baby blue, taken from Apple's own published CSS, which uses these tokens for page backgrounds via `.finish-background`) / **Blue-Slate Ground** (`--paper` dark #0d141d): the html background — one flat, still surface; nothing glows over it. Supporting tints are Apple's own ship-alongs: #edf8ff, #e3f1fa (the wash), #dbf1ff.
- **Sheet** (`--sheet-solid` #fdfdfe; dark #192431 — the composite of the translucent `--sheet-bg` over the ground) with **Sheet Hairline** (`--sheet-line`): the content slab's face. Its *edge* is not a hairline but the anodized metal — see Materials.
- **Hairline** (`--line` rgba(22,34,46,.12); dark rgba(205,226,245,.11)): separators, node dots, quiet borders inside sheets.
- **Glass** (`--glass-bg` rgba(255,255,255,.58); dark rgba(17,25,35,.55)) with **Glass Edge** (`--glass-line`, silver-tinted) and the **inner top highlight** (`--glass-highlight`, an inset white line — the tell of real glass): chrome only.
- **Dock** (`--dock-bg` rgba(255,255,255,.6); dark rgba(20,29,40,.6)): the contact dock's frosted fill — it is the page's second and last blur, small and fixed.
- **Ghost Pill** (`--pill-line` rgba(22,34,46,.24); dark rgba(205,226,245,.18), `--pill-bg` rgba(255,255,255,.7); dark rgba(205,226,245,.06)): the on-sheet ghost treatment. Accepted: the light-theme edge composites under the strict WCAG 1.4.11 3:1 non-text boundary guideline by design; the text carries the meaning.

### Materials
- **The Anodized Edge** (`--edge-metal`; single-tone `--edge-silver`): a 1px gradient that reads as machined aluminum, applied to sheets and the study slab as a border-box gradient under a solid face (the padding-box/border-box composite — this is what lets a gradient border take a 16px radius). Dark theme runs the same sweep on dark aluminum (#3a4a5c → #93a7bb sheen → #3c4d60). Chrome that must stay translucent (capsule) takes the single-tone silver instead — a translucent face would let the gradient sheen through. **Gold metal is not in the edge system**: silver frames the content, gold marks awards.

### Named Rules
**The Gold Is Singular Rule.** Gold is spent on exactly one subject — the award metric — and nowhere else. Its rarity is what makes the award land.

**The Twice-Written Rule.** Dark tokens are written twice in `app.css` — inside `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]` — because plain CSS cannot share one declaration list between them without breaking the guard. Any token change is made in both places, always.

## Typography

**Display Font:** Geist (with "Segoe UI", system-ui fallback)
**Body Font:** Geist (with "Segoe UI", system-ui, -apple-system, Helvetica fallbacks)
**Label/Mono Font:** Geist Mono (with ui-monospace, SFMono-Regular, Menlo fallbacks)

**Character:** One geometric sans for voice, one mono for data. Geist carries every word of argument with tight negative tracking; Geist Mono carries every number, label, and machine-adjacent string, so "figures" look like figures. Loaded non-blocking from Google Fonts (`display=swap`, `media="print"` swap-onload) so the font stylesheet never delays first paint.

### Hierarchy
- **Display** (700, clamp(2.4rem, 1.1rem + 5.2vw, 4.6rem), 1.02, −0.04em): the hero headline only; each line sits in its own clipping box so it can unmask line by line.
- **Headline** (600, clamp(1.85rem, 1.15rem + 2.6vw, 2.9rem), 1.18, −0.028em): sheet section titles.
- **Title** (600, clamp(1.9rem, 1.3rem + 3vw, 3rem), 1.1, −0.03em): case-study page titles; long-form block headings step down to 1.35rem.
- **Body** (400, 16px, 1.6): all prose, capped at the 68ch measure; ledes at 1.05rem in Ink Soft.
- **Small** (400, 0.92–0.96rem, 1.5–1.65): card-level prose — timeline bullets, cert names, panel summaries. The floor for anything that reads as a sentence.
- **Meta** (mono or body, 400, 0.78–0.88rem): attributions, dates, issuers, bylines, the hero facts line (mono 0.86rem, strong values 1.06em, `font-variant-numeric: tabular-nums`) — always Ink Faint.
- **Label** (Geist Mono, 600, 0.68–0.78rem, uppercase, letter-spacing 0.08–0.12em): group titles, panel labels, breadcrumbs, prev/next markers. Group titles take Accent; everything else takes Ink Faint. Below 0.72rem is reserved for uppercase micro tags only.

### Named Rules
**The No-Kicker Rule.** Nothing sits above a heading — no kickers, no eyebrows, no numbered wayfinding. A section opens with its heading; attribution and bylines go below it, in mono, in Ink Faint.

## Layout

A single 1160px page column (`--page`) with 1.25rem gutters. Content floats as sheets: `width: min(100% - 1.5rem, var(--page))`, stacked 1.4rem apart, padded `clamp(2rem, 1.2rem + 3vw, 3.75rem)` block / `clamp(1.25rem, 3.5vw, 3.25rem)` inline. The hero sheet runs wider — `calc(var(--page) + 6rem)` — so the diagram and headline share one viewport at 1280–1536px. Long-form study sheets size to the prose (`--measure` 68ch + 14rem), because a 1160px line length is unreadable. Inner grids use `repeat(auto-fit, minmax(300px, 1fr))` (skill groups, case blocks, awards, testimonials, prev/next) so wrapping is intrinsic.

Breakpoints, and what changes at each:
- **640px**: testimonials grid drops to one column.
- **720px**: the header capsule keeps two rows *inside one capsule* — name + toggle on row one, the nav as a horizontal scroll strip on row two (nowrap, hidden scrollbar, faded right edge, snap points); radius eases 999px → 24px. **The Capsule Strip Rule:** the collapsed capsule is ~98px tall (compacted 2026-09-13 from ~118px — the row gap between name and nav strip was dead air), so the mobile `scroll-margin-top` is 112px (app.css, `max-width: 720px` block, `.sheet[id], .case[id]`). If the capsule is ever compacted or expanded, that 112px must move with it — the two are one decision.
- **900px**: the hero grid stacks; the diagram's three columns become one, bridge rotating from vertical to horizontal.
- **940px**: timeline entries gain a 10.5rem right-aligned period column; below it the period sits above the body with a tight 14px rail gutter (deliberate — a wide gutter pushed entries out of alignment with the section heading on phones).

Anchor navigation is compensated everywhere: `.sheet[id]` carries `scroll-margin-top: 92px` on desktop, `.case[id]` 96px, both overridden to 112px inside the 720px block.

## Elevation & Depth

Depth is one flat ground under floating slabs — never drop shadows on inline elements, never stacked card layers, nothing layered behind the content. The ground lives on `html` (`--paper`) as a plain colour; there is no backdrop element in the DOM at all, so the prerender fill and the Blazor boot have nothing to preserve.

**The still-ground rule:** nothing behind the content animates, ever. The previous revision's drifting aurora field was the one piece of decor the page carried, and it read as generated rather than authored — its removal is the re-tint's central decision. All movement lives inside the content (the hero sequence, the timeline spine) and all depth lives on the slabs themselves.

**Reading-progress bar:** a 2px fixed `body::before` in solid accent, driven by `animation-timeline: scroll()` — no script, no markup, compositor-only. Entirely inside `@supports`, so incapable browsers never draw it; hidden in print.

### Shadow Vocabulary
- **Sheet shadow** (`--shadow-sheet`: `0 1px 2px rgba(30,45,65,.05), 0 12px 32px rgba(30,45,65,.08), 0 32px 80px rgba(30,45,65,.08)`; dark: black-based): every content sheet — one crisp contact step, one mid lift, one wide blue-cast atmosphere.
- **Float shadow** (`--shadow-float`: `0 2px 6px rgba(30,45,65,.08), 0 12px 28px rgba(30,45,65,.12)`; dark: black-based): the header capsule, the diagram stage, and the contact dock.
- **Glass highlight** (`--glass-highlight`: `inset 0 1px 0 rgba(255,255,255,.45)`; dark .09): the inner top edge that says "real glass".
- **Hover lift** (`--shadow-lift`: `0 10px 24px rgba(30,45,65,.14)`; dark: black-based): the neutral response shadow under buttons, chips, and study links on hover. No coloured glow — emphasis comes from elevation, not from light. Shadows appear as a response to state, never at rest beyond the sheet/float vocabulary.

### Named Rules
**The Chrome-Only Blur Rule.** `backdrop-filter` (`saturate(180%) blur(20px)`) is spent on exactly two fixed chrome elements — the header capsule and the contact dock, each the size of a matchbox. Content sheets never blur: a blur under a long page is a GPU layer held alive the whole read, and render cost for nothing behind an opaque face. Any new fixed chrome may ask for glass; any content surface may not.

**The Scrolled-Depth Rule.** The capsule's glass deepens once content passes underneath — `.is-scrolled` (set by an inline script at scrollY > 8, rAF-throttled, surviving the Blazor boot boundary) mixes `--glass-bg` 72% into `--paper`. It is state, not motion, so it runs regardless of reduced-motion.

## Shapes

Two form families and a hairline. **Capsules:** anything interactive or chrome-like is a full pill (999px) — buttons, nav links, chips, badges, the header capsule, the skip link; the theme toggle is a 44px circle. **Slabs:** content containers round at 16px (`--radius-sheet`), the diagram stage at 14px, inner tiles (outcome blocks, study links, testimonials, awards, diagram canvases) at 12px (`--radius`), the gold metric chip at 8px (the one squared chip — it marks data, not action), diagram nodes at 6px. **Hairlines** do the separating inside sheets: 1px `--sheet-line` between flat case sections, `--line` under study headers and between prev/next, dashed `--line` between certifications. A dashed border is otherwise reserved for exactly one thing — the diagram's blocker node. Borders go quiet-to-accent on hover; nothing gains a border at rest that it did not have. Focus is a 2px `--accent-bright` outline, offset 3px, 4px radius, on `:focus-visible` only.

## Components

### Buttons
- **Shape:** capsule (999px), min-height 44px — the tap-target floor; padding (0.6rem 1.35rem) carries the size.
- **Primary:** `--action-bg` fill, `--action-ink` text, 0.95rem/600. Hover deepens to `--action-bg-hover`, lifts 1px, and takes the neutral `--shadow-lift`.
- **Ghost:** the on-sheet pill (`--pill-line` / `--pill-bg`), ink text, no blur — see The Chrome-Only Blur Rule. Hover takes the accent border and accent text.
- **Motion:** transitions at .22s, the shared ease-out on `translate`; `:active` returns to 0.

### Chips
- **Style:** small capsules (min-height 32px, 0.88rem) bordered `--sheet-line`, background `--sheet-bg` at 80% — scannable objects, not list rows.
- **Evidenced variant:** ink text at 600, `--accent-wash` fill, accent-mixed border — an evidenced skill outranks an unevidenced one; each carries its backing employer in `--chip__where` mono (0.72rem, Ink Faint).
- **Hover:** lift 1px, accent border, neutral `--shadow-lift`. A chip never widens the page (`max-width: 100%`).
- **Metric chip:** the gold 8px-radius chip inline after an achievement; the only warm mark in running text.

### Header Capsule & Navigation
The one piece of true glass: sticky header (no background of its own), inner capsule at min-height 56px, `--glass-bg`/`--glass-line`, float shadow + glass highlight, `backdrop-filter: var(--glass-blur)`, deepening on scroll (see Elevation). Wordmark left in Geist 600; the nav links (44px tap targets, quiet ink-soft, hover wash `color-mix(in srgb, var(--ink) 7%, transparent)`) and the theme toggle form **one cluster at the capsule's end** — the nav carries `margin-inline-start: auto`, so the toggle never strands at the far edge disconnected from the links it sits with. This markup is duplicated byte-for-byte by `_tools/prerender.py`'s `static_shell_header` so pre- and post-boot chrome cannot diverge — change them together. The Testimonials link renders only while a real quote exists; an empty `testimonials.json` ships no link.

### Theme Toggle — the drag switch
An iOS-style switch (the user's proposal, refined: tap first, drag second). The button wraps a 46×26 track and keeps the 44px tap floor; the knob is a 20px polished-aluminum circle carrying the 12px sun/moon glyph — knob left + sun is light, knob right + moon is dark, both decided by the same theme selectors that flip the palette, so control and colours can never disagree. **Tap toggles** (Blazor's handler after boot; the shell's delegated click before it; `role="switch"` with painted `aria-checked`; Space/Enter; ArrowLeft/Right set a theme directly). **Drag is enhancement, never the only path**: the shell's inline script pointer-captures the knob, pulls it toward the other theme (max 22px), commits on crossing the midpoint, and calls `preventDefault()` on a dragged release so the synthetic click cannot double-fire — `touch-action: none` is scoped to the control, so a thumb resting on it never holds page scroll. A MutationObserver re-binds the drag after Blazor replaces `#app`. Theme swaps run through `themeControl.set`, which uses **View Transitions** where supported — one GPU-composited ~250ms cross-dissolve of the page — and an atomic swap under reduced motion or without support; never a per-frame repaint. **The pulse** (the user's ask: the background answers the pin): while the knob drags, a disc of the *other* theme's ground grows inside-out from the switch in step with the drag — a live preview under the finger; on commit it pulses the rest of the way out and fades, on release below the midpoint it retreats back into the switch, and taps fire the same commit ripple. Transform + opacity only via WAAPI (`.theme-pulse`, one short-lived composited layer outside `#app`), never under reduced motion, hidden in print; its two colours are the `--paper` values and must move with them. The static shell mirrors the switch markup byte-for-byte (prerender.py) and theming works with JavaScript disabled entirely.

### Contact Dock
One frosted capsule fixed to the viewport's foot — Call and Email — present on every showcase page at every scroll position. Bottom-right on desktop, centred in the thumb zone at ≤720px, safe-area aware (`env(safe-area-inset-bottom)`), min-height 44px per action, drawn SVG icons in the theme toggle's stroke language (24px viewBox, currentColor, 1.6, round caps). It is the page's second blur (with the header capsule): true glass (`--dock-bg` + the glass blur) with a single-tone silver rim and the glass highlight — fixed chrome the size of a matchbox, never a page-length blur. Pure anchors, no script: `tel:` from `Profile.PhoneHref` (digits only, number never printed as text — the anti-scrape posture, updated 2026-09-13) and `mailto:` from the profile email. The markup is mirrored by `_tools/prerender.py`'s `static_contact_dock` — change them together — and the dock is `display: none` in print.

### Hero Sheet & Diagram Stage
The opening sheet: three-line display headline ("constraint" takes the accent — the one colour word), a 46ch pitch, then the track record as one mono facts line — never a stat-card band; figures carry their final values in the markup so the count-up can only ever be an enhancement. The before/after DTC diagram sits in a **recessed keynote stage**: dark blue-charcoal in *both* themes (`linear-gradient(180deg, #101a26, #0a0f16)` plus one quiet sky wash), 14px radius, lead-mixed border — one deliberate contrast moment, with every colour inside local to the stage (`--stage-legacy` silver-steel for the legacy estate, `--stage-lead` sky for what replaced it). Before-panel nodes build, the blocker is flagged (alarm ring at 1600ms) before the bridge line draws (1620ms) and the modernized services arrive; the blocker then dissolves to .26 opacity + grayscale.

**The never-replay guard.** The ~2.6s hero sequence plays only when motion.js can prove the visitor is still on their first look: not scrolled past 40px, not already played this session (`sessionStorage.heroPlayed`), and booted within 1500ms. Any miss means the hero is never armed — it renders as plain static content, never armed-but-invisible. Reduced-motion returns before `.js-motion` is added at all: honoured by doing nothing, not by animating and undoing.

### Timeline
A 2px rail with 14px node dots (paper fill, accent-mixed 2px border, z-lifted above the spine). An accent spine draws down the rail entry by entry on reveal (`draw-y` .85s, `calc(var(--i) * 130ms + 120ms)`); without the script it is simply already drawn. The current role's node is the only thing that keeps moving (2.6s pulse) — the one entry still in progress. Badges: "Now" in accent-bright, "Returned" in gold.

### Case Sections
Five studies inside one work sheet, so they are **flat sections separated by hairlines** — no cards nested in a card, no accent rails, no hover lift on a section the reader is not navigating to. The one tinted moment is the outcome block (`--accent-wash`, 12px radius): what actually changed is where a skim stops. Architecture diagrams render on demand — Mermaid is 3.5MB and imports on first toggle, with the Mermaid source itself as the fallback.

### Awards & Credentials
Award tiles are the gold-wash surface (gold-mixed border, gold title). Certifications separate by dashed hairlines; the five that also appear on the printed CV are weighted up and carry a small accent "on CV" pill.

### Testimonials
Solid sheet tiles (`--sheet-bg` 70% mixed into `--paper`, 12px radius) — content, not chrome, so no blur rides under a page of them. The opening quotation mark is tall quiet punctuation in accent, not decoration; attribution is an initials avatar on `--accent-wash` plus name and meta. Tiles render only from real, attributed submissions.

### Browser Surfaces
The design reaches the browser chrome itself: selection tinted 26% accent blue, caret in accent, a 12px rounded translucent scrollbar thumb. The prerendered pre-boot layer is deliberately plainer than the sheets — it is the document underneath the design, and it should read as one.

## Do's and Don'ts

### Do:
- **Do** write any dark token change in both places — the guarded `prefers-color-scheme` block and the `[data-theme="dark"]` rule (The Twice-Written Rule).
- **Do** gate every hiding rule behind `.js-motion` from motion.js, and restore every hidden state in the reduced-motion blocks (app.css's, plus Hero.razor.css's own beside the rules that create it) — and in the print block, which restores below-fold reveals so Ctrl+P on the showcase never prints blank sections.
- **Do** keep `backdrop-filter` on chrome only; sheets stay translucent-without-blur at .88–.9 alpha.
- **Do** keep gold on awards only, the alarm on the diagram's blocker only, and the stage hues inside the stage only.
- **Do** keep 44px tap targets, the 68ch measure, and the 112px mobile scroll-margin in step with the capsule strip.
- **Do** keep the prerendered `<div class="prerendered">` a direct child of `#app`, and mirror any header or contact-dock change in `prerender.py` (`static_shell_header` / `static_contact_dock`) byte-for-byte.
- **Do** carry final values in markup for anything a script counts or reveals — the static layer is the contract.
- **Do** verify both themes at 390×844 and desktop width before calling anything done.

### Don't:
- **Don't** put kickers or eyebrows above headings, and don't add border-left accent stripes — both are below the craft floor (The No-Kicker Rule).
- **Don't** build a stat-card band; the facts are one mono line woven into the hero.
- **Don't** blur content, and don't put anything animated or tinted behind the content — the ground is one flat, still surface (the still-ground rule); drift or glow back there is how the page starts reading as generated decor again.
- **Don't** give the hero sequence to a visitor who scrolled, has seen it this session, or waited past the 1500ms boot deadline — and never arm without a proved restore path.
- **Don't** raise the reveal IntersectionObserver threshold above 0 — a height-ratio threshold blanks tall sections on phones (the 6533px "Selected work" section was the proof).
- **Don't** print the design: the contact dock and progress bar are hidden in print, below-fold reveals are force-restored, and the printed CV (`/cv` document, `print.css`, `EmptyLayout`) stays deliberately ATS-plain outside this system by product rule — plain where machines read, expressive where humans look.
- **Don't** adopt numbered section wayfinding — the "Retrospective" discipline was declined at direction time; section numbers conflict with the No-Kicker Rule.
- **Don't** print the phone number as visible text on the showcase — it travels in the dock's `tel:` href only (anti-scrape posture, 2026-09-13).
