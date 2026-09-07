using Cv.Application;
using Cv.Domain;

namespace Cv.Tests;

public class CvValidatorTests
{
    private static readonly YearMonth AsOf = YearMonth.Parse("2026-09");

    private static CvDocument DocumentWith(params ExperienceEntry[] experience) => new()
    {
        Profile = new Profile
        {
            Name = "Test Person",
            Title = "Engineer",
            Location = "Alexandria, Egypt",
            Phone = "+20 128 458 6608",
            Email = "test@example.com",
            GitHub = "https://github.com/example",
            Website = "https://example.github.io",
        },
        Summary = "Summary.",
        Experience = experience,
    };

    private static ExperienceEntry Role(string company, string start, string? end, EmploymentType type) => new()
    {
        Company = company,
        Role = "Engineer",
        EmploymentType = type,
        Period = new DateRange(YearMonth.Parse(start), end is null ? null : YearMonth.Parse(end)),
    };

    [Fact]
    public void ReportsAnErrorWhenTwoFullTimeRolesOverlap()
    {
        // This is the exact defect found on the original CV.
        var document = DocumentWith(
            Role("PS Digital", "2023-03", "2025-11", EmploymentType.FullTime),
            Role("MEEM", "2024-07", "2024-11", EmploymentType.FullTime));

        var errors = CvValidator.Validate(document, AsOf)
            .Where(i => i.Severity == IssueSeverity.Error)
            .ToList();

        Assert.Single(errors);
        Assert.Contains("Two full-time roles overlap", errors[0].Message);
    }

    [Fact]
    public void AllowsAPartTimeRoleToOverlapAFullTimeOne()
    {
        var document = DocumentWith(
            Role("PS Digital", "2023-03", "2025-11", EmploymentType.FullTime),
            Role("MEEM", "2024-07", "2024-11", EmploymentType.PartTime));

        Assert.DoesNotContain(
            CvValidator.Validate(document, AsOf),
            i => i.Severity == IssueSeverity.Error);
    }

    [Fact]
    public void AllowsConsecutiveFullTimeRolesThatMerelyTouch()
    {
        var document = DocumentWith(
            Role("PS Digital", "2023-03", "2024-07", EmploymentType.FullTime),
            Role("MEEM", "2024-08", "2024-11", EmploymentType.FullTime));

        Assert.DoesNotContain(
            CvValidator.Validate(document, AsOf),
            i => i.Severity == IssueSeverity.Error);
    }

    [Fact]
    public void AllowsAJobChangeThatSharesItsBoundaryMonth()
    {
        // Leaving one employer in July and starting the next in July is how a job change
        // is normally written. It must not be reported as two concurrent roles.
        var document = DocumentWith(
            Role("PS Digital", "2023-03", "2024-07", EmploymentType.FullTime),
            Role("MEEM", "2024-07", "2024-11", EmploymentType.FullTime));

        Assert.DoesNotContain(
            CvValidator.Validate(document, AsOf),
            i => i.Severity == IssueSeverity.Error);
    }

    [Fact]
    public void StillReportsAnOverlapThatExtendsBeyondASingleSharedMonth()
    {
        var document = DocumentWith(
            Role("PS Digital", "2023-03", "2024-09", EmploymentType.FullTime),
            Role("MEEM", "2024-07", "2024-11", EmploymentType.FullTime));

        Assert.Contains(
            CvValidator.Validate(document, AsOf),
            i => i.Severity == IssueSeverity.Error);
    }

    [Fact]
    public void WarnsAboutHighlightsThatCarryNoMetric()
    {
        var role = Role("Andalusia", "2025-11", null, EmploymentType.FullTime) with
        {
            Highlights =
            [
                new Highlight { Text = "Significantly improved performance." },
                new Highlight { Text = "Cut the upgrade cycle.", Metric = "5–7 days reduced to 3" },
            ],
        };

        var warnings = CvValidator.Validate(DocumentWith(role), AsOf)
            .Where(i => i.Severity == IssueSeverity.Warning)
            .ToList();

        Assert.Single(warnings);
        Assert.Contains("Significantly improved", warnings[0].Message);
    }

    [Fact]
    public void FlagsAPhoneNumberKeepingATrunkZeroAfterTheCountryCode()
    {
        var document = DocumentWith(Role("A", "2023-03", null, EmploymentType.FullTime));
        document = document with
        {
            Profile = document.Profile with { Phone = "+20 01284586608" },
        };

        Assert.Contains(
            CvValidator.Validate(document, AsOf),
            i => i.Severity == IssueSeverity.Error && i.Message.Contains("click-to-call"));
    }

    [Fact]
    public void ReportsATechnologyVersionThatDidNotExistDuringTheRole()
    {
        // The original CV claimed a ".NET 9 Web API" built in a role ending July 2024.
        // .NET 9 shipped in November 2024.
        var role = Role("PS Digital", "2023-03", "2024-07", EmploymentType.FullTime) with
        {
            Highlights = [new Highlight { Text = "Rebuilt the application as a .NET 9 Web API." }],
        };

        Assert.Contains(
            CvValidator.Validate(DocumentWith(role), AsOf),
            i => i.Severity == IssueSeverity.Error && i.Message.Contains(".NET 9 was released"));
    }

    [Fact]
    public void AcceptsATechnologyVersionThatShippedBeforeTheRoleEnded()
    {
        var role = Role("PS Digital", "2023-03", "2024-07", EmploymentType.FullTime) with
        {
            Highlights = [new Highlight { Text = "Rebuilt the application as a .NET 8 Web API." }],
        };

        Assert.DoesNotContain(
            CvValidator.Validate(DocumentWith(role), AsOf),
            i => i.Severity == IssueSeverity.Error);
    }

    [Fact]
    public void AllowsAnOngoingRoleToMentionAnyReleasedVersion()
    {
        var role = Role("Andalusia", "2025-11", null, EmploymentType.FullTime) with
        {
            Highlights = [new Highlight { Text = "Targeting .NET 10 across the estate." }],
        };

        Assert.DoesNotContain(
            CvValidator.Validate(DocumentWith(role), AsOf),
            i => i.Severity == IssueSeverity.Error);
    }

    [Fact]
    public void DoesNotMistakeDotNetTenForDotNetOne()
    {
        var role = Role("Andalusia", "2023-03", "2024-07", EmploymentType.FullTime) with
        {
            Highlights = [new Highlight { Text = "Worked with .NET 10 features." }],
        };

        // .NET 10 postdates this role, so exactly one error — not a spurious ".NET 1" match too.
        var errors = CvValidator.Validate(DocumentWith(role), AsOf)
            .Where(i => i.Severity == IssueSeverity.Error)
            .ToList();

        Assert.Single(errors);
        Assert.Contains(".NET 10 was released", errors[0].Message);
    }

    [Fact]
    public void WarnsWhenNoPortfolioUrlIsPresent()
    {
        // Without it the printed CV has no route to the case studies and diagrams.
        var document = DocumentWith(Role("A", "2023-03", null, EmploymentType.FullTime));
        document = document with { Profile = document.Profile with { Website = null } };

        Assert.Contains(
            CvValidator.Validate(document, AsOf),
            i => i.Message.Contains("No portfolio URL"));
    }

    [Fact]
    public void WarnsWhenNoGitHubLinkIsPresent()
    {
        var document = DocumentWith(Role("A", "2023-03", null, EmploymentType.FullTime));
        document = document with { Profile = document.Profile with { GitHub = null } };

        Assert.Contains(
            CvValidator.Validate(document, AsOf),
            i => i.Message.Contains("No GitHub link"));
    }
}
