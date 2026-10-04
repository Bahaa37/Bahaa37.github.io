using Cv.Application;
using Cv.Domain;

namespace Cv.Tests;

public class CareerSummaryTests
{
    private static readonly YearMonth AsOf = YearMonth.Parse("2026-09");

    private static ExperienceEntry Role(string company, string start, string? end) => new()
    {
        Company = company,
        Role = "Engineer",
        Period = new DateRange(YearMonth.Parse(start), end is null ? null : YearMonth.Parse(end)),
    };

    [Fact]
    public void TotalExperience_SumsNonOverlappingRoles()
    {
        ExperienceEntry[] experience =
        [
            Role("A", "2023-01", "2023-07"), // 6 months
            Role("B", "2024-01", "2024-04"), // 3 months
        ];

        Assert.Equal(9, CareerSummary.TotalExperienceInMonths(experience, AsOf));
    }

    [Fact]
    public void TotalExperience_CountsOverlappingPeriodOnlyOnce()
    {
        // Two concurrent roles across the same 12 months must total 12, not 24.
        ExperienceEntry[] experience =
        [
            Role("A", "2023-01", "2024-01"),
            Role("B", "2023-01", "2024-01"),
        ];

        Assert.Equal(12, CareerSummary.TotalExperienceInMonths(experience, AsOf));
    }

    [Fact]
    public void TotalExperience_MergesPartiallyOverlappingRoles()
    {
        // Jan 2023 - Jan 2024 and Jul 2023 - Jul 2024 together span Jan 2023 - Jul 2024 = 18 months.
        ExperienceEntry[] experience =
        [
            Role("A", "2023-01", "2024-01"),
            Role("B", "2023-07", "2024-07"),
        ];

        Assert.Equal(18, CareerSummary.TotalExperienceInMonths(experience, AsOf));
    }

    [Fact]
    public void TotalExperience_TreatsRoleContainedInAnotherAsAlreadyCounted()
    {
        ExperienceEntry[] experience =
        [
            Role("A", "2023-01", "2025-01"), // 24 months
            Role("B", "2023-06", "2023-09"), // fully inside the first
        ];

        Assert.Equal(24, CareerSummary.TotalExperienceInMonths(experience, AsOf));
    }

    [Fact]
    public void TotalExperience_MeasuresOngoingRoleToTheAsOfDate()
    {
        ExperienceEntry[] experience = [Role("A", "2026-03", null)];

        Assert.Equal(6, CareerSummary.TotalExperienceInMonths(experience, AsOf));
    }

    [Fact]
    public void TotalExperience_IsZeroWhenThereIsNoExperience()
    {
        Assert.Equal(0, CareerSummary.TotalExperienceInMonths([], AsOf));
    }

    [Fact]
    public void TotalExperience_HandlesTheRealBoomerangShape()
    {
        // PS Digital -> MEEM -> PS Digital again -> Andalusia, continuous from Mar 2023.
        ExperienceEntry[] experience =
        [
            Role("PS Digital", "2023-03", "2024-07"),
            Role("MEEM", "2024-07", "2024-11"),
            Role("PS Digital", "2024-11", "2025-11"),
            Role("Andalusia", "2025-11", null),
        ];

        // Mar 2023 to Sep 2026 inclusive of start month = 42 months.
        Assert.Equal(42, CareerSummary.TotalExperienceInMonths(experience, AsOf));
        Assert.Equal(3, CareerSummary.TotalExperienceInYears(experience, AsOf));
    }

    [Fact]
    public void ExperiencePhrase_UsesAHalfYearWhenTheRemainderWarrantsIt()
    {
        ExperienceEntry[] experience = [Role("A", "2023-03", null)]; // 42 months

        Assert.Equal("3.5+ years", CareerSummary.ExperiencePhrase(experience, AsOf));
    }

    [Fact]
    public void InReverseChronologicalOrder_PutsTheOngoingRoleFirst()
    {
        ExperienceEntry[] experience =
        [
            Role("PS Digital", "2023-03", "2024-07"),
            Role("Andalusia", "2025-11", null),
            Role("MEEM", "2024-07", "2024-11"),
        ];

        var ordered = CareerSummary.InReverseChronologicalOrder(experience);

        Assert.Equal(["Andalusia", "MEEM", "PS Digital"], ordered.Select(e => e.Company));
    }

    [Fact]
    public void InReverseChronologicalOrder_DoesNotThrowOnAnOngoingRole()
    {
        // Regression: an earlier implementation sorted ongoing roles using a far-future
        // sentinel date that YearMonth's own range validation rejected at runtime.
        ExperienceEntry[] experience = [Role("Andalusia", "2025-11", null)];

        var ordered = CareerSummary.InReverseChronologicalOrder(experience);

        Assert.Single(ordered);
    }

    [Fact]
    public void Employers_ListsARepeatEmployerOnlyOnce()
    {
        ExperienceEntry[] experience =
        [
            Role("PS Digital", "2023-03", "2024-07"),
            Role("MEEM", "2024-07", "2024-11"),
            Role("PS Digital", "2024-11", "2025-11"),
        ];

        var employers = CareerSummary.Employers(experience);

        Assert.Equal(2, employers.Count);
        Assert.Contains("PS Digital", employers);
        Assert.Contains("MEEM", employers);
    }
}
