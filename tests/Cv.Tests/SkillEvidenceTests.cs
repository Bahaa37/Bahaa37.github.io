using Cv.Application;
using Cv.Domain;

namespace Cv.Tests;

public class SkillEvidenceTests
{
    private static ExperienceEntry Role(string company, params Highlight[] highlights) => new()
    {
        Company = company,
        Role = "Engineer",
        Period = new DateRange(YearMonth.Parse("2023-01"), null),
        Highlights = highlights,
    };

    [Fact]
    public void FindsAnEmployerFromHighlightText()
    {
        ExperienceEntry[] experience =
        [
            Role("PS Digital", new Highlight { Text = "Replaced Entity Framework with Dapper." }),
        ];

        var evidence = SkillEvidence.For(new SkillGroup { Category = "Data", Skills = ["Dapper"] }, experience);

        Assert.Equal(["PS Digital"], evidence[0].UsedAt);
    }

    [Fact]
    public void FindsAnEmployerFromATag()
    {
        ExperienceEntry[] experience =
        [
            Role("Andalusia", new Highlight { Text = "Built an agent.", Tags = ["Copilot Studio"] }),
        ];

        var evidence = SkillEvidence.For(
            new SkillGroup { Category = "AI", Skills = ["Microsoft Copilot Studio"] },
            experience);

        Assert.Equal(["Andalusia"], evidence[0].UsedAt);
    }

    [Fact]
    public void DoesNotMatchASkillNameInsideALongerWord()
    {
        // "Git" must not match "digital", and "React" must not match "reactive".
        ExperienceEntry[] experience =
        [
            Role("PS Digital", new Highlight { Text = "Worked on a digital reactive platform." }),
        ];

        var evidence = SkillEvidence.For(
            new SkillGroup { Category = "Tools", Skills = ["Git", "React"] },
            experience);

        Assert.All(evidence, e => Assert.Empty(e.UsedAt));
    }

    [Fact]
    public void ListsEachEmployerOnlyOnceEvenWithSeveralMatchingHighlights()
    {
        ExperienceEntry[] experience =
        [
            Role("Andalusia",
                new Highlight { Text = "Used Dapper here." },
                new Highlight { Text = "Also used Dapper there." }),
        ];

        var evidence = SkillEvidence.For(new SkillGroup { Category = "Data", Skills = ["Dapper"] }, experience);

        Assert.Equal(["Andalusia"], evidence[0].UsedAt);
    }

    [Fact]
    public void ReportsNoEvidenceRatherThanGuessing()
    {
        ExperienceEntry[] experience = [Role("PS Digital", new Highlight { Text = "Did unrelated work." })];

        var evidence = SkillEvidence.For(new SkillGroup { Category = "Data", Skills = ["Redis"] }, experience);

        Assert.False(evidence[0].HasEvidence);
    }
}
