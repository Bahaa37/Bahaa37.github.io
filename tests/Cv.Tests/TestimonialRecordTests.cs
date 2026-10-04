using Cv.Application;
using Cv.Domain;
using System.Text.Json;

namespace Cv.Tests;

/// <summary>
/// Exercises the real testimonials.json rather than a fixture.
/// </summary>
/// <remarks>
/// A testimonial puts words in a named person's mouth on a public CV site, so the bar
/// for what may render is strict: a real name, real words, and a link that lets a
/// reader verify the person exists and actually said it. These tests fail the build
/// the moment an entry shows up without that attribution.
/// </remarks>
public class TestimonialRecordTests
{
    private static string TestimonialsJsonPath()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);

        while (directory is not null)
        {
            var candidate = Path.Combine(directory.FullName, "src", "Cv.Web", "wwwroot", "data", "testimonials.json");
            if (File.Exists(candidate))
            {
                return candidate;
            }

            directory = directory.Parent;
        }

        throw new FileNotFoundException("Could not locate src/Cv.Web/wwwroot/data/testimonials.json by walking up from the test output directory.");
    }

    private static IReadOnlyList<Testimonial> LoadTestimonials()
        => JsonSerializer.Deserialize<IReadOnlyList<Testimonial>>(
               JsonDocument.Parse(File.ReadAllText(TestimonialsJsonPath()))
                   .RootElement.GetProperty("testimonials").GetRawText(),
               CvJson.Options)
           ?? throw new InvalidOperationException("testimonials.json deserialized to null.");

    [Fact]
    public void TheRealFileDeserializes()
    {
        Assert.NotNull(LoadTestimonials());
    }

    [Fact]
    public void EveryEntryHasANameAndWords()
    {
        foreach (var testimonial in LoadTestimonials())
        {
            Assert.False(string.IsNullOrWhiteSpace(testimonial.Name), "a testimonial without a name cannot be attributed.");
            Assert.False(string.IsNullOrWhiteSpace(testimonial.Text), "a testimonial without text is a placeholder, not a quote.");
        }
    }

    [Fact]
    public void EveryEntryCarriesAProfileLink()
    {
        foreach (var testimonial in LoadTestimonials())
        {
            var links = new[] { testimonial.LinkedIn, testimonial.GitHub }
                .Where(link => !string.IsNullOrWhiteSpace(link))
                .ToList();

            // The whole point of the feature: a reader can check that the person exists.
            // A quote with no profile link is unverifiable, so it does not render.
            Assert.NotEmpty(links);
            Assert.All(links, link => Assert.True(
                Uri.TryCreate(link, UriKind.Absolute, out var uri)
                && uri.Scheme is "http" or "https",
                $"'{link}' is not an absolute http(s) URL."));
        }
    }

    [Fact]
    public void NoNameSaysTheSameThingTwice()
    {
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (var testimonial in LoadTestimonials())
        {
            // Same person twice is plausible; the same words twice is a copy-paste bug.
            Assert.True(seen.Add($"{testimonial.Name}|{testimonial.Text}"),
                $"'{testimonial.Name}' appears with duplicate text.");
        }
    }

    [Fact]
    public void DatesWhenPresentAreYearMonth()
    {
        foreach (var testimonial in LoadTestimonials())
        {
            if (string.IsNullOrWhiteSpace(testimonial.Date))
            {
                continue;
            }

            Assert.Matches(@"^\d{4}-(0[1-9]|1[0-2])$", testimonial.Date);
        }
    }
}
