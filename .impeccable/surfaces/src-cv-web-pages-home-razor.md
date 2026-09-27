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
Proof/content: projections of cv.json only — verified metrics, evidenced skill chips, real case studies. No invented material, no fabricated numbers.

## Direction contract

DIRECTION: **LEGAL TENDER** — chosen on the decision page (answer: model-pick — Impeccable's Pick, no steer, buildPath code). Seed key aaa7f143; the roll's assigned direction "The Annual Report" (Swiss annual report) was beaten on audience identification and tied on clarity, but its four raises were named on the card and carry into this build as disciplines. Prior worlds (Frosted Keynote / Sky Aluminum) are the anti-reference; the hero before/after diagram is deleted at the user's word ("i hate the diagram").

THESIS: The portfolio as an engraved banknote — the solo-built payment gateway earns the denomination. Where every other portfolio shows screenshots, this one shows intaglio: the craft of printing value, held by the engineer who built payment rails for nine markets. It refuses the category-default project-grid and the old aluminum world alike.

OWN-WORLD: Rag-paper ground in light (#f3eede), deep intaglio plate in dark (#0d1712 — green-black, not gray). Ink: green-black (#14261e light / #e6dcc2 aged cream dark). One accent: banknote green (#0c5a45 light / #4ba583 dark); bronze/copper (#7a4a2b / #c98a4b) marks recognition only (medallions — awards), the gold-singularity rule reborn in copper. Engine-turned line fields (authored SVG line geometry, data-URI or inline) fill the denomination numeral and plate borders — lines as structure, never loose ornament. Double hairline rules with corner rosettes frame each content plate. Type: Bodoni Moda (display/denomination — engraved didone), Spectral (body — document serif), Fragment Mono (serials, labels, data). No blur anywhere in this world: intaglio is flat ink on paper; the header is opaque paper under a double rule.

STORY: One viewport shows the denomination — a "9" at banknote scale, engine-turned — and the legend NINE COUNTRIES — ONE GATEWAY · BUILT ALONE, and the reader understands both the claim and the trade: precision. The skim moves across the plate series (flagship note, then the numbered issues), takes the specimen (PDF), and reaches the contact seal from any scroll position.

FIRST VIEWPORT: Opaque paper header band under a double hairline (wordmark, tracked-caps nav, medallion theme toggle). The note face fills the rest: left, the denomination "9" in Bodoni at ~40vh with the engine-turned fill; right, the title lettering "NINE COUNTRIES — ONE GATEWAY", the plate legend "BUILT ALONE · END TO END" in tracked mono, the pitch in Spectral, the plate serial set from real figures (9 markets · 7 gateways · 491 tests), and the key-figures rule-row; actions as the green intaglio seal ("Read the CV") beside a ruled ghost ("Download CV (PDF)").

FORM: Signature interaction — "the plate press": on first visit the denomination's line field prints in one damped pass (~800ms, clip/opacity, never replayed on scroll; static under reduced-motion and on replay), and sections enter with a single press-settle (rise 8px, damped ease-out, from visible). The damped cross-check sweep disciplines the count-ups. States: chips are cited seals; the contact dock is a seal strip (behavior unchanged: tel:/mailto, anti-scrape).

CONSTRAINTS (binding, carried): prerendered div stays a direct child of #app; prerender.py's static_shell_header and static_contact_dock mirror the new chrome (class names preserved where possible); dark tokens written twice; hiding classes only via motion.js; testimonials link only when real quotes exist; 44px tap targets; no kickers or eyebrows above headings; no border-left accent stripes; nothing animated behind content (still-ground); contact dock hidden in print, below-fold reveals force-restored; printed CV stays ATS-plain; both themes verified at 390×844 and desktop; the user's review browser is an old Edge WebView (no `translate` property, no `color-mix()` — transform + solid fallbacks only).

Unresolved: none blocking.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
