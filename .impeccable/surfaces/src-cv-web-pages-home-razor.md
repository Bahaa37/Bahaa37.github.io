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

THESIS: The site behaves like a native Apple app — frosted chrome floating over solid content sheets on one aurora-lit field — proving the candidate engineers calm. It refuses the category-default scrolling document with its sticky stat band.

OWN-WORLD: An aurora gradient mesh (blue #0A84FF, teal #5AC8D8, violet #7D7AFF) drifting on one shared clock over a deep-space ground in dark theme and an airy #F5F5F7 ground in light; frosted-glass chrome (header capsule, pills, chips — backdrop-filter with saturate(180%) blur(20px), chrome only); near-opaque rounded content sheets (12–16px radii) carrying all dense text; Geist and Geist Mono; one blue accent for action and focus, gold reserved solely for the award metric.

STORY: One viewport states who he is and the argument; the live diagram proves it; the visitor scrolls solid sheets, opens the diagram, downloads the PDF, and emails — answers in hand.

FIRST VIEWPORT: Floating glass header capsule (wordmark, root-relative nav, drawn SVG theme toggle) over the aurora field. One solid hero sheet: the two-line display headline "I remove the constraint that froze the estate.", a pitch paragraph with the verified metrics woven into the sentence in mono numerals (5–7 days → 3 · 9 countries · 3.5+ years — no stat-card band), the before/after DTC diagram live in a recessed stage inside the sheet, then the blue capsule "Read the CV" beside glass pills for Selected work and GitHub.

FORM: the pinned Apple-app world, seed key d60cb62c. Signature interaction: "the springy sheet" — sections enter once on a shared spring clock (rise + settle from an already-visible default, static under reduced-motion), and the header capsule's glass density responds to scroll. The hero diagram keeps its choreography but never replays over content already on screen (sessionStorage guard).

CONSTRAINTS (binding): prerendered div stays a direct child of #app; prerender.py's static_shell_header and NAV_LINKS are rewritten with the same capsule header; dark tokens written twice (prefers-color-scheme and [data-theme]); hiding classes only via motion.js; testimonials nav link dropped while the file ships empty; 44px tap targets; no kickers or eyebrows above headings; no border-left accent stripes; backdrop-filter on chrome only, never on content sheets; the printed CV stays ATS-plain; both themes verified at 390×844 and desktop.

Unresolved: none blocking.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
