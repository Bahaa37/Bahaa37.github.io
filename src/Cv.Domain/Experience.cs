namespace Cv.Domain;

public enum EmploymentType
{
    FullTime,
    PartTime,
    Contract,
    Freelance,
    Internship,
}

/// <summary>One role at one employer.</summary>
/// <remarks>
/// A single employer may appear more than once. Two separate entries for the same
/// company with a different employer in between is how a return to a former employer
/// is represented, and that shape is deliberate: being re-hired is visible evidence
/// against having been let go.
/// </remarks>
public sealed record ExperienceEntry
{
    public required string Company { get; init; }

    public required string Role { get; init; }

    public required DateRange Period { get; init; }

    public EmploymentType EmploymentType { get; init; } = EmploymentType.FullTime;

    public string? Location { get; init; }

    public IReadOnlyList<Highlight> Highlights { get; init; } = [];

    /// <summary>Identifies repeat entries for the same employer, for timeline grouping.</summary>
    public bool IsSameEmployerAs(ExperienceEntry other) =>
        string.Equals(Company, other.Company, StringComparison.OrdinalIgnoreCase);
}

/// <summary>
/// A single achievement bullet.
/// </summary>
/// <remarks>
/// <see cref="Metric"/> is separate from <see cref="Text"/> on purpose. Un-quantified
/// bullets ("significantly improved performance") are the most common weakness in an
/// engineering CV, and keeping the number in its own field lets the editor show which
/// bullets are still missing one. Making the gap visible is what keeps it fixed.
/// A null metric is honest; an invented one cannot be defended in an interview.
/// </remarks>
public sealed record Highlight
{
    public required string Text { get; init; }

    /// <summary>The quantified outcome, e.g. "5–7 days reduced to 3". Null when not yet supplied.</summary>
    public string? Metric { get; init; }

    /// <summary>Free-form tags used to link a skill back to the roles where it was used.</summary>
    public IReadOnlyList<string> Tags { get; init; } = [];

    /// <summary>Marks the strongest bullets, which are the ones the print CV keeps when space is tight.</summary>
    public bool IsFeatured { get; init; }

    public bool HasMetric => !string.IsNullOrWhiteSpace(Metric);
}
