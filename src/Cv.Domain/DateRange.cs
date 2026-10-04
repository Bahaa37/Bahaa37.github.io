namespace Cv.Domain;

/// <summary>
/// A month-precision span. A null <see cref="End"/> means the span is ongoing.
/// </summary>
/// <remarks>
/// Modelling "present" as a null end date rather than the literal string "Present"
/// is what lets an ongoing role take part in duration maths and timeline sorting
/// exactly like a closed one.
/// </remarks>
public sealed record DateRange(YearMonth Start, YearMonth? End)
{
    public bool IsOngoing => End is null;

    /// <summary>Duration in whole months, measured to <paramref name="asOf"/> when ongoing.</summary>
    public int DurationInMonths(YearMonth asOf) => Start.MonthsUntil(End ?? asOf);

    /// <summary>True when the two spans genuinely run concurrently.</summary>
    /// <remarks>
    /// Used to detect the impossible case of two concurrent full-time roles, which is
    /// the defect that prompted this type to exist. See the content intake notes.
    ///
    /// The comparison is strict so that a shared boundary month does not count as an
    /// overlap: leaving one employer in July and starting the next in July is the
    /// normal way a job change is written on a CV, not a contradiction. Only a span
    /// that extends past the other's start is treated as concurrent.
    /// </remarks>
    public bool Overlaps(DateRange other, YearMonth asOf)
    {
        var thisEnd = End ?? asOf;
        var otherEnd = other.End ?? asOf;

        return Start < otherEnd && other.Start < thisEnd;
    }

    /// <summary>"March 2023 – November 2025", or "November 2025 – Present" when ongoing.</summary>
    public string ToDisplayString() =>
        $"{Start.ToDisplayString()} – {(End?.ToDisplayString() ?? "Present")}";

    /// <summary>"Mar 2023 – Nov 2025", for space-constrained layouts.</summary>
    public string ToShortDisplayString() =>
        $"{Start.ToShortDisplayString()} – {(End?.ToShortDisplayString() ?? "Present")}";
}
