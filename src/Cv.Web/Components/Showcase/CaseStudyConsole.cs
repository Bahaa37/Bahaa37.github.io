using System.Net;
using Cv.Domain;
using Microsoft.AspNetCore.Components;

namespace Cv.Web.Components.Showcase;

/// <summary>
/// How a case study prints in a Hairline console: one shape, read only from the study's
/// own record. The hero and the style guide both render it; prerender.py's
/// <c>_console_run_lines</c> is the static mirror, so a change here is a change there.
/// </summary>
public static class CaseStudyConsole
{
    /// <summary>
    /// The study's page: the long-form write-up where one exists, otherwise its generated
    /// page, the same URL Home's case index links. No study means the home page.
    /// </summary>
    public static string StudyUrl(CaseStudy? study) =>
        study is null ? "/" : study.HasWriteup ? study.WriteupUrl! : $"/work/{study.Slug}";

    /// <summary>The study's situation in one line: the first sentence, full stop kept.</summary>
    public static string FirstSentence(string summary)
    {
        var cut = summary.IndexOf(". ", StringComparison.Ordinal);

        return cut < 0 ? summary : summary[..(cut + 1)];
    }

    /// <summary>
    /// One console run: command, the situation, the stack trail, the outcome and the link
    /// into the full study. The same lines render into a visible log and into each run's
    /// template, so a static page shows a finished run and the kit replays the rest.
    /// </summary>
    public static MarkupString RunLines(CaseStudy study)
    {
        static string Encode(string value) => WebUtility.HtmlEncode(value);

        var result = $"""
            <p class="hl-window__line hl-window__line--cmd">open {Encode(study.Slug)}</p>
            <p class="hl-window__line hl-window__line--muted">{Encode(FirstSentence(study.Summary))}</p>
            <p class="hl-window__line hl-window__line--info">{Encode(string.Join(" → ", study.Stack.Take(4)))}</p>
            <p class="hl-window__result">◆ {Encode(study.Outcomes.FirstOrDefault() ?? "")} <a href="{Encode(StudyUrl(study))}">Read the case study →</a></p>
            """;

        return new MarkupString(result);
    }
}
