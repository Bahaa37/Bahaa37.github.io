namespace Cv.Domain;

/// <summary>
/// A recommendation a real person has given, attributed to them by their LinkedIn
/// and/or GitHub profile.
/// </summary>
/// <remarks>
/// Testimonials are third-party content: they are curated into
/// <c>data/testimonials.json</c> only after the named person actually gave them, and
/// every entry carries a live link to the person who did. Nothing here is invented —
/// the same no-fabrication rule the CV follows applies doubly to words put in
/// someone else's mouth.
/// </remarks>
public sealed record Testimonial
{
    /// <summary>The person's name as they write it.</summary>
    public required string Name { get; init; }

    /// <summary>What they do, e.g. "Engineering Manager".</summary>
    public string? Role { get; init; }

    /// <summary>Where they do it, e.g. "Andalusia Business Solutions".</summary>
    public string? Company { get; init; }

    /// <summary>The recommendation itself, in the giver's own words.</summary>
    public required string Text { get; init; }

    /// <summary>LinkedIn profile URL. One of <see cref="LinkedIn"/>/<see cref="GitHub"/>
    /// is required so every quote points back to a verifiable person.</summary>
    public string? LinkedIn { get; init; }

    /// <summary>GitHub profile URL. Also the source of the avatar when present.</summary>
    public string? GitHub { get; init; }

    /// <summary>When the recommendation was given, as YYYY-MM.</summary>
    public string? Date { get; init; }

    /// <summary>Lower sorts first; entries with the same order keep file order.</summary>
    public int DisplayOrder { get; init; }
}
