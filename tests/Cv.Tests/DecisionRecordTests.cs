using System.Text.Json;
using Cv.Application;
using Cv.Domain;

namespace Cv.Tests;

/// <summary>
/// Exercises the real decisions.json.
/// </summary>
/// <remarks>
/// These records exist to evidence a claim the CV makes about architecture practice, so
/// a malformed or half-written one is worse than none at all — it demonstrates the
/// opposite of what it is there to demonstrate. The rules below are the ones that
/// separate a decision record from a summary of what was built.
/// </remarks>
public class DecisionRecordTests
{
    private sealed record DecisionFile(IReadOnlyList<DecisionRecord> Decisions);

    private static string DecisionsPath()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);

        while (directory is not null)
        {
            var candidate = Path.Combine(directory.FullName, "src", "Cv.Web", "wwwroot", "data", "decisions.json");
            if (File.Exists(candidate))
            {
                return candidate;
            }

            directory = directory.Parent;
        }

        throw new FileNotFoundException(
            "Could not locate src/Cv.Web/wwwroot/data/decisions.json by walking up from the test output directory.");
    }

    private static IReadOnlyList<DecisionRecord> Load() =>
        JsonSerializer.Deserialize<DecisionFile>(File.ReadAllText(DecisionsPath()), CvJson.Options)?.Decisions
        ?? throw new InvalidOperationException("decisions.json deserialized to null.");

    [Fact]
    public void TheRealFileDeserializes()
    {
        var records = Load();

        Assert.NotEmpty(records);
        Assert.All(records, r => Assert.False(string.IsNullOrWhiteSpace(r.Decision)));
    }

    [Fact]
    public void EveryRecordNamesExactlyOneChosenOption()
    {
        // Zero chosen options means the record never says what was decided. More than
        // one means it is not a decision.
        foreach (var record in Load())
        {
            var chosen = record.Options.Count(o => o.Chosen);

            Assert.True(
                chosen == 1,
                $"{record.Id} marks {chosen} options as chosen; a decision record names exactly one.");
        }
    }

    [Fact]
    public void EveryRecordConsidersAnAlternative()
    {
        // A record listing only the option that won is a press release. The rejected
        // options are where the reasoning actually lives, and they are what a reader is
        // assessing.
        foreach (var record in Load())
        {
            Assert.True(
                record.Options.Count(o => !o.Chosen) >= 1,
                $"{record.Id} lists no rejected option, so it records a conclusion rather than a decision.");
        }
    }

    [Fact]
    public void EveryRecordStatesItsConsequences()
    {
        foreach (var record in Load())
        {
            Assert.True(
                record.Consequences.Count >= 2,
                $"{record.Id} lists {record.Consequences.Count} consequences. A decision that only " +
                "bought and never cost anything has not been examined honestly.");
        }
    }

    [Fact]
    public void IdentifiersAndSlugsAreUnique()
    {
        var records = Load();

        var ids = records.Select(r => r.Id).ToList();
        var slugs = records.Select(r => r.Slug).ToList();

        Assert.Equal(ids.Count, ids.Distinct(StringComparer.OrdinalIgnoreCase).Count());
        Assert.Equal(slugs.Count, slugs.Distinct(StringComparer.OrdinalIgnoreCase).Count());
    }

    [Fact]
    public void EveryRecordHasATitleThatSurvivesASearchResult()
    {
        // Matches the rule the case studies are held to; the prerenderer appends the
        // same " — Bahaa Aldeen Mohamed" suffix to both.
        const int suffix = 23;

        foreach (var record in Load())
        {
            Assert.True(
                record.DisplayTitle.Length + suffix <= 70,
                $"{record.Id} renders a {record.DisplayTitle.Length + suffix}-character page title. " +
                "Add or shorten its shortTitle.");
        }
    }
}
