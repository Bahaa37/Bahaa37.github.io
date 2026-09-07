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

    private static IReadOnlyList<string> EmployersUsing(
        string skill,
        IReadOnlyList<ExperienceEntry> experience) =>
        [.. experience
             .Where(entry => entry.Highlights.Any(h => Mentions(h, skill)))
             .Select(entry => entry.Company)
             .Distinct(StringComparer.OrdinalIgnoreCase)];

    private static bool Mentions(Highlight highlight, string skill) =>
        highlight.Tags.Any(tag => tag.Contains(skill, StringComparison.OrdinalIgnoreCase)
                                  || skill.Contains(tag, StringComparison.OrdinalIgnoreCase))
        || ContainsWord(highlight.Text, skill);

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
