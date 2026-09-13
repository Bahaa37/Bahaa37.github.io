---
version: 1
slug: "src-cv-web-pages-home-razor"
primary_target: "src/Cv.Web/Pages/Home.razor"
related_targets: ["src/Cv.Web/Pages/CaseStudyPage.razor","src/Cv.Web/Pages/TestimonialsPage.razor","src/Cv.Web/Pages/PrintCv.razor","src/Cv.Web/Pages/NotFound.razor","src/Cv.Web/Pages/WwbWriteup.razor"]
---

# Surface brief — the showcase world

Scope: the whole showcase — / (canonical surface), /work/{slug}, the Windoor writeup, /testimonials, 404. /cv keeps its ATS-plain document; only its on-page chrome adopts the world.
Visitor mode: Experience (portfolio). Audience: recruiters and hiring managers first (30–60 second skim), engineers reading closely second.

Audience job: match seniority and fit in one skim, download the ATS-clean PDF, contact without follow-up questions.
Proof/content: projections of cv.json only — the DTC before/after diagram, verified metrics, evidenced skill chips. No invented material, no fabricated numbers.

Direction: FROSTED KEYNOTE — chosen on the decision page (answer: model-pick, no steer, buildPath code). The brief's pinned world; the roll's "Retrospective" declined on the pin, its numbered-wayfinding discipline noted but not adopted (section numbers conflict with the craft floor). Seed key d60cb62c; form = candidate 1 of the ordered grounded list.

AMENDMENT (2026-09-13, Sky Aluminum revision — user-proposed): three re-tints in one day, each on the record. The aurora died first (generated decor); neutral graphite died the same morning (correct but generic); Terminal Green was the user's pick from four swatched directions and died on review. The user then proposed the surviving direction themselves: **Apple's anodized baby-blue aluminum as a design language** — Glacier light (#E8F2FF — the iPhone 18 Pro's baby blue, exact from Apple's own CSS, agent-verified 2026-09-13), blue-slate night (#0D141D), steel-blue ink steps (#16222E family), Apple's own action blue (#0066CC light with white ink; #0A84FF with near-black ink in dark, the iOS pattern), and the material system the user named: **anodized-silver gradient edges** — 1px border-box gradient composites (--edge-metal) on every sheet and the study slab, single-tone silver (--edge-silver) on glass chrome and the toggle's hover ring, the contact dock now true frosted glass (the page's second fixed blur, with the header capsule). Gold metal stays awards-only: silver frames the content, gold marks recognition. The diagram stage is dark blue-charcoal with silver-steel (--stage-legacy) as the legacy estate and sky (--stage-lead) as what replaced it. The header compaction (~98px capsule, 112px scroll-margin), still-ground rule, toggle-glyph treatment, and phone-travel rule from earlier amendments all stand.

THESIS: The site behaves like a native Apple app — frosted chrome floating over solid content sheets on one still, neutral ground — proving the candidate engineers calm. It refuses the category-default scrolling document with its sticky stat band.

OWN-WORLD: A flat, still neutral ground (airy #F5F5F7 in light, graphite #0F1012 in dark — no tint, no drift, nothing animated behind the content); frosted-glass chrome (header capsule — backdrop-filter with saturate(180%) blur(20px), chrome only); near-opaque rounded content sheets (12–16px radii) carrying all dense text; Geist and Geist Mono; one blue accent for action and focus, gold reserved solely for the award metric, stage hues local to the hero diagram.

STORY: One viewport states who he is and the argument; the live diagram proves it; the visitor scrolls solid sheets, opens the diagram, downloads the PDF, and calls or emails — answers in hand, from any scroll position.

FIRST VIEWPORT: Floating glass header capsule (wordmark, root-relative nav with the theme glyph clustered at its end) over the flat ground. One solid hero sheet: the two-line display headline "I remove the constraint that froze the estate.", a pitch paragraph with the verified metrics woven into the sentence in mono numerals (5–7 days → 3 · 9 countries · 3.5+ years — no stat-card band), the before/after DTC diagram live in a recessed stage inside the sheet, then the blue capsule "Read the CV" beside ghost pills for Selected work and GitHub.

FORM: the pinned Apple-app world, seed key d60cb62c, graphite revision. Signature interaction: "the springy sheet" — sections enter once on a shared spring clock (rise + settle from an already-visible default, static under reduced-motion), and the header capsule's glass density responds to scroll. The hero diagram keeps its choreography but never replays over content already on screen (sessionStorage guard).

CONSTRAINTS (binding): prerendered div stays a direct child of #app; prerender.py's static_shell_header and static_contact_dock are rewritten with the same chrome; dark tokens written twice (prefers-color-scheme and [data-theme]); hiding classes only via motion.js; testimonials nav link dropped while the file ships empty; 44px tap targets; no kickers or eyebrows above headings; no border-left accent stripes; backdrop-filter on chrome only, never on content sheets; the contact dock and progress bar hidden in print with below-fold reveals force-restored; the printed CV stays ATS-plain; both themes verified at 390×844 and desktop.

Unresolved: none blocking.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
