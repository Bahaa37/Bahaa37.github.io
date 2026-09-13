# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: recruiters and hiring managers screening candidates for senior .NET and
solution-architecture-track roles — mostly remote-first (EU hours; open to Gulf/EU
relocation). Success is an interview invitation, and the site must survive a close
reading by an engineer during the process, because it doubles as the work sample.
(Confirmed in the init interview, 2026-09-12.)

## Product Purpose

The personal portfolio and CV of Bahaa Aldeen Mohamed: an interactive showcase, a
downloadable ATS-clean printable CV, and per-engagement case studies, all projected
from one data file. It exists to win interviews for solution architecture and systems
analysis roles by presenting evidence — a verifiable timeline, quantified outcomes,
and a site that demonstrates the engineering it claims.

## Positioning

Confirmed in the init interview (2026-09-12): the site must make two things undeniable
when compared against another senior .NET candidate —

1. **Architecture-ready.** Systems analysis and design depth: solution architecture
   documents, SRS/LLD, diagramming — the credible step up to solution architect.
2. **AI-forward engineering.** AI skills, Copilot Studio agents, and AI-guided
   workflows that measurably halved an upgrade cycle and trained a whole company.

Modernization leadership (the DTC-removal story) and the site-as-work-sample argument
remain supporting evidence for those two claims, not the headline.

## Operating Context

- Public repository, deployed to GitHub Pages at bahaa37.github.io; recruiters can read
  the source, so nothing may be committed that the candidate would not publish.
- The PDF travels through job applications where applicant tracking systems
  machine-parse it; `_tools/ats_check.py` gates every deploy on real text extraction.
- Working from Alexandria, Egypt (EET, UTC+2): full EU-hours overlap, mornings overlap
  US Eastern. Availability: open to opportunities, one month's notice. Open to remote,
  hybrid, on-site, and relocation to the Gulf or EU.
- Job-search strategy material lives in `docs/content/` (gitignored): target companies
  and salary posture never enter the public repo.

## Capabilities and Constraints

- `wwwroot/data/cv.json` is the single source of truth; the showcase, printable CV, and
  `CvValidator` are projections of it. Content lives nowhere else.
- CI content gates: overlapping full-time roles fail the build; technology claimed
  before its release date fails; unquantified achievements warn and are never
  auto-filled; no invented testimonials — third-party quotes arrive only from real,
  attributed submissions in `testimonials.json`, which currently ships empty.
- Content must be readable in under a second on a cold visit. The prerendered static
  layer is the contract: every page must be complete without the Blazor runtime, which
  never boots on data-saver/2G connections.
- The printed CV is deliberately plain for ATS parsing; every visual idea lives on the
  web page.
- Job-title rule: `profile.title` never claims "Solution Architect" as a current role —
  the experience timeline starts March 2023. AZ-305 status confirmed 2026-09-12: not
  started or paused, so the rule stands unchanged.
- The `mvc-to-webapi-rebuild` case study stays qualitative: no real figure exists for it.
- The site is English-only (the Arabic-RTL work belongs to the Windoor Wizard Builder
  project, presented here as a case study).
- Explicitly undecided: no formal WCAG conformance target has been chosen; no
  headshot/photo policy has been decided.

## Brand Commitments

- Name: Bahaa Aldeen Mohamed. Title: "Senior .NET Engineer — Legacy Modernization &
  Solution Architecture".
- Contacts (fixed): BahaaMohamed37@gmail.com · linkedin.com/in/bahaamohamed-dev ·
  github.com/Bahaa37 · bahaa37.github.io.
- Voice, binding via AGENTS.md/CLAUDE.md: first-person, precise, engineering-grade;
  every claim must be defensible in an interview; explanations lead with why.

## Evidence on Hand

- Full real CV data in `src/Cv.Web/wwwroot/data/cv.json`: four roles (Andalusia
  Business Solutions, PS Digital ×2, MEEM Development), five case studies, two company
  awards, education, and certifications — all real and attributable.
- `testimonials.json` ships empty: no third-party quotes exist yet. Future work must
  not fabricate testimonials, metrics, or awards.
- Static assets in place: favicon, PWA icons, `og-preview.png`; design artboards under
  `design/`.

## Product Principles

1. **Truth over polish.** Nothing may claim more than the timeline proves; a claim that
   cannot be defended in an interview does not ship, and CI enforces the mechanical
   half of that.
2. **The first second belongs to the reader.** Content visible under a second on a
   cold visit; anything that delays first paint is a bug, not a trade-off.
3. **One source of truth.** Every surface is a projection of `cv.json`; content is
   never duplicated.
4. **The site is the work sample.** It runs on the stack being sold, so its engineering
   quality is part of the evidence.
5. **Plain where machines read, expressive where humans look.** The ATS PDF stays
   plain; the web page carries the visual ideas.

## Accessibility & Inclusion

Known requirements: full light/dark theming (system preference plus explicit toggle),
mobile layout verified at 390×844 as well as desktop width, and machine readability of
the PDF (ATS text extraction). No formal WCAG conformance target has been set — open
decision.
