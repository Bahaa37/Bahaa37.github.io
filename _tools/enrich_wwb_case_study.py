"""Sharpen the WWB case study and give it an architecture diagram.

The showcase page is read by people evaluating architecture judgement, so the case study
leads with the decisions rather than the feature list. Full write-up:
docs/writeups/wwb-technical-writeup.md
"""

import json
from pathlib import Path

path = Path("src/Cv.Web/wwwroot/data/cv.json")
doc = json.loads(path.read_text(encoding="utf-8-sig"))

study = next(c for c in doc["caseStudies"] if c["slug"] == "windoor-wizard-builder")

study["title"] = "Windoor Wizard Builder — a fabrication engine that has to be exactly right"

study["summary"] = (
    "A multi-tenant SaaS for Egyptian UPVC window and door workshops, merging a commercial "
    "quoting and production platform with a cutting-optimisation engine verified against a "
    "real shop floor."
)

study["problem"] = (
    "Egyptian UPVC workshops run on WhatsApp, Excel, and paper. Quotes are priced by hand, "
    "cut lists are worked out per job, and the profile offcuts that decide whether a job is "
    "profitable are estimated rather than calculated. Generic ERP does not help because it "
    "does not model the domain — it has no concept of a frame deduction registry, bar "
    "nesting, or the glass area and steel reinforcement that drive real cost. A workshop "
    "running generic software still does the hard part on paper."
)

study["approach"] = (
    "Three decisions carry this system. First, lengths are stored as exact integer tenths of "
    "a millimetre rather than as decimals: the shop cuts half-millimetres — 44 of 195 "
    "verified rows — and a rounded cut list produces a window that does not fit. The value "
    "type deliberately exposes no decimal factory, so rounding cannot enter the model at "
    "all; the wrong thing is unrepresentable rather than merely discouraged. Second, bar "
    "nesting is one-dimensional bin packing, so it uses First-Fit-Decreasing, with the three "
    "details that separate a real implementation from the textbook one: saw kerf charged per "
    "cut, loud failure on a piece longer than a bar rather than a best-effort list that "
    "cannot be executed, and a stable sort so two runs over one order produce identical cut "
    "lists. Every constant — bar length, end trim, kerf, minimum reusable offcut — is "
    "supplied by the caller, so a different workshop is configuration rather than code. "
    "Third, the engine became a bounded context inside the SaaS rather than a service beside "
    "it, because its calculations always run inside a tenant's quote and share that "
    "transaction; a network boundary would have bought overhead and returned nothing. "
    "Tenant isolation is enforced by EF Core global query filters, not by a WHERE clause "
    "every query is trusted to remember."
)

study["outcomes"] = [
    "Two half-built systems merged into one .NET 10 monorepo: the SaaS had a stubbed pricing "
    "engine, the engine had no tenancy or persistence.",
    "491 unit tests passing across domain, application, API, and infrastructure.",
    "Cutting engine oracle-verified against real orders from a working workshop, not against "
    "assumptions derived from the same understanding that wrote the code.",
    "72 pre-existing pricing failures kept and documented as the integration specification "
    "rather than deleted to make the suite green.",
    "Arabic right-to-left throughout, in the interface and in generated PDFs.",
]

study["stack"] = [
    ".NET 10", "Clean Architecture", "MediatR CQRS", "EF Core", "Multi-tenancy",
    "JWT", "QuestPDF", "Angular 18", "NgRx Signals", ".NET Aspire", "Arabic RTL",
]

study["mermaidDiagram"] = (
    "flowchart TB\n"
    "  subgraph Before[\"Two systems, each incomplete\"]\n"
    "    direction LR\n"
    "    S[\"SaaS shell<br/>auth · tenancy · quotes · orders<br/><b>pricing: stubbed</b>\"]\n"
    "    E[\"Fabrication engine<br/>cut lists · nesting · glass · steel<br/><b>storage: JSON files</b>\"]\n"
    "  end\n"
    "  subgraph After[\"One product\"]\n"
    "    direction TB\n"
    "    API[\"WWB.Api\"] --> APP[\"WWB.Application<br/>MediatR · CQRS\"]\n"
    "    APP --> DOM[\"WWB.Domain\"]\n"
    "    APP --> FAB[\"WWB.Fabrication<br/>bounded context\"]\n"
    "    APP --> INF[\"WWB.Infrastructure<br/>EF Core · tenant query filters\"]\n"
    "    FAB -.->|\"tenant-scoped repositories\"| INF\n"
    "  end\n"
    "  Before ==> After"
)

path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

print(f"updated: {study['slug']}")
print(f"  outcomes: {len(study['outcomes'])}")
print(f"  diagram:  {'yes' if study.get('mermaidDiagram') else 'no'}")
print(f"  diagrams across all case studies: "
      f"{sum(1 for c in doc['caseStudies'] if c.get('mermaidDiagram'))}/{len(doc['caseStudies'])}")
