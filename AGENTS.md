# AGENTS.md

Portfolio/CV site for bahaa37.github.io — Blazor WebAssembly on .NET 10, published as
static files. Read `CLAUDE.md` before touching anything non-trivial; it explains the
reasoning behind the rules below.

## Layout

```
src/Cv.Domain/        Records and value objects. No dependencies.
src/Cv.Application/   Derived values, validation, serialization.
src/Cv.Web/           Blazor WASM host, components, wwwroot/data/cv.json.
tests/Cv.Tests/       Unit tests, run against the real cv.json (not fixtures).
_tools/               Python: PDF render, ATS check, prerender, local publish server.
docs/content/         GITIGNORED — candid career material. Never commit anything from it.
```

## Commands

```bash
dotnet test tests/Cv.Tests/Cv.Tests.csproj
dotnet run --project src/Cv.Web/Cv.Web.csproj        # → http://localhost:5046

dotnet publish src/Cv.Web/Cv.Web.csproj -c Release -o publish
python _tools/make_cv_pdf.py publish/wwwroot publish/wwwroot/Bahaa-Aldeen-Mohamed-CV.pdf
python _tools/ats_check.py  publish/wwwroot/Bahaa-Aldeen-Mohamed-CV.pdf
python _tools/prerender.py  publish/wwwroot --base-url https://bahaa37.github.io
python _tools/serve_publish.py 5210 publish/wwwroot
```

The publish order is load-bearing: `prerender.py` refuses to finish unless the CV PDF
already exists in the published output. Requires Python `playwright` + `pypdf` and
`python -m playwright install chromium`. CI (`.github/workflows/ci.yml`, `pages.yml`)
runs the same steps; deploys gate on all of them.

## Non-negotiable rules

- `wwwroot/data/cv.json` is the single source of truth. The showcase page, printable CV,
  and `CvValidator` are projections of it — never put content anywhere else.
  `data/decisions.json` (ADRs) is deliberately separate.
- Content rules fail the build on purpose: overlapping full-time roles, technology claimed
  before its release date, and malformed ADRs. Unquantified achievements warn, never
  auto-fill — no fabricated numbers.
- Cache-busting is manual. Anything new fetched by a bare path needs `?v=<hash>` (done in
  `prerender.py`, which also stamps and registers `service-worker.js` — in dev it is
  never registered) or `BrowserRequestCache.NoCache` (see `CvDataService`). The service
  worker serves `/_framework/` and `?v=` URLs cache-first (immutable by fingerprint) and
  keeps `/data/` strictly network-first.
- Blazor boots deferred: `autostart="false"`, started on idle by `js/boot.js`, skipped
  entirely on data-saver/2G connections (ADR-0007). The static layer is the contract —
  every page must be complete without the runtime. That includes the header: the
  prerendered header in `prerender.py` (`static_shell_header` + `NAV_LINKS`) duplicates
  `MainLayout.razor`'s on purpose; change them together or pre- and post-boot chrome
  diverges.
- Motion is additive: `motion.js` is the only thing that applies hiding classes. Never
  write an unconditional `opacity: 0` — invisible-content bugs happened three times.
- No CSS framework. Dark tokens are written twice (`prefers-color-scheme` and
  `[data-theme="dark"]`) — change both. Component-owned looks use CSS isolation;
  shared long-form layout lives in `app.css`.
- Never commit anything from `docs/content/` or any target-company/salary material —
  public repo.

## Deliberate decisions — do not "fix"

- Blazor WASM stays; the site is itself a work sample. But the runtime's size is a
  budget, not an excuse: **content must be visible in under a second on a cold
  visit.** That is why every route ships prerendered HTML in `#app` (see
  `prerender.py`), why `app.css` is inlined into the shell at publish time (a
  render-blocking stylesheet is the last thing between HTML arriving and first
  paint), why the Google Fonts stylesheet and the CSS-isolation bundle load
  non-blocking, and why the two heaviest framework files are `<link
  rel="preload">`ed from the shell. Anything that delays first paint is a bug, not
  a trade-off. One invariant to protect: the prerendered `<div class="prerendered">`
  must be a DIRECT child of `#app` — a regex drift once nested it inside
  `.loading-progress-text`, which the CSS hides, blanking every page until boot.
  `prerender.py` now refuses such output.
- `profile.title` never claims "Solution Architect" as current — the timeline starts
  March 2023. Revisit only after AZ-305 is passed.
- The printed CV is deliberately plain (ATS parsing); visual ideas live on the web page.

## Verification

CI cannot see unstyled buttons or dead links. Run the app and check `/`, `/cv`,
`/work/{slug}` and `/architecture` at 390×844 and desktop width, in both themes, before
calling anything done.
