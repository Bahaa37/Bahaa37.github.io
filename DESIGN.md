---
name: Frosted Keynote — Bahaa Aldeen Mohamed
description: A native-app portfolio — frosted glass chrome floating over solid content sheets on one aurora-lit field.
colors:
  ink: "#1d1d1f"
  ink-soft: "#424245"
  ink-faint: "#56575b"
  paper: "#f5f5f7"
  sheet-bg: "rgba(255, 255, 255, .9)"
  sheet-line: "rgba(0, 0, 0, .08)"
  accent: "#0066cc"
  accent-bright: "#0071e3"
  accent-wash: "#e8f1fb"
  action-bg: "#0066cc"
  action-bg-hover: "#0059b3"
  action-ink: "#ffffff"
  gold: "#8a6116"
  gold-wash: "#fbf3e2"
  alarm: "#b0432c"
  alarm-wash: "#fbeae6"
  aurora-blue: "#0a84ff"
  aurora-teal: "#5ac8d8"
  aurora-violet: "#7d7aff"
  glass-bg: "rgba(255, 255, 255, .58)"
  glass-line: "rgba(255, 255, 255, .65)"
  pill-line: "rgba(0, 0, 0, .24)"
  pill-bg: "rgba(255, 255, 255, .7)"
  line: "rgba(0, 0, 0, .1)"
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
    backgroundColor: "transparent"
    textColor: "{colors.ink-soft}"
    rounded: "50%"
    size: "44px"
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

**Creative North Star: "Frosted Keynote"**

The site behaves like a native Apple app: one aurora-lit field behind everything, frosted glass reserved for chrome (the header capsule), and near-opaque rounded content sheets carrying every dense word. Direction chosen on the impeccable decision page (answer: model-pick, code-led; seed key `d60cb62c`), first shipped 2026-09-12. The world proves the candidate engineers calm — it refuses the category-default scrolling document and its sticky stat band.

The dosage law governs everything: **glass is chrome, sheets are solid.** `backdrop-filter` is spent exactly once, on the header capsule; content sheets are translucent without blur (`--sheet-bg` at .88–.9 alpha), so a 6000px page never holds a live GPU blur under the reader and first paint stays under a second — a product rule, not a preference. Depth comes from the fixed aurora field and a three-stage sheet shadow, not from layer effects on content.

Motion is one orchestrated system on a shared ease-out clock (`cubic-bezier(.16, 1, .3, 1)`): sections settle in as sheets (rise 26px + settle from an already-visible default), items stagger at 50ms per index, and the hero plays a single ~2.6s sequence — but only for qualifying visits (see Components). Hiding is additive-only: every hiding rule is gated behind `.js-motion`, added by `js/motion.js` and nowhere else, so a script failure can never leave content invisible. Reveals animate the individual `translate`/`scale` properties, never `transform` — transform is reserved for hover lifts so the two compose cleanly.

The interface's voice is first-person, precise, engineering-grade: labels are quiet Geist Mono uppercase, attribution reads as a byline under a title (never a label above it), and verified metrics are woven into sentences in tabular mono numerals instead of card grids. Nothing decorative is asserted as fact — no invented numbers, no invented quotes.

**Key Characteristics:**

- Aurora field: three transform-only radial-gradient blobs on one shared drift clock, present at first paint from the shell, outside the app runtime.
- Frosted capsule header is the only real glass; sheets are translucent-without-blur slabs (16px radius).
- One blue accent for action, links, and focus; gold spent on exactly one subject (awards); alarm red only for the diagram's blocker.
- Geist + Geist Mono; negative tracking on every heading; mono carries all data and labels.
- Capsule radii (999px) for all interactive chrome; hairlines, not boxes, separate content inside a sheet.
- Reduced motion restores every hidden state; the printed CV sits outside this system entirely (ATS-plain by product rule).

## Colors

Cool, restrained, and atmospheric: near-neutral ink steps on an airy light ground or a deep-space dark ground, one engineering blue for action, and single-use warm and alarm notes.

