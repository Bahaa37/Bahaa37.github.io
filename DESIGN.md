---
name: Hairline
description: The portfolio as a running engineering console. A near-black ground ruled by a 1px blueprint grid, two-tone Geist headings, Geist Mono for commands and data, a mint accent spent only on state, pill CTAs and chips, and a hero console that runs the real case studies.
colors:
  bg: "#050709"               # page ground                     light: #f6f7f9
  surface-1: "#0b0c0f"        # console windows                 light: #ffffff
  surface-2: "#0d0e11"        # cards                           light: #fbfbfc
  surface-3: "#101115"        # raised fills                    light: #f0f2f5
  surface-4: "#1d1d24"        # window dots, deepest step       light: #e6e9ee
  line: "#2e3238"             # the blueprint grid, card edges  light: #d5dae1
  text-1: "#f2f3f5"           # headings, key words             light: #0b0d10
  text-2: "#c3c8cf"           # lead, prose                     light: #2a3038
  text-3: "#9eaabf"           # body, console lines             light: #4a5363
  text-4: "#8a8f98"           # dim lead-in words, labels       light: #5b6472
  text-5: "#7a808c"           # smallest meta, $ prompt         light: #6b7280
  accent: "#6ee7a0"           # STATE ONLY: active, live, outcome, hero key phrase   light: #047857
  accent-bright: "#81ffb6"    # lit rules, glows                light: #059669
  info: "#7bd8ff"             # sky: flows, stack trails        light: #0369a1
  warn: "#ffa2a2"             # coral: problems                 light: #b42318
  gold: "#e6c766"             # awards only                     light: #a16207
  action-bg: "#ffffff"        # the one primary pill fill       light: #0b0d10
  action-ink: "#0a0a0a"       # text on the fill                light: #ffffff
  # Source: the vendored kit, src/Cv.Web/wwwroot/kit/hairline.css (readable source
  # in the private repo bahaa37/hairline-kit, src/tokens.css; synced by
  # _tools/sync_kit.py). Dark is the default on :root; LIGHT values are written
  # TWICE (the prefers-color-scheme block guarded by :not([data-theme="dark"]) and
  # :root[data-theme="light"]). Change both. app.css reads --hl-* directly and adds
  # layout tokens only (--measure, --site-header-h, --scroll-margin, --site-dock-h).
typography:
  family: "Geist (headings, UI, prose); Geist Mono (commands, data, dates, stack, slugs, the primary CTA)"
  display: "700 clamp(2.5rem, 1.6rem + 3.4vw, 4rem) / 1.06, tracking -0.025em (hero overrides size to clamp(2.5rem, 1.1rem + 3.2vw, 3.75rem))"
  h2: "500 clamp(2rem, 1.5rem + 2vw, 3rem) / 1.08, tracking -0.042em, two-tone"
  h3: "600 1.5rem / 1.33"
  h4: "600 1.1875rem / 1.47, tracking -0.01em"
  lead: "400 1.25rem / 1.4"
  body: "400 1.0625rem / 1.65 on the site (kit body 1rem / 1.5)"
  label: "Geist Mono 500 0.6875rem / 1.4, uppercase, tracking 0.12em: data labels only"
  term: "Geist Mono 400 0.71875rem / 2: console lines"
  cta: "Geist Mono 700 1.125rem / 1.4, uppercase, tracking 0.12em: the primary pill only"
rounded:
  pill: "9999px (CTAs, chips, badges)"
  window: "16px (console windows)"
  card: "12px (cards)"
  panel: "10px (compare halves)"
  chip-square: "6px"
  xs: "3px (rail bar)"
spacing:
  scale: "4, 6, 8, 10, 12, 16, 20, 24, 40, 56, 80px"
  container: "1320px, gutter 16px (24px from 640px)"
  header: "72px fixed; two rows under 720px"
  measure: "68ch"
---

# Design System: Hairline

Pinned by the owner on 2026-10-09 to the look and feel of jsmastery.com's
agentic-engineering course page. It replaced the Spec Sheet world (graphite, no hue,
no capsules) outright. The pills, the mint accent and the guarded header blur were
reversals the owner chose on purpose. The kit is its own product (private repo
`bahaa37/hairline-kit`), and this site vendors it to `wwwroot/kit`. `/styleguide`
renders every token and component live from the shipped stylesheet.

## Principles

1. **The page runs, it does not describe.** The hero console runs the real case
   studies: the slug command, the first sentence of the summary, the stack trail,
   then the ◆ outcome with a link to the study. It autoplays every 6s and pauses on
   hover, on focus, when offscreen, or when the tab is hidden. Tapping a slug chip runs
   that study. Every line comes from cv.json (`CaseStudyConsole.RunLines`).
2. **Mint is state, never decoration.** `--hl-accent` marks the active chip or tab,
   the live dot, the outcome, the console command, the current role's rail segment, and
   the headline's key phrase (hero only). Coral (`--hl-warn`) marks problems, sky
   (`--hl-info`) marks flows and stack trails, gold marks awards. There are no era or
   category colours.
