namespace Cv.Domain;

/// <summary>
/// An architecture decision record: what was decided, what else was on the table, and
/// what it cost.
/// </summary>
/// <remarks>
/// The CV claims solution architecture documents, SRS and low-level design. Claiming it
/// is not evidence of it. A hiring architect wants to see how a system gets specified
/// far more than they want to read an opinion about specifying systems, and an ADR is
/// the smallest artifact that actually shows the reasoning.
///
/// The shape is deliberately the standard one — context, options, decision,
/// consequences — because recognisability is the point. A reader should know what they
/// are looking at before they read a word of it.
/// </remarks>
public sealed record DecisionRecord
{
    /// <summary>Sequential identifier, e.g. "ADR-0003". Stable once published.</summary>
    public required string Id { get; init; }

    /// <summary>URL-safe identifier used for deep links.</summary>
    public required string Slug { get; init; }

    public required string Title { get; init; }

    /// <summary>A compact title for browser tabs and search results.</summary>
    public string? ShortTitle { get; init; }

    public DecisionStatus Status { get; init; } = DecisionStatus.Accepted;

    /// <summary>When the decision was taken, as "YYYY-MM".</summary>
    public required string Decided { get; init; }

    /// <summary>Where this decision was taken — a project, or this repository.</summary>
    public string? Context { get; init; }

    /// <summary>The forces in play: what made a decision necessary at all.</summary>
    public required string Situation { get; init; }

    /// <summary>
    /// What was considered, including what was rejected. An ADR listing only the option
    /// that won is a press release; the rejected options are where the reasoning is.
    /// </summary>
    public IReadOnlyList<DecisionOption> Options { get; init; } = [];

    /// <summary>What was chosen, stated plainly.</summary>
    public required string Decision { get; init; }

    /// <summary>What it cost as well as what it bought. Both, or it is not honest.</summary>
    public IReadOnlyList<string> Consequences { get; init; } = [];

    /// <summary>Optional Mermaid source illustrating the decision.</summary>
    public string? MermaidDiagram { get; init; }

    /// <summary>Ordering on the index; lower sorts first.</summary>
    public int DisplayOrder { get; init; }

    public string DisplayTitle => string.IsNullOrWhiteSpace(ShortTitle) ? Title : ShortTitle;

    public bool HasDiagram => !string.IsNullOrWhiteSpace(MermaidDiagram);
}

/// <summary>One option that was on the table, and how it was judged.</summary>
public sealed record DecisionOption
{
    public required string Name { get; init; }

    /// <summary>Why it was chosen, or why it was not.</summary>
    public required string Assessment { get; init; }

    /// <summary>True for the option that was taken.</summary>
    public bool Chosen { get; init; }
}

public enum DecisionStatus
{
    Proposed,
    Accepted,

    /// <summary>Replaced by a later decision. Kept: the record is the point.</summary>
    Superseded,
}