### Primary
- **Action Blue** (`--accent` / `--action-bg` #0066cc): links and text on sheets — split from the button fill because a fill and a text link need different contrast solutions; the fill carries white text at AA, the link sits on a white sheet at AA. `--action-bg-hover` #0059b3 on hover; `--accent-bright` #0071e3 is the focus-ring and timeline-spine brightness; `--accent-wash` #e8f1fb tints evidenced chips, outcome blocks, and avatars. Dark: `--accent` #8abaff, `--accent-bright` #a8ccff, `--action-bg` #0a84ff with `--action-ink` #071018.
- **Aurora Blue** (`--aurora-1` #0a84ff): the field's dominant blob, the selection tint (26% mix), and the reading-progress bar's left stop. Same in both themes.

### Secondary
- **Aurora Teal** (`--aurora-2` #5ac8d8) and **Aurora Violet** (`--aurora-3` #7d7aff): the field's other two blobs; teal also marks the "After"/lead state in the diagram stage and the progress bar's right stop. Same hues in both themes — only the veil over them changes (`--aurora-veil` .35 light, .3 dark), so the field reads airy by day and submarine by night.

### Tertiary
- **Award Gold** (`--gold` #8a6116, `--gold-wash` #fbf3e2; dark #e0b95f / #2a2213): the one warm note, spent on awards only — the hero's award fact, metric chips on award-earning achievements, award tiles, and the "returned" badge. Nowhere else.
- **Blocker Alarm** (`--alarm` #b0432c, `--alarm-wash` #fbeae6; dark #e5806a / #2c1a15): the diagram's blocker colour — dashed border, dissolving node, flag pulse. It earned its own token when it started animating; it does not generalize to "errors" elsewhere.

### Neutral
- **Ink** (`--ink` #1d1d1f; dark #f5f5f7): headings and primary text. **Ink Soft** (`--ink-soft` #424245; dark #c6cdd8): body prose and ledes. **Ink Faint** (`--ink-faint` #56575b; dark #9aa4b1): the smallest text — held at or above 4.5:1 on its sheet after the previous palette failed AA.
- **Airy Ground** (`--paper` #f5f5f7) / **Deep-Space Ground** (`--paper` dark #0b1220): the html background the aurora glows over; body stays transparent so the fixed field shows through.
- **Sheet** (`--sheet-bg` rgba(255,255,255,.9); dark rgba(21,29,41,.88)) with **Sheet Hairline** (`--sheet-line` rgba(0,0,0,.08); dark rgba(255,255,255,.09)): the content slab. Opaque enough that body text keeps AA over whatever part of the aurora drifts beneath.
- **Hairline** (`--line` rgba(0,0,0,.1); dark rgba(255,255,255,.11)): separators, node dots, quiet borders.
- **Glass** (`--glass-bg` rgba(255,255,255,.58); dark rgba(16,24,36,.55)) with **Glass Edge** (`--glass-line`) and the **inner top highlight** (`--glass-highlight`, an inset white line — the tell of real glass): chrome only.
- **Ghost Pill** (`--pill-line` rgba(0,0,0,.24); dark rgba(255,255,255,.18), `--pill-bg` rgba(255,255,255,.7); dark rgba(255,255,255,.06)): the on-sheet ghost treatment. Deliberately distinct from true glass — a pill sits ON a sheet, not over the field, so it needs a sheet-visible edge instead of a blur. Accepted: the light-theme edge composites under the strict WCAG 1.4.11 3:1 non-text boundary guideline by design; the text carries the meaning.

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
- **720px**: the header capsule keeps two rows *inside one capsule* — name + toggle on row one, the nav as a horizontal scroll strip on row two (nowrap, hidden scrollbar, faded right edge, snap points); radius eases 999px → 24px. **The Capsule Strip Rule:** the collapsed capsule is ~118px tall, so the mobile `scroll-margin-top` is 132px (app.css, `max-width: 720px` block, `.sheet[id], .case[id]`). If the capsule is ever compacted or expanded, that 132px must move with it — the two are one decision.
- **900px**: the hero grid stacks; the diagram's three columns become one, bridge rotating from vertical to horizontal.
- **940px**: timeline entries gain a 10.5rem right-aligned period column; below it the period sits above the body with a tight 14px rail gutter (deliberate — a wide gutter pushed entries out of alignment with the section heading on phones).

Anchor navigation is compensated everywhere: `.sheet[id]` carries `scroll-margin-top: 92px` on desktop, `.case[id]` 96px, both overridden to 132px inside the 720px block.

## Elevation & Depth

Depth is one continuous field behind floating slabs — never drop shadows on inline elements, never stacked card layers. The ground lives on `html` (`--paper`), the aurora is `position: fixed; z-index: -1` outside `#app` in `index.html`, so it survives both the prerender fill and the Blazor boot and costs zero runtime bytes. Body stays transparent or it would paint over the field.

**The aurora field:** three `<i>` layers, plain radial gradients (`closest-side`, transparent at 70–72%), 68/58/64 vmax, veiled by `--aurora-veil`. Drift is transform-only animation on a shared clock of deliberately non-multiple periods (84s / 63s / 77s, `linear infinite alternate`) so the field phases in and out of alignment rather than ticking mechanically; the gradients themselves rasterize exactly once. Under reduced motion the layers hold their rest pose; in print the field is `display: none` — three colour blobs behind ATS-critical text is a defect CI cannot see.

**Reading-progress bar:** a 2px fixed `body::before` gradient (Aurora Blue → Aurora Violet) driven by `animation-timeline: scroll()` — no script, no markup, compositor-only. Entirely inside `@supports`, so incapable browsers never draw it; hidden in print.

### Shadow Vocabulary
- **Sheet shadow** (`--shadow-sheet`: `0 1px 2px rgba(16,24,40,.05), 0 12px 32px rgba(16,24,40,.08), 0 32px 80px rgba(10,80,160,.07)`; dark: black-based): every content sheet — one crisp contact step, one mid lift, one wide blue-tinted atmosphere.
- **Float shadow** (`--shadow-float`: `0 2px 6px rgba(16,24,40,.08), 0 12px 28px rgba(16,24,40,.12)`; dark: black-based): the header capsule and the diagram stage.
- **Glass highlight** (`--glass-highlight`: `inset 0 1px 0 rgba(255,255,255,.45)`; dark .09): the inner top edge that says "real glass".
- **Aurora glow** (`--aurora-glow` rgba(10,132,255,.14); dark teal rgba(90,200,216,.12)): hover-only halo (`0 10px 26px` under buttons and study links, `0 6px 18px` under chips). Shadows appear as a response to state, never at rest beyond the sheet/float vocabulary.

### Named Rules
**The Chrome-Only Blur Rule.** `backdrop-filter` (`saturate(180%) blur(20px)`) is spent exclusively on the header capsule. Content sheets are translucent *without* blur: a blur under a long page is a GPU layer held alive the whole read, and render cost for nothing behind a .9-alpha sheet. Any new floating chrome may ask for glass; any content surface may not.

**The Scrolled-Depth Rule.** The capsule's glass deepens once content passes underneath — `.is-scrolled` (set by an inline script at scrollY > 8, rAF-throttled, surviving the Blazor boot boundary) mixes `--glass-bg` 72% into `--paper`. It is state, not motion, so it runs regardless of reduced-motion.

## Shapes

Two form families and a hairline. **Capsules:** anything interactive or chrome-like is a full pill (999px) — buttons, nav links, chips, badges, the header capsule, the skip link; the theme toggle is a 44px circle. **Slabs:** content containers round at 16px (`--radius-sheet`), the diagram stage at 14px, inner tiles (outcome blocks, study links, testimonials, awards, diagram canvases) at 12px (`--radius`), the gold metric chip at 8px (the one squared chip — it marks data, not action), diagram nodes at 6px. **Hairlines** do the separating inside sheets: 1px `--sheet-line` between flat case sections, `--line` under study headers and between prev/next, dashed `--line` between certifications. A dashed border is otherwise reserved for exactly one thing — the diagram's blocker node. Borders go quiet-to-accent on hover; nothing gains a border at rest that it did not have. Focus is a 2px `--accent-bright` outline, offset 3px, 4px radius, on `:focus-visible` only.

## Components

### Buttons
- **Shape:** capsule (999px), min-height 44px — the tap-target floor; padding (0.6rem 1.35rem) carries the size.
- **Primary:** `--action-bg` fill, `--action-ink` text, 0.95rem/600. Hover deepens to `--action-bg-hover`, lifts 1px, and throws the aurora glow.
- **Ghost:** the on-sheet pill (`--pill-line` / `--pill-bg`), ink text, no blur — see The Chrome-Only Blur Rule. Hover takes the accent border and accent text.
- **Motion:** transitions at .22s, the shared ease-out on `translate`; `:active` returns to 0.

### Chips
- **Style:** small capsules (min-height 32px, 0.88rem) bordered `--sheet-line`, background `--sheet-bg` at 80% — scannable objects, not list rows.
- **Evidenced variant:** ink text at 600, `--accent-wash` fill, accent-mixed border — an evidenced skill outranks an unevidenced one; each carries its backing employer in `--chip__where` mono (0.72rem, Ink Faint).
- **Hover:** lift 1px, accent border, aurora glow. A chip never widens the page (`max-width: 100%`).
- **Metric chip:** the gold 8px-radius chip inline after an achievement; the only warm mark in running text.

### Header Capsule & Navigation
The one piece of true glass: sticky header (no background of its own), inner capsule at min-height 56px, `--glass-bg`/`--glass-line`, float shadow + glass highlight, `backdrop-filter: var(--glass-blur)`, deepening on scroll (see Elevation). Wordmark left in Geist 600; root-relative nav links (44px tap targets, quiet ink-soft, hover wash `color-mix(in srgb, var(--ink) 7%, transparent)`) and the theme toggle right. This markup is duplicated byte-for-byte by `_tools/prerender.py`'s `static_shell_header` so pre- and post-boot chrome cannot diverge — change them together. The Testimonials link renders only while a real quote exists; an empty `testimonials.json` ships no link.

### Theme Toggle
A 44px circle, 1px `--line` border, holding both drawn SVG icons (sun and moon, `stroke="currentColor"`, **stroke-width 1.6**, round caps) at 18px. Which icon shows is pure CSS state — the theme selectors decide — so the control is byte-identical between the prerendered shell and the Blazor render, and the icon can never fall out of sync with the palette. The toggle inverts the *effective* theme, not the stored value: system-dark with no preference goes to light in one click.

### Hero Sheet & Diagram Stage
The opening sheet: three-line display headline ("constraint" takes the accent — the one colour word), a 46ch pitch, then the track record as one mono facts line — never a stat-card band; figures carry their final values in the markup so the count-up can only ever be an enhancement. The before/after DTC diagram sits in a **recessed keynote stage**: dark in *both* themes (`linear-gradient(180deg, #101a2c, #0b1220)` plus aurora radial washes), 14px radius, aurora-blue-mixed border — one deliberate contrast moment, with every colour inside local to the stage. Before-panel nodes build, the blocker is flagged (alarm ring at 1600ms) before the bridge line draws (1620ms) and the modernized services arrive; the blocker then dissolves to .26 opacity + grayscale.

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
The design reaches the browser chrome itself: selection tinted 26% Aurora Blue, caret in accent, a 12px rounded translucent scrollbar thumb. The prerendered pre-boot layer is deliberately plainer than the sheets — it is the document underneath the design, and it should read as one.

## Do's and Don'ts

### Do:
- **Do** write any dark token change in both places — the guarded `prefers-color-scheme` block and the `[data-theme="dark"]` rule (The Twice-Written Rule).
- **Do** gate every hiding rule behind `.js-motion` from motion.js, and restore every hidden state in the reduced-motion blocks (app.css's, plus Hero.razor.css's own beside the rules that create it).
- **Do** keep `backdrop-filter` on chrome only; sheets stay translucent-without-blur at .88–.9 alpha.
- **Do** keep gold on awards only, and the alarm on the diagram's blocker only.
- **Do** keep 44px tap targets, the 68ch measure, and the 132px mobile scroll-margin in step with the capsule strip.
- **Do** keep the prerendered `<div class="prerendered">` a direct child of `#app`, and mirror any header change in `prerender.py`'s `static_shell_header` byte-for-byte.
- **Do** carry final values in markup for anything a script counts or reveals — the static layer is the contract.
- **Do** verify both themes at 390×844 and desktop width before calling anything done.

### Don't:
- **Don't** put kickers or eyebrows above headings, and don't add border-left accent stripes — both are below the craft floor (The No-Kicker Rule).
- **Don't** build a stat-card band; the facts are one mono line woven into the hero.
- **Don't** blur content, animate the aurora with anything but transform, or repaint the field after first raster.
- **Don't** give the hero sequence to a visitor who scrolled, has seen it this session, or waited past the 1500ms boot deadline — and never arm without a proved restore path.
- **Don't** raise the reveal IntersectionObserver threshold above 0 — a height-ratio threshold blanks tall sections on phones (the 6533px "Selected work" section was the proof).
- **Don't** print the design: the aurora and progress bar are hidden in print, and the printed CV (`/cv` document, `print.css`, `EmptyLayout`) stays deliberately ATS-plain outside this system by product rule — plain where machines read, expressive where humans look.
- **Don't** adopt numbered section wayfinding — the "Retrospective" discipline was declined at direction time; section numbers conflict with the No-Kicker Rule.
