---
target: src/Cv.Web/Pages/Home.razor
total_score: 25
max_score: 36
na_heuristics: 10
p0_count: 0
p1_count: 2
target_identity: "file:C:\\Users\\bahaa\\OneDrive\\Desktop\\My Resume Project\\src\\Cv.Web\\Pages\\Home.razor"
target_fingerprint: "sha256:e3a41872d5926f528f0bc165caa78992f413e4c5c6244bb59ef53e752f3ef62b"
target_path: "C:\\Users\\bahaa\\OneDrive\\Desktop\\My Resume Project\\src\\Cv.Web\\Pages\\Home.razor"
timestamp: 2026-09-24T20-59-29Z
slug: src-cv-web-pages-home-razor
---
---
target: critic of the Sky Aluminum world as shipped (post clarify copy pass)
total_score: 25
max_score: 36
na_heuristics: 10
p0_count: 0
p1_count: 2
target_identity: "file:C:\Users\bahaa\OneDrive\Desktop\My Resume Project\src\Cv.Web\Pages\Home.razor"
target_fingerprint: "sha256:PENDING"
target_path: "C:\Users\bahaa\OneDrive\Desktop\My Resume Project\src\Cv.Web\Pages\Home.razor"
timestamp: 2026-09-24T00:00:00Z
slug: src-cv-web-pages-home-razor
---
# Impeccable critique — Sky Aluminum as shipped

Method: dual-agent (A: design-review subagent, unanchored · B: detector + browser-overlay subagent).
Target: src/Cv.Web/Pages/Home.razor — routes /, /cv, /work/*, /testimonials. Date: 2026-09-24.
Evidence: .impeccable/review/critique3 (6 full-page captures) + agent mobile slices + overlay injection on 3 routes.

## Design Health Score

#10 n/a (no help surface on a reading portfolio); applicable max 36. Total 25/36 — Acceptable (69%).
Trend caution: prior runs scored /40 (28, 30); this run's agent was stricter — not like-for-like.

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | No current-section state in nav on a ~13,500px page |
| 2 | Match System / Real World | 3 | "3 days max" beside "Distributed Transaction Coordinator" — register shifts |
| 3 | User Control and Freedom | 3 | No back-to-top on the long mobile page |
| 4 | Consistency and Standards | 3 | Mermaid legibility varies per card; hero and contact swap primary action |
| 5 | Error Prevention | 3 | No input surfaces; existing guards correct |
| 6 | Recognition Rather Than Recall | 2 | 390px nav clips "Credentials" mid-word, hides "CV" entirely |
| 7 | Flexibility and Efficiency | 2 | Only accelerators are skip link and dock |
| 8 | Aesthetic and Minimalist Design | 3 | Work section over-stacks (summary+outcome+tags+buttons+diagram x5) |
| 9 | Error Recovery | 3 | Prerendered layer survives failed boot; 404 ships with chrome |
| 10 | Help and Documentation | n/a | No help surface exists |

## Design Specificity Verdict

Authored, not a template, in the places that matter most: hero carries the actual before/after DTC
orchestration diagram; skill chips carry employer citations; gold confined to awards. Drifts
category-generic mid-page: five structurally identical case cards, standard contact block/footer;
personal project wears same chrome as employer work.

Deterministic scan (source-only, obj/ and mermaid excluded): 101 findings — 5 warning / 96 advisory,
0 blocking. Real: ~85-90 char line measures on ledes/case summaries; 35 em-dashes in /cv body;
55 CSS values undocumented in DESIGN.md (token drift, mostly anodized alpha tints/shadow hexes);
og.html gold #e0b95f on sky #dbf1ff at 1.6:1 (card-internal only).
False positives dismissed: Geist "overused" (documented primary), thin-border-wide-shadow on the two
deliberate glass surfaces, Georgia in print CSS (ATS rule), og.html design-system set, 87% obj//mermaid noise.
Overlays: injection succeeded 3/3 pages (15/5/6 in-page findings, matching CLI set).

## Overall Impression

First viewport is the strongest thing on the site (claim + proof-diagram + numbers in one fixation
path). Valley is the middle: five same-shaped cards, same blue Outcome tint, 3-day metric repeated
four times — reads as padding by card three. End is functionally right, ceremonially dull.

## What's Working

1. The hero diagram is the thesis — the DTC story as argument, with a real text alternative.
2. Evidenced skill chips — employer citations; two-tier disclosure serves positioning pillars.
3. Trust engineering — final values in markup, no autofill, gold scarcity kept meaningful.

## Priority Issues

1. [P1] Mobile nav truncates the CV path — "Credentials" clipped mid-word, "CV" off-screen past the
   mask at 390px. Fix: shorten labels <=720px, move CV early, visible chevron affordance. ($adapt)
2. [P1] Five equal case cards dilute the signature story — DTC pillar carries same weight as routine
   MVC rebuild; >4-way equal choice. Fix: featured DTC panel + compact 4-index (title/org/one-liner/
   outcome chip/link). ($layout/$distill)
3. [P2] Headline line-break drift — "that froze the estate." wraps to a 4th line at 1280 and 390,
   orphaning "the estate.". Fix: tune clamp or split third span. ($typeset)
4. [P2] Email-as-primary-button — raw address only, no verb/icon; may be copied not tapped. Fix:
   "Email" + envelope icon, address secondary. ($clarify)
5. [P2] Overlay and legibility at the extremes — dock covers footer's last line at scroll end
   (padding < dock height); payment card Mermaid labels ~8px on desktop. ($adapt)

## Persona Red Flags

- Screening recruiter: "3.5+ years across 3 employers" headline invites discount; Download CV only
  ~13,000px down on mobile; 3-day metric x4 reads as inflation; contact button no action cue.
- Casey (390px): nav hides CV; dock overlays footer last line; hero actions wrap raggedly; facts
  line breaks mid-fact with stranded middots.
- Sam (SR/keyboard): aria-label on <p class="hero__facts"> unreliable naming; count-up mutates text
  without aria-live governance; chip evidence leans on title; theme toggle precedes nav in focus order.

## Minor Observations

"The CV is this page's content..." clunky; "2 awards, one a company award" forces re-read; counter
animates 7->3 showing the bad number first; mono facts row and footer dimmest dark-theme text; no
current-section state on desktop either.

## Questions to Consider

1. Is "3.5+ years across 3 employers" serving the positioning, or feeding the skeptic's filter?
2. Is "Selected work" a menu or a memoir — what would 1-featured-plus-4-index cost?
3. "The CV is this page's content" vs a separate /cv route still fights — which truth to tell?
