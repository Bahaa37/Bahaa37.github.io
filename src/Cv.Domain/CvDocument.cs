namespace Cv.Domain;

/// <summary>
/// The single source of truth. Every renderer — print CV, showcase page, editor —
/// projects from this one object; none of them holds content of its own.
/// </summary>
public sealed record CvDocument
{
    public required Profile Profile { get; init; }

    /// <summary>
    /// The short summary, for the showcase page. Kept deliberately brief: a reader gives
    /// the top of a CV a few seconds, and a paragraph that has to be worked through is a
    /// paragraph that gets skipped.
    /// </summary>
    public required string Summary { get; init; }

    /// <summary>
    /// The long-form summary, used only on the printed CV. An ATS indexes the whole
    /// document, and a human reading the PDF has already decided to spend time on it —
    /// so the depth belongs there rather than on the page a recruiter skims.
    /// </summary>
    public string? SummaryExtended { get; init; }

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

    /// <summary>
    /// The headline title. Kept in step with what the experience record actually shows —
    /// a title the timeline contradicts is worse than a modest one, because the reader
    /// finds the contradiction on the same page.
    /// </summary>
    public required string Title { get; init; }

    public required string Location { get; init; }

    /*
        The five fields below are the ones a recruiter asks for in the first reply to any
        application, in every market this CV targets. Leaving them to that email costs a
        round trip and, for a remote or relocation role, is often the question that
        decides whether the reply comes at all.
    */

    /// <summary>Home timezone, e.g. "EET (UTC+2)".</summary>
    public string? Timezone { get; init; }

    /// <summary>Which working days this timezone actually overlaps, in plain words.</summary>
    public string? WorkingOverlap { get; init; }

    /// <summary>Spoken languages with proficiency, e.g. "English — professional working proficiency".</summary>
    public IReadOnlyList<string> Languages { get; init; } = [];

    /// <summary>Availability and notice period.</summary>
    public string? Availability { get; init; }

    /// <summary>Relocation and remote-work stance.</summary>
    public string? Relocation { get; init; }

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
