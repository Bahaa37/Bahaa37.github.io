# Working in this repository

The README explains the architecture for a reader. This file covers what is easy to get
wrong, and the decisions that look like oversights but are not.

## Build and verify

```bash
dotnet test tests/Cv.Tests/Cv.Tests.csproj
dotnet run --project src/Cv.Web/Cv.Web.csproj        # → http://localhost:5046
```

The publish path, **in this order**:

```bash
dotnet publish src/Cv.Web/Cv.Web.csproj -c Release -o publish
python _tools/make_cv_pdf.py publish/wwwroot publish/wwwroot/Bahaa-Aldeen-Mohamed-CV.pdf
python _tools/ats_check.py  publish/wwwroot/Bahaa-Aldeen-Mohamed-CV.pdf
python _tools/prerender.py  publish/wwwroot --base-url https://bahaa37.github.io
python _tools/serve_publish.py 5210 publish/wwwroot
```

**The order is load-bearing.** `prerender.py` refuses to finish unless the CV PDF is
already in the published output, so rendering the PDF second fails the build. This is
exactly how it was written the first time, and CI caught it.

Requires `playwright` and `pypdf`, plus `python -m playwright install chromium`.

`.github/workflows/ci.yml` runs all of this on every branch and pull request.
`pages.yml` runs it again on `main` and deploys. Neither publishes anything if a gate fails.

## Things that will bite

**Two publish-time guards live in `_tools/prerender.py`.** Both catch defects that look
fine in a browser:

- Every route must have its own title, description and canonical. The site once served
  three routes with byte-identical metadata, which made it one page to every crawler.
- The CV PDF must exist in the published output and be a plausible size. Two pages link to
  it, and a missing file on GitHub Pages is served as the 404 page — so the link does not
  break visibly, it just stops being a CV.

**Cache-busting is manual, and there are now three layers of it.** Only `_framework/*`
fingerprints itself. Head assets (the kit's two files included) get `?v=<content hash>` appended by `prerender.py`;
`data/cv.json` and `data/testimonials.json` are fetched with `BrowserRequestCache.NoCache` in
`CvDataService`; and `service-worker.js` sits underneath both — cache-first for `_framework`
and any `?v=` URL (immutable by construction), strictly network-first for `/data/` and page
navigations, so it can never serve a stale CV. It is stamped and registered by
`prerender.py` at publish time and never registered in development.

**Anything new fetched by a bare path inherits the bug all of this exists to fix** —
returning browsers running new code against an old stylesheet and an old CV. Known accepted
exception: the three JS modules imported from C# by literal path (`js/motion.js`,
`js/diagram-interop.js`, `js/styleguide.js`), which change rarely.

**The prerendered page is the product, not a placeholder.** `boot.js` starts Blazor on idle
with `autostart="false"`, and skips it entirely on data-saver or 2G connections.
So for some visitors the runtime never boots at all. Anything a reader must be able to do
has to work in the static layer — which is why `prerender.py` injects a static copy of the
theme switch that the inline script in `index.html` wires up by delegation, and why Blazor
replacing `#app` on boot silently takes that duty over. The switch is a tap-first control
by design: the drag (knob past the midpoint) and the ripple (`.theme-pulse`) are
enhancements layered on top of a plain button — never the only path. If you add
interactive chrome, either give it a static counterpart or accept that those visitors
never get it.

**The handover is one swap, never a gap.** Every page's first Blazor render is a
"Loading…" placeholder (`.booting`/`.loading`) while `cv.json` is fetched. So `boot.js`
moves the static page out of `#app` into `#app-static` before starting the runtime, lets
Blazor render into a hidden `#app`, and swaps in one synchronous step only when that render
has an `h1` and no placeholder — then `Hairline.settle()` shows on-screen reveals without
fading. A page whose loading state lacks one of those classes, or that renders no `h1`,
never hands over (the static page just stays). Entrances (`.hl-enter`) play once per load:
`html.hl-entered` switches them off for every later render.

**The static layer mirrors more than the chrome now.** Besides the header and dock,
`prerender.py` renders its own copies of the hero console, the `#skills` tabs, the
`/styleguide` page and the 404 console, so they work for visitors whose runtime never boots
(`kit/hairline.js` drives them pre-boot). Each Razor/Python pair says "change both":
`CaseStudyConsole.RunLines` ↔ `_console_run_lines`, and `SkillEvidence.cs` ↔ its
line-for-line Python port. Scoped `.razor.css` cannot reach these static copies, which is
why their styles live unscoped in `app.css`.

**Motion is additive, always.** `motion.js` and the kit (`html.hl-motion`, added only when
IntersectionObserver exists and reduced motion is off) are the only things that apply
hiding classes, so a script failure can never leave content invisible. Three separate bugs in this project's
history were content that was present, selectable and invisible. Never write an
unconditional `opacity: 0`.

**Adding a route** costs nothing extra: `prerender.py` derives the route table from
`cv.json` and `testimonials.json`, and the sitemap, `llms.txt` and 200-status materialization
all follow from it. There is no hand-maintained list to update any more.

## Data