3. **The grid is the frame.** A 1px `--hl-line` ruled blueprint grid (`.hl-grid` /
   `.hl-cell`) frames every section. Neighbouring cells share one rule through a
   -1px start margin, so seams never double.
4. **Two-tone headings.** Lead-in words are dim (`.hl-dim`, text-4) and the key words
   are text-1. In the hero alone, the key phrase is mint (`.hl-key`). No gradient
   text, ever.
5. **Mono has a job.** Geist Mono sets commands, data, dates, stack, slugs and labels,
   plus one voice: the single primary CTA, in mono uppercase. Ghost and secondary
   buttons are Geist, sentence case, weight 600. A row of mono-caps buttons shouts.
6. **Light around content, stillness behind it.** Soft radial glows and a static hero
   mesh (`--hl-hero-mesh`, painted, never animated) sit behind the hero. Console
   windows carry the deep window shadow; cards stay flat with a hairline edge.

## Shapes

- Pills (`9999px`) for every CTA and chip. The primary pill is white (dark theme) or
  ink (light theme), 56px tall, and carries a sheen that crosses once per 7s and only
  under motion. Ghost pills sit on a translucent fill with a soft line.
- 12px cards (`.hl-card`). Hover lights the edge mint and fades in a top wash. A
  featured card (the flagship case study) replaces its border with a lit ring that
  travels along the line. That ring is a masked gradient, never a side stripe.
- 16px console windows (`.hl-window`): traffic dots (coral, gold, mint), a mono
  title, a bottom-anchored log, a status row with a live dot, and slug chips.
- Compare blocks (`.hl-compare`): a coral-washed "from" panel and a mint-washed "to"
  panel at 10px, joined by one coral-to-mint lit rule.

## Layout

- **Hero:** 58/42 from 960px. The left column holds the two-tone headline, the pitch,
  the white "Read the CV" pill, ghost pills, and four derived figures as a mono proof
  row. The right column holds the console, with a glow off its corner. On mobile the
  console comes before the proof row. The tech-stack marquee sits at the fold line.
- **Home order:** hero, marquee, selected work (ruled cells with problem-to-outcome
  compares), skills, career rail, credentials, contact. The dock is reachable from
  anywhere.
- **Skills (`#skills`):** Workflow-style tabs (`.hl-tabs`) on a 7s autoplay ring,
  each panel paired with an evidence console for its skill group. Below 720px the tab
  strip becomes a scroll row with a trailing fade as its cue.
- **Career rail:** neutral. A 1px line runs the length, and only the current role is
  lit: a 3px mint segment that grows with scaleY on reveal, topped by the live dot.
- **Header and dock:** fixed, using `--hl-header-bg`. The opaque value is the
  fallback, and inside `@supports (backdrop-filter)` the alpha drops and a 12px blur
  takes over.
- **Long-form pages** (`/work/{slug}`, the write-up): document styles live in
  `app.css`, at a 68ch measure.

## Motion

Motion is additive. Content is hidden only under `html.hl-motion`, which `hairline.js`
adds only when IntersectionObserver exists and motion is allowed. Dead JS therefore
leaves everything visible. Sections reveal with a 16px rise on the reveal ease
(700ms). Hero lines rise with a 90ms stagger. Console lines fade in, and the result
pops with overshoot. With reduced motion, every completed state shows at once: no
autoplay, a static marquee, a fully drawn rail, no sheen, no pulse.

## Rules carried from earlier worlds (correctness, not taste)

- **Theme tokens are written twice.** Change both blocks, in the kit, never in
  app.css.
- **The old Edge WebView forbids** `color-mix()` and the individual
  `translate` / `rotate` / `scale` properties. Use precomputed `rgba()` and
  `transform`.
- **`backdrop-filter` only inside `@supports`**, always over an opaque fallback
  value.
- **Never an unconditional `opacity: 0`.** Hiding lives behind `.hl-motion` (kit) or
  `.js-motion` (motion.js).
- **The static layer is mirrored.** The header (`static_shell_header`), the dock
  (`static_contact_dock`), the hero console and figures, the marquee, the skills tabs,
  the testimonial card and `/styleguide` all have markup mirrors in
  `_tools/prerender.py`. Change both sides. `hairline.js` runs the console and tabs
  without Blazor.
- **`/cv` stays ATS-plain white paper.** Only its on-page action row wears the world,
  and print drops all chrome.
- **Tap targets are 44px** (`pointer: coarse` floors on buttons, chips and tabs).
- **Every figure is derived** from cv.json. Never type one into markup.

## Don't

- Don't put eyebrows or kickers above headings. `.hl-label` is for data labels only
  (console hints, `dt` terms, counters).
- Don't number sections. Grid lists drop their markers so they never read as
  numbers.
- Don't use border-left accent stripes, or gradient text.
- Don't spend mint on decoration, links-at-rest or chrome. Don't bring gold out of
  awards.
- Don't animate anything inside the hero mesh or behind the content.
- Don't set secondary buttons in mono caps.
