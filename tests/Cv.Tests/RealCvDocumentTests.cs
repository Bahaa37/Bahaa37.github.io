using Cv.Application;
using Cv.Domain;

namespace Cv.Tests;

/// <summary>
/// Exercises the real cv.json rather than a fixture.
/// </summary>
/// <remarks>
/// The whole design rests on cv.json being the single source of truth, so a schema
/// drift between the file and the records would break all three renderers at once.
/// These tests fail loudly the moment the file and the model disagree.
/// </remarks>
public class RealCvDocumentTests
{
    private static readonly YearMonth AsOf = YearMonth.Parse("2026-09");

    private static string CvJsonPath()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);

        while (directory is not null)
        {
            var candidate = Path.Combine(directory.FullName, "src", "Cv.Web", "wwwroot", "data", "cv.json");
            if (File.Exists(candidate))
            {
                return candidate;
            }

            directory = directory.Parent;
        }

        throw new FileNotFoundException("Could not locate src/Cv.Web/wwwroot/data/cv.json by walking up from the test output directory.");
    }

    private static CvDocument LoadDocument() => CvJson.Deserialize(File.ReadAllText(CvJsonPath()));

    [Fact]
    public void TheRealDocumentDeserializes()
    {
        var document = LoadDocument();

        Assert.Equal("Bahaa Aldeen Mohamed", document.Profile.Name);
        Assert.NotEmpty(document.Experience);
        Assert.NotEmpty(document.SkillGroups);
        Assert.NotEmpty(document.Certifications);
        Assert.NotEmpty(document.CaseStudies);
    }

    [Fact]
    public void TheRealDocumentHasNoBlockingErrors()
    {
        var errors = CvValidator.Validate(LoadDocument(), AsOf)
            .Where(i => i.Severity == IssueSeverity.Error)
            .ToList();

        // Warnings are tolerated — an unquantified bullet is worth seeing, not worth
        // blocking on. Anything at Error severity is a defect a recruiter would notice,
        // and must not survive into a build.
        Assert.True(
            errors.Count == 0,
            "Blocking CV issues found:" + Environment.NewLine +
            string.Join(Environment.NewLine, errors.Select(e => $"  [{e.Location}] {e.Message}")));
    }

    [Fact]
    public void NoTwoFullTimeRolesOverlap()
    {
        var fullTime = LoadDocument().Experience
            .Where(e => e.EmploymentType == EmploymentType.FullTime)
            .ToList();

        foreach (var (first, second) in fullTime.SelectMany(
                     (a, i) => fullTime.Skip(i + 1).Select(b => (a, b))))
        {
            Assert.False(
                first.Period.Overlaps(second.Period, AsOf),
                $"'{first.Role}' at {first.Company} overlaps '{second.Role}' at {second.Company}.");
        }
    }

    [Fact]
    public void TheAwardedMetricIsPresentOnTheFlagshipAchievement()
    {
        // The 5-7 days to 3 figure is the strongest line on the CV. If a refactor of the
        // data ever drops it, that is a regression worth failing the build over.
        var metrics = LoadDocument().Experience
            .SelectMany(e => e.Highlights)
            .Where(h => h.HasMetric)
            .Select(h => h.Metric!)
            .ToList();

        Assert.Contains(metrics, m => m.Contains("3", StringComparison.Ordinal) && m.Contains("5-7", StringComparison.Ordinal));
    }

    [Fact]
    public void ExperienceIsContinuousFromTheFirstRoleToToday()
    {
        var document = LoadDocument();
        var months = CareerSummary.TotalExperienceInMonths(document.Experience, AsOf);

        // March 2023 through September 2026.
        Assert.Equal(42, months);
        Assert.Equal("3.5+ years", CareerSummary.ExperiencePhrase(document.Experience, AsOf));
    }

    [Fact]
    public void FeaturedCertificationsFitOnAPrintedPage()
    {
        var featured = LoadDocument().Certifications.Where(c => c.IsFeatured).ToList();

        Assert.InRange(featured.Count, 3, 6);
    }

    [Fact]
    public void CaseStudySlugsAreUniqueSoDeepLinksResolve()
    {
        var slugs = LoadDocument().CaseStudies.Select(c => c.Slug).ToList();

        Assert.Equal(slugs.Count, slugs.Distinct(StringComparer.OrdinalIgnoreCase).Count());
    }

    [Fact]
    public void CaseStudyDisplayOrdersAreUniqueSoTheOrderIsDeterministic()
    {
        var orders = LoadDocument().CaseStudies.Select(c => c.DisplayOrder).ToList();

        Assert.Equal(orders.Count, orders.Distinct().Count());
    }

    [Fact]
    public void TheShortSummaryStaysShortEnoughToBeRead()
    {
        // The showcase summary is the first prose a recruiter meets, and it competes with
        // the back button. The long version lives in SummaryExtended and is what the
        // printed CV renders, so there is no pressure to say everything here.
        var words = LoadDocument().Summary.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;

        Assert.InRange(words, 30, 90);
    }

    [Fact]
    public void ThePrintedCvStillCarriesTheLongSummary()
    {
        var document = LoadDocument();

        Assert.False(
            string.IsNullOrWhiteSpace(document.SummaryExtended),
            "summaryExtended is empty, so /cv would silently fall back to the short summary " +
            "and the printed CV would lose the depth an ATS indexes.");
        Assert.True(
            document.SummaryExtended!.Length > document.Summary.Length,
            "summaryExtended is no longer than summary, which inverts the point of having both.");
    }

    [Fact]
    public void TheProfileAnswersTheFirstQuestionsARecruiterAsks()
    {
        // Timezone, notice and languages decide whether a remote or relocation
        // application gets a reply at all. Their absence is a silent conversion loss,
        // which is exactly the kind of defect this suite exists to make loud.
        var profile = LoadDocument().Profile;

        Assert.False(string.IsNullOrWhiteSpace(profile.Timezone));
        Assert.False(string.IsNullOrWhiteSpace(profile.Availability));
        Assert.False(string.IsNullOrWhiteSpace(profile.Relocation));
        Assert.NotEmpty(profile.Languages);
    }

    [Fact]
    public void TheSkillsListStaysShortEnoughToReadAsASpecialism()
    {
        // Ten flat categories read as a developer's inventory; a handful reads as a
        // practitioner with a specialty. The cap is the whole point of the regrouping,
        // so it is enforced rather than left to discipline.
        var groups = LoadDocument().SkillGroups;

        Assert.InRange(groups.Count, 4, 7);
    }

    [Fact]
    public void TheSkillsListKeepsNoDuplicatesAcrossGroups()
    {
        // A skill in two groups is a regrouping that was half-finished, and it shows up
        // on the page as the same chip twice.
        var skills = LoadDocument().SkillGroups.SelectMany(g => g.Skills).ToList();

        var duplicated = skills
            .GroupBy(s => s, StringComparer.OrdinalIgnoreCase)
            .Where(g => g.Count() > 1)
            .Select(g => g.Key)
            .ToList();

        Assert.True(duplicated.Count == 0, "Skills listed in more than one group: " + string.Join(", ", duplicated));
    }

    [Fact]
    public void TheDataFileHasNoByteOrderMark()
    {
        // A BOM breaks strict JSON parsers, and Windows tooling adds one readily.
        var bytes = File.ReadAllBytes(CvJsonPath());

        Assert.False(
            bytes.Length >= 3 && bytes[0] == 0xEF && bytes[1] == 0xBB && bytes[2] == 0xBF,
            "cv.json starts with a UTF-8 BOM. Rewrite it without one.");
    }

    [Fact]
    public void TheDocumentSurvivesARoundTripThroughTheEditorsSerializer()
    {
        // The editor exports JSON that is then committed back as canonical input.
        // An asymmetric serializer would silently corrupt the CV on every export.
        //
        // Compared as serialized text rather than by record equality: C# records compare
        // collection properties by reference, so Assert.Equal on the documents would fail
        // even on a perfect round-trip and would tell us nothing.
        var original = LoadDocument();

        var once = CvJson.Serialize(original);
        var twice = CvJson.Serialize(CvJson.Deserialize(once));

        Assert.Equal(once, twice);
    }
}
