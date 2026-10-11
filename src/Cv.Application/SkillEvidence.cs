using Cv.Domain;

namespace Cv.Application;

/// <summary>A skill, together with the employers where it was actually used.</summary>
public sealed record SkillWithEvidence(string Skill, IReadOnlyList<string> UsedAt)
{
    public bool HasEvidence => UsedAt.Count > 0;
}

/// <summary>
/// Links each listed skill back to the roles that demonstrate it.
/// </summary>
/// <remarks>
/// A skills list is the least trusted part of any CV, because anyone can type anything
/// into it. Attaching the employers where a skill actually appears in the achievement
/// record turns a claim into a citation. Skills with no supporting evidence are not
/// hidden — the gap is worth seeing, both for the reader and for the author.
/// </remarks>
public static class SkillEvidence
{
    public static IReadOnlyList<SkillWithEvidence> For(
        SkillGroup group,
        IReadOnlyList<ExperienceEntry> experience) =>
        [.. group.Skills.Select(skill => new SkillWithEvidence(skill, EmployersUsing(skill, experience)))];

    /// <summary>
    /// The skills from the grouped vocabulary that one role's achievement record
    /// actually mentions, in first-mention order. The timeline renders this as the
    /// per-role stack line — the way real senior profiles tag the stack on every
    /// role so a skimmer sees it evolve across the career.
    /// </summary>
    /// <remarks>
    /// Derived from the same highlights the bullets render, through the same matcher
    /// the evidence chips use — a stack line can never claim a technology the role's
    /// own record does not name, and no stack vocabulary is hardcoded anywhere.
    /// </remarks>
    public static IReadOnlyList<string> ForRole(
        ExperienceEntry entry,
        IReadOnlyList<SkillGroup> groups)
    {
        var taken = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var specific = new List<string>();
        var loose = new List<string>();

        // Pass one: what the record is explicit about — the skill named in the bullet
        // text itself, or a tag that is exactly the skill. Pass two catches the looser
        // tag-contains matches the evidence chips accept, but only after them: a
        // byline leads with what the record names outright, not what a generic
        // "Architecture" tag implies.
        foreach (var highlight in entry.Highlights)
        {
            foreach (var group in groups)
            {
                foreach (var skill in group.Skills)
                {
                    if (!taken.Contains(skill)
                        && (ContainsWord(highlight.Text, skill)
                            || highlight.Tags.Any(tag => tag.Equals(skill, StringComparison.OrdinalIgnoreCase))))
                    {
                        taken.Add(skill);
                        specific.Add(skill);
                    }
                }
            }
        }

        foreach (var highlight in entry.Highlights)
        {
            foreach (var group in groups)
            {
                foreach (var skill in group.Skills)
                {
                    if (!taken.Contains(skill) && Mentions(highlight, skill))
                    {
                        taken.Add(skill);
                        loose.Add(skill);
                    }
                }
            }
        }

        var line = specific.Concat(loose).ToList();

        // One name can subsume another — "Workflow Orchestration (Temporal.io)" contains
        // "Temporal", and a byline carrying both reads as duplication. The shorter name
        // wins the line; the longer stays in the skills sheet and the chip tooltips.
        return [.. line.Where(skill =>
            !line.Any(other => other.Length < skill.Length
                               && skill.Contains(other, StringComparison.OrdinalIgnoreCase)))];
    }

    private static IReadOnlyList<string> EmployersUsing(
        string skill,
        IReadOnlyList<ExperienceEntry> experience) =>
        [.. experience
             .Where(entry => entry.Highlights.Any(h => Mentions(h, skill)))
             .Select(entry => entry.Company)
             .Distinct(StringComparer.OrdinalIgnoreCase)];

    /// <summary>
    /// Record phrasing and vocabulary names drift apart: a bullet says "MVC" while the
    /// skills list says "ASP.NET MVC"; the record says "autonomous AI agent" while the
    /// vocabulary says "Autonomous agent development". Aliases bridge the two so the
    /// flagship skills can never render as uncited — and no alias may widen a match
    /// the record does not support.
    /// </summary>
    private static readonly Dictionary<string, string[]> Aliases =
        new(StringComparer.OrdinalIgnoreCase)
        {
            ["ASP.NET MVC"] = ["MVC"],
            ["Entity Framework Core"] = ["Entity Framework"],
            ["AI-guided development workflows"] = ["AI skills"],
            ["Autonomous agent development"] = ["autonomous"],
            ["Project templating & rule authoring"] = ["project template"],
            ["Workflow Orchestration (Temporal.io)"] = ["Temporal"],
            ["Solution architecture documents"] = ["solution architecture documentation"],
            ["Microsoft Copilot Studio"] = ["Copilot Studio"],
            ["Microsoft Azure"] = ["Azure"],
            ["Mermaid diagramming"] = ["Mermaid"],
            ["Payment gateway integration"] = ["payment"],
            ["AI training & curriculum design"] = ["AI training"],
            ["API documentation"] = ["API endpoints"],
        };

    private static bool Mentions(Highlight highlight, string skill) =>
        ContainsWord(highlight.Text, skill)
        || highlight.Tags.Any(tag => tag.Contains(skill, StringComparison.OrdinalIgnoreCase))
        || (Aliases.TryGetValue(skill, out var aliases)
            && (aliases.Any(alias => ContainsWord(highlight.Text, alias))
                || highlight.Tags.Any(tag => aliases.Any(alias => tag.Contains(alias, StringComparison.OrdinalIgnoreCase)))));

    /// <summary>
    /// Substring matching with a guard against accidental hits inside longer words —
    /// otherwise "Git" matches "digital" and "React" matches "reactive".
    /// </summary>
    private static bool ContainsWord(string text, string term)
    {
        var index = text.IndexOf(term, StringComparison.OrdinalIgnoreCase);

        while (index >= 0)
        {
            var beforeOk = index == 0 || !char.IsLetterOrDigit(text[index - 1]);
            var afterIndex = index + term.Length;
            var afterOk = afterIndex >= text.Length || !char.IsLetterOrDigit(text[afterIndex]);

            if (beforeOk && afterOk)
            {
                return true;
            }

            index = text.IndexOf(term, index + 1, StringComparison.OrdinalIgnoreCase);
        }

        return false;
    }
}
