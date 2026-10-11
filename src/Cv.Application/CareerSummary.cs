using Cv.Domain;

namespace Cv.Application;

/// <summary>
/// Figures computed from the experience list rather than typed by hand.
/// </summary>
/// <remarks>
/// The previous CV claimed "3+ years" as literal text, which was already stale.
/// Anything derivable from the dates is derived here so it can never drift again.
/// </remarks>
public static class CareerSummary
{
    /// <summary>
    /// Total professional experience in months, counting overlapping roles once.
    /// </summary>
    /// <remarks>
    /// Summing each role's duration would double-count any period with concurrent
    /// roles and inflate the total — so the spans are merged into a union first.
    /// Overstating experience on a CV is a correctness bug, not a rounding choice.
    /// </remarks>
    public static int TotalExperienceInMonths(IEnumerable<ExperienceEntry> experience, YearMonth asOf)
    {
        var ordered = experience
            .Select(e => e.Period)
            .OrderBy(p => p.Start)
            .ToList();

        if (ordered.Count == 0)
        {
            return 0;
        }

        var total = 0;
        var currentStart = ordered[0].Start;
        var currentEnd = ordered[0].End ?? asOf;

        foreach (var period in ordered.Skip(1))
        {
            var start = period.Start;
            var end = period.End ?? asOf;

            if (start <= currentEnd)
            {
                // Overlapping or contiguous — extend the current span instead of adding a new one.
                if (end > currentEnd)
                {
                    currentEnd = end;
                }
            }
            else
            {
                total += currentStart.MonthsUntil(currentEnd);
                currentStart = start;
                currentEnd = end;
            }
        }

        total += currentStart.MonthsUntil(currentEnd);
        return total;
    }

    /// <summary>Experience expressed in whole years, rounded down.</summary>
    public static int TotalExperienceInYears(IEnumerable<ExperienceEntry> experience, YearMonth asOf) =>
        TotalExperienceInMonths(experience, asOf) / 12;

    /// <summary>A phrase safe to drop into the summary line, e.g. "3+ years".</summary>
    public static string ExperiencePhrase(IEnumerable<ExperienceEntry> experience, YearMonth asOf)
    {
        var months = TotalExperienceInMonths(experience, asOf);
        var years = months / 12;
        var remainder = months % 12;

        return years switch
        {
            0 => $"{months} month{(months == 1 ? string.Empty : "s")}",
            _ when remainder >= 6 => $"{years}.5+ years",
            _ => $"{years}+ years",
        };
    }

    /// <summary>Roles newest first, which is the order every renderer displays them in.</summary>
    /// <remarks>
    /// Ongoing roles sort above finished ones rather than being given a far-future
    /// sentinel end date. A sentinel would have to be a real <see cref="YearMonth"/>,
    /// and inventing an out-of-range one to mean "still here" is the kind of trick that
    /// works until the type validates its own input.
    /// </remarks>
    public static IReadOnlyList<ExperienceEntry> InReverseChronologicalOrder(
        IEnumerable<ExperienceEntry> experience) =>
        [.. experience.OrderByDescending(e => e.Period.IsOngoing)
                      .ThenByDescending(e => e.Period.End ?? e.Period.Start)
                      .ThenByDescending(e => e.Period.Start)];

    /// <summary>Distinct employers, newest first. A repeat employer is counted once.</summary>
    public static IReadOnlyList<string> Employers(IEnumerable<ExperienceEntry> experience) =>
        [.. InReverseChronologicalOrder(experience)
             .Select(e => e.Company)
             .Distinct(StringComparer.OrdinalIgnoreCase)];
}
