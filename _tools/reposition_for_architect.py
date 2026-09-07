"""Reposition the CV toward systems analysis and architecture roles.

The target changed from "senior engineer" to "systems analyst / architect". That is a
content decision, not a wording tweak: skill groups render top-down, so what sits first
is what a reader sees first. Architecture and analysis move above languages.

No facts are added. Bullets are re-framed to foreground the design and analysis work
that was already there but buried.
"""

import json
from pathlib import Path

path = Path("src/Cv.Web/wwwroot/data/cv.json")
doc = json.loads(path.read_text(encoding="utf-8-sig"))

# --- Profile ---------------------------------------------------------------------

doc["profile"]["title"] = "Senior .NET Engineer — Solution Architecture & Systems Analysis"

# A URL printed on a CV cannot be changed after it has been emailed, so it must read as
# permanent. A GitHub Pages user site is free, predictable, and serves at the domain root
# (no base-href rewriting), unlike an Azure Static Web Apps free-tier random subdomain.
doc["profile"]["website"] = "https://bahaa37.github.io"

doc["summary"] = (
    "Software architect and systems analyst working in the .NET ecosystem, with a track "
    "record of taking architectural decisions on systems that were considered too risky "
    "to change. Led the re-architecture of a distributed orchestrator to remove its "
    "transaction-coordinator dependency — the constraint that had frozen an entire service "
    "estate on unsupported runtimes — then authored the transformation template, its "
    "governing rules, and the AI-guided workflow that let other teams repeat it. A single "
    "upgrade cycle fell from 5-7 working days to a maximum of 3, with a company award for "
    "the time and cost saved. Designs and documents systems as well as building them: "
    "solution architecture documents, SRS and low-level design, and Mermaid workflow "
    "modelling. Architected payment middleware serving 9 countries on Clean Architecture "
    "with CQRS, Strategy, and Pipeline. Separately awarded as a subject matter expert for "
    "AI enablement across non-technical departments. Completing diplomas in microservices "
    "architecture and Azure, and targeting systems analysis and architecture roles."
)

# --- Skill groups ----------------------------------------------------------------

analysis_group = {
    "category": "Systems Analysis & Design",
    "skills": [
        "Solution architecture documents",
        "Software Requirements Specification (SRS)",
        "Low-Level Design (LLD)",
        "Architecture diagrams",
        "Workflow and sequence modelling",
        "Mermaid diagramming",
        "Requirements analysis",
        "Cross-team technical facilitation",
    ],
}

by_category = {g["category"]: g for g in doc["skillGroups"]}
by_category[analysis_group["category"]] = analysis_group

# Architecture and analysis lead; implementation detail follows.
order = [
    "Architecture & Patterns",
    "Systems Analysis & Design",
    "Legacy Modernization",
    "AI Engineering & Enablement",
    "Languages & Frameworks",
    "Data & Messaging",
    "Cloud & DevOps",
    "APIs & Integration",
    "Frontend",
    "Practice & Documentation",
]

missing = [c for c in by_category if c not in order]
if missing:
    raise SystemExit(f"Skill groups not covered by the ordering list: {missing}")

doc["skillGroups"] = [by_category[c] for c in order if c in by_category]

# "Practice & Documentation" duplicated what the new analysis group now says better.
practice = by_category.get("Practice & Documentation")
if practice:
    practice["skills"] = [
        s for s in practice["skills"]
        if s not in {"Solution architecture documents", "SRS & LLD authoring", "Mermaid diagrams"}
    ]

# --- MEEM: re-framed as the analysis role it actually was -------------------------

meem = next(e for e in doc["experience"] if e["company"] == "MEEM Development")
meem["role"] = "Backend Software Engineer"
meem["highlights"] = [
    {
        "text": "Produced solution architecture documentation — architecture diagrams and "
                "workflow designs — used by delivery teams as the reference for build work.",
        "tags": ["Architecture", "Documentation", "Systems Analysis"],
        "isFeatured": True,
    },
    {
        "text": "Authored Software Requirements Specification (SRS) and Low-Level Design (LLD) "
                "documents, translating business requirements into unambiguous technical "
                "specifications that teams could implement without re-interpretation.",
        "tags": ["SRS", "LLD", "Systems Analysis", "Requirements"],
        "isFeatured": True,
    },
]

path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

print(f"title:   {doc['profile']['title']}")
print(f"website: {doc['profile']['website']}")
print("skill groups, in render order:")
for group in doc["skillGroups"]:
    print(f"  - {group['category']}")
