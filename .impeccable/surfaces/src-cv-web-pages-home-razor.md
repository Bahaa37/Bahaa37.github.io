---
version: 1
slug: "src-cv-web-pages-home-razor"
primary_target: "src/Cv.Web/Pages/Home.razor"
related_targets: ["src/Cv.Web/Pages/CaseStudyPage.razor","src/Cv.Web/Pages/TestimonialsPage.razor","src/Cv.Web/Pages/PrintCv.razor","src/Cv.Web/Pages/NotFound.razor","src/Cv.Web/Pages/WwbWriteup.razor"]
---

# Surface brief: the showcase world

Scope: the whole showcase: `/` (the canonical surface), `/work/{slug}`, the Windoor write-up,
`/testimonials`, `/styleguide` and 404. `/cv` keeps its ATS-plain document; only its on-page
chrome adopts the world.

Visitor mode: Experience (portfolio). Audience: recruiters and hiring managers first (a 30–60
second skim), engineers reading closely second.

Audience job: match seniority and fit in one skim, download the ATS-clean PDF, and get in touch
without follow-up questions.

Proof and content: projections of cv.json only. Verified metrics, evidenced skills and real case
studies. No invented material.

## Direction contract

DIRECTION: **HAIRLINE**. Pinned by the user on 2026-10-09: "looks and feels like"
jsmastery.com/course/agentic-engineering-course. The direction roll was skipped because a
user-pinned direction beats the roll. Measured reference: hairline-kit/reference/findings.md.
Seed key: none (pinned). The kit lives in the private repo bahaa37/hairline-kit and is vendored to
wwwroot/kit.

THESIS: The portfolio as a running engineering console. Instead of describing the method, the page
executes it: the hero console runs the real case studies, and the skills tab through their evidence.
It refuses the screenshot-grid portfolio and the previous Spec Sheet grey-on-grey.

OWN-WORLD:
- Grounds: near-black `#050709`, surfaces stepping up in 2–4% increments.
- Structure: a 1px `#2E3238` ruled blueprint grid frames every section.
- Accent: mint `#6EE7A0`, spent only on state (active, live, outcome, the key words of the headline).
- Secondary colours: coral for problems, sky for flows, gold for awards.
- Type: Geist (two-tone headings: grey lead-in words, white key words) and Geist Mono for commands
  and data only.
- Shapes: pill CTAs and chips; 12px cards; 16px console windows.
- Effects: soft radial glows; a static blurred hero mesh.
- Light theme: the same structure on `#F6F7F9`, with an emerald accent `#047857`.

STORY: In one viewport the visitor reads the claim, sees a console printing a real engagement
(problem → approach → ◆ outcome), and can tap any case study to run it. The skim continues:
- selected work, as ruled cells with problem→outcome comparisons
- skills, as autoplaying tabs with an evidence console
- the career rail, whose bars grow as it scrolls into view
- credentials
- the contact close; the dock is reachable from anywhere

FIRST VIEWPORT:
- Header: a 72px glass header (logo/name left; nav plus theme switch right).
- Left column (about 52%): the two-tone display headline with key words in mint, the pitch, the
  white pill "Read the CV", ghost pills for the PDF and the work, and the four derived figures as a
  mono proof row.
- Right column: the `.hl-window` `bahaa · case-studies.run`, with a bottom-anchored log, a live
  dot and status row, and case-study chips.
- The hero mesh glows behind the window.
- Below the fold line: the tech-stack marquee.

FORM: The signature interaction is "the run": the console types a case study line by line
(450ms steps, the ◆ result pops with overshoot), autoplays every 6s, pauses on hover or focus or
offscreen, and runs the chosen study on tap. The result links to the full case study. Supporting
it:
- One page entrance: the headline lines rise with a 90ms stagger and settle by about 1.2s.
- Sections reveal by rising 16px with the reveal ease.
- Skills autoplay on a 7s progress ring.
- Reduced motion shows every completed state, with no autoplay.

CONSTRAINTS (binding, carried over):
- The prerendered div stays a direct child of `#app`.
- prerender.py's `static_shell_header` and `static_contact_dock` mirror the chrome.
- Dark tokens are written twice.
- Hiding happens only under `.hl-motion` / `.js-motion`.
- 44px tap targets.
- No kickers or eyebrows above headings, no border-left accent stripes, no gradient text.
- Mono for data only.
- The console and tabs work in the static layer (`hairline.js` runs without Blazor).
- Testimonials are linked only when real quotes exist.
- The printed CV stays ATS-plain.
- Both themes are verified at 390×844 and at desktop width.
- The old Edge WebView: no `translate` property, no `color-mix()`, and `backdrop-filter` only
  under `@supports`.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
