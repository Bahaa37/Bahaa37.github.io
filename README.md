# Bahaa Aldeen Mohamed

**Senior .NET Engineer** · Alexandria, Egypt (EET, full overlap with EU hours)

[bahaa37.github.io](https://bahaa37.github.io) · [Download my CV (PDF)](https://bahaa37.github.io/Bahaa-Aldeen-Mohamed-CV.pdf) · [LinkedIn](https://linkedin.com/in/bahaamohamed-dev)

Hi, I'm Bahaa. I build .NET systems and I'm happiest with the ones other people are scared to
touch. I'm open to remote senior .NET and architecture roles.

## A few things I've built

- **Payments for 9 countries.** I designed and wrote the payment middleware behind Texas Chicken:
  seven gateways behind one stateless API, one adapter per gateway, no database. It shipped in
  about a month.
- **A legacy estate that could finally move.** I led the removal of a distributed transaction
  coordinator that had pinned a .NET platform to old runtimes. The AI-guided workflow I built for
  the migration took an upgrade cycle from 5-7 working days down to 3, and it won a company award.
- **A multi-tenant SaaS, written down first.** My current side project isolates tenants in four
  separate layers (auth claim, EF Core filters, PostgreSQL row-level security, a save interceptor),
  and every structural decision has an ADR.

The full stories, with the trade-offs, are on the site.

## About this repo

The site is a Blazor WebAssembly app on .NET 10, built and deployed by GitHub Actions to
GitHub Pages. I could have used a template; I wanted the portfolio itself to be a piece of work
you can read.

- **One JSON file drives everything.** `cv.json` feeds the website, the printable CV and the
  content checks, so the site and the PDF can't drift apart.
- **The CV has tests.** The build fails on overlapping full-time jobs, on a .NET version claimed
  before it existed, and if an applicant tracking system can't read the generated PDF.
- **Every page is prerendered** with its own title, description and structured data, so search
  engines and AI crawlers that don't run WebAssembly still get the content.

## Security

I treated this like a production repo:

- **No personal data in the code.** My email and phone number are stored as encrypted Actions
  secrets and injected at build time. The source and its history only contain placeholders, and
  the build refuses to deploy if a secret is missing.
- **A tight pipeline.** The workflow token is read-only, only GitHub-owned or verified actions can
  run, and outside contributors need approval before any workflow runs.
- **Protected repo.** Secret scanning with push protection, Dependabot security updates, and a
  `main` branch that can't be force-pushed or deleted.

## Running it

```bash
dotnet test tests/Cv.Tests/Cv.Tests.csproj
dotnet run --project src/Cv.Web/Cv.Web.csproj     # http://localhost:5046
```

## Get in touch

Use the contact bar on [bahaa37.github.io](https://bahaa37.github.io) (call, WhatsApp, email or
download the CV), or message me on [LinkedIn](https://linkedin.com/in/bahaamohamed-dev).
