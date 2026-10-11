namespace Cv.Domain;

/// <summary>A qualification, diploma, or degree.</summary>
public sealed record EducationEntry
{
    public required string Institution { get; init; }

    public required string Credential { get; init; }

    public required DateRange Period { get; init; }

    public IReadOnlyList<string> Details { get; init; } = [];

    /// <summary>True for study still under way, which is shown as an in-progress section.</summary>
    public bool InProgress => Period.IsOngoing;
}

/// <summary>A certification or course completion.</summary>
/// <remarks>
/// <see cref="IsFeatured"/> is the mechanism that lets one list serve two audiences:
/// the print CV renders only the featured few, while the showcase page renders all of
/// them. Without it the full list consumes a page of the PDF that would be better
/// spent on achievements.
/// </remarks>
public sealed record Certification
{
    public required string Name { get; init; }

    public required string Issuer { get; init; }

    public YearMonth? Awarded { get; init; }

    public bool IsFeatured { get; init; }

    public string? CredentialUrl { get; init; }
}

/// <summary>An award or formal recognition received at work.</summary>
public sealed record Award
{
    public required string Title { get; init; }

    public required string Issuer { get; init; }

    public YearMonth? Awarded { get; init; }

    public string? Description { get; init; }
}
