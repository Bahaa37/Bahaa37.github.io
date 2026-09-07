using Cv.Domain;

namespace Cv.Application;

public enum IssueSeverity
{
    /// <summary>Something a recruiter would read as an error or a red flag.</summary>
    Error,

    /// <summary>Something that weakens the CV without being wrong.</summary>
    Warning,
}

public sealed record CvIssue(IssueSeverity Severity, string Location, string Message);

/// <summary>
/// Checks the CV for the defects that cost candidates interviews.
/// </summary>
/// <remarks>
/// This exists because the original CV shipped with two concurrent full-time roles and
/// not a single quantified achievement. Both are the kind of thing that is obvious to a
/// reader and invisible to the author. Encoding them as checks means the editor can
/// surface them continuously instead of relying on someone noticing.
/// </remarks>
public static class CvValidator
{
    public static IReadOnlyList<CvIssue> Validate(CvDocument document, YearMonth asOf)
    {
        List<CvIssue> issues = [];

        issues.AddRange(FindConcurrentFullTimeRoles(document.Experience, asOf));
        issues.AddRange(FindUnquantifiedHighlights(document.Experience));
        issues.AddRange(FindMissingContactLinks(document.Profile));
        issues.AddRange(FindAnachronisticTechnologyVersions(document.Experience));

        return issues;
    }

    /// <summary>
    /// General availability dates for .NET versions, used to catch claims about a
    /// technology that did not exist yet during the role being described.
    /// </summary>
    private static readonly (int Version, YearMonth ReleasedOn)[] DotNetReleases =
    [
        (5, new YearMonth(2020, 11)),
        (6, new YearMonth(2021, 11)),
        (7, new YearMonth(2022, 11)),
        (8, new YearMonth(2023, 11)),
        (9, new YearMonth(2024, 11)),
        (10, new YearMonth(2025, 11)),
    ];

    /// <summary>
    /// Flags a bullet claiming a .NET version that had not shipped when the role ended.
    /// </summary>
    /// <remarks>
    /// This is the most damaging kind of CV error: a technical interviewer spots it
    /// immediately, and unlike a vague bullet it reads as padding rather than as
    /// imprecision. The original CV claimed a ".NET 9 Web API" built during a role that
    /// ended four months before .NET 9 was released.
    /// </remarks>
    private static IEnumerable<CvIssue> FindAnachronisticTechnologyVersions(
        IReadOnlyList<ExperienceEntry> experience)
    {
        foreach (var entry in experience)
        {
            // A role that is still running can legitimately mention anything released to date.
            if (entry.Period.End is not { } roleEnd)
            {
                continue;
            }

            foreach (var highlight in entry.Highlights)
            {
                foreach (var (version, releasedOn) in DotNetReleases)
                {
                    if (!MentionsDotNetVersion(highlight.Text, version) || releasedOn <= roleEnd)
                    {
                        continue;
                    }

                    yield return new CvIssue(
                        IssueSeverity.Error,
                        $"{entry.Company} — {entry.Role}",
                        $".NET {version} was released in {releasedOn.ToDisplayString()}, after this role ended " +
                        $"({roleEnd.ToDisplayString()}): \"{Truncate(highlight.Text, 60)}\"");
                }
            }
        }
    }

    private static bool MentionsDotNetVersion(string text, int version)
    {
        var token = $".NET {version}";
        var index = text.IndexOf(token, StringComparison.OrdinalIgnoreCase);

        while (index >= 0)
        {
            // Reject ".NET 1" matching inside ".NET 10" by requiring a non-digit after the number.
            var after = index + token.Length;
            if (after >= text.Length || !char.IsDigit(text[after]))
            {
                return true;
            }

            index = text.IndexOf(token, after, StringComparison.OrdinalIgnoreCase);
        }

        return false;
    }

    /// <summary>
    /// Two full-time roles cannot run at the same time. A recruiter comparing date
    /// ranges spots this immediately, and it reads as either carelessness or dishonesty.
    /// Part-time and contract roles are exempt, since concurrency there is normal.
    /// </summary>
    private static IEnumerable<CvIssue> FindConcurrentFullTimeRoles(
        IReadOnlyList<ExperienceEntry> experience,
        YearMonth asOf)
    {
        var fullTime = experience
            .Where(e => e.EmploymentType == EmploymentType.FullTime)
            .ToList();

        for (var i = 0; i < fullTime.Count; i++)
        {
            for (var j = i + 1; j < fullTime.Count; j++)
            {
                var first = fullTime[i];
                var second = fullTime[j];

                if (first.Period.Overlaps(second.Period, asOf))
                {
                    yield return new CvIssue(
                        IssueSeverity.Error,
                        $"{first.Company} / {second.Company}",
                        $"Two full-time roles overlap: '{first.Role}' at {first.Company} " +
                        $"({first.Period.ToShortDisplayString()}) and '{second.Role}' at {second.Company} " +
                        $"({second.Period.ToShortDisplayString()}). A reader will treat this as an error.");
                }
            }
        }
    }

    /// <summary>
    /// Flags achievement bullets with no number attached. These are reported rather than
    /// auto-filled — a fabricated figure cannot be defended in an interview, so a blank
    /// metric is always preferable to an invented one.
    /// </summary>
    private static IEnumerable<CvIssue> FindUnquantifiedHighlights(IReadOnlyList<ExperienceEntry> experience)
    {
        foreach (var entry in experience)
        {
            foreach (var highlight in entry.Highlights.Where(h => !h.HasMetric))
            {
                yield return new CvIssue(
                    IssueSeverity.Warning,
                    $"{entry.Company} — {entry.Role}",
                    $"No metric on: \"{Truncate(highlight.Text, 70)}\"");
            }
        }
    }

    private static IEnumerable<CvIssue> FindMissingContactLinks(Profile profile)
    {
        if (string.IsNullOrWhiteSpace(profile.GitHub))
        {
            yield return new CvIssue(
                IssueSeverity.Warning,
                "Profile",
                "No GitHub link. Its absence is conspicuous for a senior engineer.");
        }

        if (string.IsNullOrWhiteSpace(profile.Website))
        {
            yield return new CvIssue(
                IssueSeverity.Warning,
                "Profile",
                "No portfolio URL. The printed CV then has no route to the case studies.");
        }

        if (profile.Phone.Contains("+20 0", StringComparison.Ordinal))
        {
            yield return new CvIssue(
                IssueSeverity.Error,
                "Profile",
                "Phone number keeps a trunk '0' after the +20 country code, which breaks click-to-call.");
        }
    }

    private static string Truncate(string value, int maxLength) =>
        value.Length <= maxLength ? value : value[..maxLength].TrimEnd() + "…";
}
