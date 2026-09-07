# bahaa37.github.io

The source of my portfolio and CV — [bahaa37.github.io](https://bahaa37.github.io).

I build .NET systems and lead legacy modernization, so the site is a .NET application
rather than a template: it is meant to be readable as a work sample, not just to display
one.

## The idea

There is **one data file and three readers of it**.

```
wwwroot/data/cv.json          the single source of truth
        │
        ├── Print renderer    →  the CV that gets sent to employers
        ├── Showcase page     →  the interactive portfolio
        └── Validation        →  content rules enforced in CI
```

Adding a role is one edit. The alternative — a PDF and a website maintained separately —
drifts apart within a month.

## The constraint that shaped the design

The PDF is machine-parsed by applicant tracking systems. Multi-column layouts, icon
fonts, tables, and text inside graphics all break that parsing, so **the CV and the
website are designed in opposite directions**: every visual idea lives on the web page,
and the printed CV is deliberately plain.

That is not a claim, it is a test. `_tools/ats_check.py` extracts the generated PDF's
text layer and asserts that every section heading, employer, contact detail, and key
metric comes out readable and in document order. If the extractor cannot read it,
neither can an ATS.

## Content rules run in CI

`CvValidator` treats CV defects as build failures rather than proofreading:

- **Overlapping full-time roles** — two full-time jobs cannot run concurrently, and a
  reader who spots it reads carelessness.
- **Anachronistic technology claims** — a bullet naming a .NET version released after
  the role ended fails the build. The original CV had exactly this.
- **Unquantified achievements** — flagged, never auto-filled. A fabricated number cannot
  be defended in an interview.

Deploys are gated on these, so a broken timeline cannot reach a recruiter.

## Stack

**Blazor WebAssembly on .NET 10**, published as static files to GitHub Pages.

Chosen over server-rendered ASP.NET Core for one reason: every free .NET server tier
cold-starts, and a recruiter waiting fifteen seconds on a blank page is a cost worth
avoiding. Static hosting has no such failure mode while keeping the stack entirely C#.

Full trimming plus invariant globalization brings the payload to ~1.6 MB Brotli. Mermaid
is ~3.5 MB, so it loads only when a diagram is opened — never on first paint.

## Layout

```
src/Cv.Domain/        Records and value objects. No dependencies.
src/Cv.Application/   Derived values, validation, serialization.
src/Cv.Web/           Blazor WebAssembly host, components, cv.json.
tests/Cv.Tests/       Unit tests, including tests over the real cv.json.
_tools/               ATS check, PDF generation, local publish server.
design/               Design canvas artboards.
```

## Running it

```bash
dotnet test tests/Cv.Tests/Cv.Tests.csproj
dotnet run --project src/Cv.Web/Cv.Web.csproj     # → http://localhost:5199
```

Regenerating the CV PDF and checking it against the ATS gate:

```bash
dotnet publish src/Cv.Web/Cv.Web.csproj -c Release -o publish
python _tools/serve_publish.py 5210 publish/wwwroot
chrome --headless --print-to-pdf=output/cv.pdf http://localhost:5210/cv
python _tools/ats_check.py output/cv.pdf
```

## Contact

[BahaaMohamed37@gmail.com](mailto:BahaaMohamed37@gmail.com) ·
[LinkedIn](https://linkedin.com/in/bahaamohamed-dev)
