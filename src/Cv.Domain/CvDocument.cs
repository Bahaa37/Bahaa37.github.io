namespace Cv.Domain;

/// <summary>
/// The single source of truth. Every renderer — print CV, showcase page, editor —
/// projects from this one object; none of them holds content of its own.
/// </summary>
public sealed record CvDocument
{
    public required Profile Profile { get; init; }

    public required string Summary { get; init; }

    public IReadOnlyList<SkillGroup> SkillGroups { get; init; } = [];

    public IReadOnlyList<ExperienceEntry> Experience { get; init; } = [];

    public IReadOnlyList<EducationEntry> Education { get; init; } = [];

    public IReadOnlyList<Certification> Certifications { get; init; } = [];

    /// <summary>Formal recognition received at work. Distinct from certifications, which are earned by study.</summary>
    public IReadOnlyList<Award> Awards { get; init; } = [];

    /// <summary>
    /// Long-form case studies for the showcase page. These have no equivalent on the
    /// printed CV — they are the depth layer that gives a hiring manager a reason to
    /// stay on the page.
    /// </summary>
    public IReadOnlyList<CaseStudy> CaseStudies { get; init; } = [];
}

/// <summary>Identity and contact details.</summary>
public sealed record Profile
{
    public required string Name { get; init; }

    /// <summary>The headline title, e.g. "Senior .NET Full-Stack Software Engineer".</summary>
    public required string Title { get; init; }

    public required string Location { get; init; }

    /// <summary>
    /// Stored in international format ("+20 128 458 6608") so that click-to-call works.
    /// A leading trunk zero after the country code breaks the tel: link.
    /// </summary>
    public required string Phone { get; init; }

    public required string Email { get; init; }

    public string? LinkedIn { get; init; }

    public string? GitHub { get; init; }

    public string? Website { get; init; }

    /// <summary>Digits only, for the tel: href.</summary>
    public string PhoneHref => "tel:" + new string([.. Phone.Where(c => char.IsDigit(c) || c == '+')]);
}

/// <summary>A named cluster of skills, e.g. "Architecture &amp; Patterns".</summary>
public sealed record SkillGroup
{
    public required string Category { get; init; }

    public IReadOnlyList<string> Skills { get; init; } = [];
}