`src/Cv.Web/wwwroot/data/cv.json` is the single source of truth. The showcase page, the
printable CV and `CvValidator` are three projections of it; none holds content of its own.

`data/testimonials.json` is deliberately separate — recommendations are a different
document for a different audience, and nothing in them belongs on a printed CV or in an
ATS. It ships empty: an honest "no recommendations yet" beats an invented quote.

Tests run against the real data files, not fixtures. `TestimonialRecordTests` enforces that
every entry carries a real name, real words, and an absolute LinkedIn or GitHub URL — a
reader can check that the person exists and actually said it. An unattributable quote fails
the build on purpose: on a page whose subject is honest reasoning, a bad quote is worse
than no quote.

`CvValidator` fails the build on overlapping full-time roles and on technology claimed
before its release date. Unquantified achievements are warnings, never auto-filled — a
fabricated figure cannot be defended in an interview.

## Decisions that are not oversights

**The job title.** `profile.title` says *Senior .NET Engineer — Legacy Modernization &
Solution Architecture*, and the site never claims "Solution Architect" as a current role.
That is deliberate: the experience record starts March 2023, and a title the timeline
contradicts costs the screen it was meant to win. Revisit when AZ-305 is passed.

**`docs/content/` is gitignored** and holds candid career material — job-search strategy,
worksheets, framing notes. This is a public repository. Never commit anything from it, and
never put a target-company list or a salary posture anywhere tracked.

**Blazor WebAssembly stays.** The ~1.6 MB payload is the known cost; the trimming rationale
is in `Cv.Web.csproj`. "This site is itself a work sample" only holds while it remains in
the stack being sold.

**No CSS framework; the design system is Hairline, vendored.** Tokens (`--hl-*`), components
(`hl-*`) and the motion engine live in the private repo `bahaa37/hairline-kit` (kept separate
so other projects, Angular first, can reuse it). They are copied into `wwwroot/kit/` by
`python _tools/sync_kit.py <kit-path>`, which builds the kit and writes `kit/VERSION`. Never
hand-edit `wwwroot/kit/`: change the kit, push it, sync. `prerender.py` versions both kit
files and inlines `kit/hairline.css` ahead of `app.css` into first paint.

The kit is dark by default; its light tokens are written twice — under `prefers-color-scheme:
light` guarded with `:not([data-theme="dark"])`, and under `[data-theme="light"]` — so an
explicit choice and the system default both work. Plain CSS cannot share one declaration list
between them; change both.

The old Edge WebView constraint holds: no `color-mix()`, no individual
`translate`/`rotate`/`scale` properties (the kit's build fails on them). `backdrop-filter`
appears once, on the header and dock, and only inside `@supports`, over an opaque fallback.

`app.css` reads `--hl-*` directly and defines only layout tokens of its own (`--measure`, the
header and dock clearances). CSS isolation is right for a component that owns its look and
wrong for a layout several pages share, and it cannot reach the prerendered static copies, so
long-form and mirrored styles live in `app.css`. `/cv`'s document is white paper in both
themes: `PrintCv.razor.css` pins its heading and link colours on screen only, so the PDF is
untouched.

## Considered and rejected

These were planned and deliberately dropped. The reasons matter more than the decisions —
without them the next person rebuilds work that was already thought through and discarded.

**Cross-document view transitions.** Blazor WebAssembly routes client-side, so
`@view-transition` never fires for in-app navigation. It would be dead CSS that looks
modern in a diff and does nothing on the site.

**Container queries on `CaseStudyPanel` / `SkillMatrix`.** Those components render at one
width, in one column. Converting them is churn with no visible change.

**Scroll-driving the hero before/after diagram.** It is not static — `Hero.razor.css`
carries a choreographed ~2.5 second sequence in which the legacy estate builds, the blocker
is flagged, the bridge draws, the modernized services arrive, and only then does the blocker
dissolve. A hero is already in view on load; scroll-linking it would be a downgrade, not a
modernization.

**A `testimonials: []` stub in `cv.json`.** An unrendered schema field is dead weight. The
full `Testimonial` record arrived with the feature that renders it, in its own curated
`data/testimonials.json`.

**A number on the `mvc-to-webapi-rebuild` case study.** Every other case study carries one;
this one does not, because no real figure exists. `CvValidator` flags unquantified
achievements as a warning and never auto-fills them for exactly this reason — a fabricated
number cannot be defended in an interview. Leave it qualitative.

## Style

Comments explain *why*, not *what* — the reasoning that would otherwise be lost, the
alternative that was rejected, the bug a line prevents. Match the density already present;
it is deliberately high in the places where the reasoning is not recoverable from the code.

Commit messages follow the same rule: what changed, and what it was for.

## Verification discipline

CI cannot see an unstyled button or a dead link. Phases 1–4 of this work were verified
entirely through CI and never looked at, and two defects reached production as a result —
a theme toggle rendering as a grey bar, and a download link that did nothing.

Run the app. Open the pages. Check `/`, `/cv`, `/work/{slug}`, `/testimonials` and `/styleguide` at 390×844
and at desktop width, in both themes, before calling anything done.
