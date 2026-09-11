namespace Cv.Domain;

/// <summary>
/// A long-form piece of work, told as problem → approach → outcome.
/// </summary>
/// <remarks>
/// Case studies exist only on the showcase page. A CV bullet has room to say
/// <em>what</em> was done; a case study has room to show <em>how it was decided</em>,
/// which is the part a hiring manager is actually assessing.
/// </remarks>
public sealed record CaseStudy
{
    /// <summary>URL-safe identifier used for deep links, e.g. "legacy-modernization".</summary>
    public required string Slug { get; init; }

    public required string Title { get; init; }

    /// <summary>
    /// A compact form of the title for browser tabs, search results and link previews,
    /// where the full sentence is cut off mid-word. Falls back to <see cref="Title"/>.
    /// </summary>
    /// <remarks>
    /// Written rather than computed on purpose: truncating a title at a word boundary
    /// produces something that reads like a mistake, and this is the line a recruiter
    /// sees in a Google result before they see anything else.
    /// </remarks>
    public string? ShortTitle { get; init; }

    /// <summary>The short title where one is written, otherwise the full one.</summary>
    public string DisplayTitle => string.IsNullOrWhiteSpace(ShortTitle) ? Title : ShortTitle;

    /// <summary>One-line description, used on cards and in link previews.</summary>
    public required string Summary { get; init; }

    /// <summary>The employer or context this work belongs to.</summary>
    public string? Organisation { get; init; }

    /// <summary>What was wrong, or what needed to exist.</summary>
    public required string Problem { get; init; }

    /// <summary>How it was solved, and why that way rather than another.</summary>
    public required string Approach { get; init; }

    /// <summary>What changed as a result. Quantified wherever a real number exists.</summary>
    public IReadOnlyList<string> Outcomes { get; init; } = [];

    public IReadOnlyList<string> Stack { get; init; } = [];

    /// <summary>
    /// Optional Mermaid diagram source describing the architecture.
    /// Mermaid is already used for documentation at work, so this is consistent
    /// with existing practice rather than decoration.
    /// </summary>
    public string? MermaidDiagram { get; init; }

    /// <summary>Controls ordering on the showcase page; lower sorts first.</summary>
    public int DisplayOrder { get; init; }

    /// <summary>
    /// Optional route to a long-form write-up. Present when the work warrants more
    /// depth than a card can hold — typically where the repository itself is private,
    /// so the write-up is the only thing a reader can actually evaluate.
    /// </summary>
    public string? WriteupUrl { get; init; }

    public bool HasWriteup => !string.IsNullOrWhiteSpace(WriteupUrl);

    public bool HasDiagram => !string.IsNullOrWhiteSpace(MermaidDiagram);
}
