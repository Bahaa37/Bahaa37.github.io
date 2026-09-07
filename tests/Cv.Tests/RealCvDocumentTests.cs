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

        // GitHub is still missing, which is only a warning. Anything at Error severity
        // is a defect a recruiter would notice, and must not survive into a build.
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
