---
target: critic of the Frosted Keynote redesign as shipped
total_score: 30
max_score: 40
na_heuristics: 
p0_count: 1
p1_count: 2
target_identity: "file:C:\\Users\\bahaa\\OneDrive\\Desktop\\My Resume Project\\src\\Cv.Web\\Pages\\Home.razor"
target_fingerprint: "sha256:fbf28edb3ea2b06b9ef6cc2397478d8b5451bc3c388543ca445e8ad795a93937"
target_path: "C:\\Users\\bahaa\\OneDrive\\Desktop\\My Resume Project\\src\\Cv.Web\\Pages\\Home.razor"
timestamp: 2026-09-13T07-20-12Z
slug: src-cv-web-pages-home-razor
---
# Impeccable critique — Frosted Keynote as shipped

Method: dual-agent (A: agent_1b951f34 · B: agent_aa0fd870)
Target: src/Cv.Web/Pages/Home.razor (canonical) — routes: / , /work/legacy-modernization , /testimonials
Date: 2026-09-13 · Evidence: .impeccable/review/critique2 (53 tiles; mobile-light tiles rendered dark by capture mistake — mobile findings are dark-theme)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | No current-section state in nav on an 11,000px page |
| 2 | Match System / Real World | 4 | Engineering-grade, defensible, DTC metaphor carried by the diagram |
| 3 | User Control and Freedom | 3 | Dense sections cannot collapse |
| 4 | Consistency and Standards | 4 | Outcome block tinted on home, plain on study pages; two near-identical CV exits |
| 5 | Error Prevention | 3 | Little error-prone action exists |
| 6 | Recognition Rather Than Recall | 3 | No scrollspy across 13 tiles of scroll |
| 7 | Flexibility and Efficiency | 2 | No back-to-top; chip evidence title-only |
| 8 | Aesthetic and Minimalist Design | 2 | Material restraint high, information design not minimal (~60 chips, ~26 flat bullets, 17 certs, 7 primaries) |
| 9 | Error Recovery | 3 | Mermaid falls back to source; honest empty state |
| 10 | Help and Documentation | 3 | Copy self-documents |

**Total 30/40 — Good** (was 28/40 pre-redesign).

## Verdict summary

Authored, not a template — specific in the evidence system (evidenced chips, mono facts line, performing diagram, single gold, honesty made perceptible). Category-generic one layer down: ~11,000px home at uniform density. "The material system over-delivers on surfaces and under-delivers on behavior." Rhythm = "a metronome with two loud bookends."

## Priority issues

1. **[P0] Mobile chrome tax** — 3-row sticky capsule ~165px for a 21-tile scroll. Fix: single 56px row + horizontal-scroll nav; scroll-margin 216→~76px (coupling rule).
2. **[P1] No skim layer** — equal-weight bullets/certs/chips; positioning pillars have no priority. Fix: 3 highlights + "Show all N" (no-JS), "12 more" certs, skill matrix split Architecture / AI-and-Delivery + "Also".
3. **[P1] Primary-action inflation** — 7 solid-blue buttons per page. Fix: per-case CTAs to ghost/arrow; one primary per viewport.
4. **[P2] Dark loses the diagram stage** — no separation in dark. Fix: lift stage gradient/alphas in both dark token blocks.
5. **[P2] Case-study click betrays its promise** — home carries full prose. Fix: home = summary + tinted outcome + CTA; prose on study pages; tint study outcomes too.

Premium sweep: hero facts line stray middot wrap (desktop) + mid-unit break (mobile); aurora near-invisible in light mode; empty testimonials room undesigned; chips ragged heights + evidenced tint dilution (~40% tinted); footer sits on loudest dark blob; hero sheet +6rem width reads as misalignment; two identical "Senior Full-Stack Software Engineer" titles read as duplication.

## Personas (red flags)

- Screening recruiter: no authored path to the two positioning claims; outcomes below prose; 5 identical CTAs; 17 certs dilute seniority.
- Casey (390px): capsule tax ~20% of every screen; 4 consecutive chip screens; CTA ~19 tiles down.
- Sam: diagram is a screen-reader run-on, blocker meaning color-only; Mermaid SVG inaccessible; chip evidence title-only.

## Detector (B)

70 source-only findings (57 advisory / 13 warning): design-system doc scope (stage palette, print-CV Georgia + print colors, code syntax colors, og card sizes), og.html gradient false-positives ×9, Geist overused-font ×1. No contrast or slop findings in shipped pages — issues are compositional, not mechanical.

## Provocative questions

1. Could a recruiter recite the two positioning claims after reading only hero + outcomes? Why is that evidence at equal weight?
2. Dosage enforced on bytes (Mermaid 3.5MB deferred) but not attention — is backdrop-filter the only rationed thing?
3. If the aurora field were deleted, how much of the light-mode identity would survive? Should a named element be visible enough to earn the name?
