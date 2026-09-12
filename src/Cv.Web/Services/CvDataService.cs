using System.Net.Http.Json;
using Cv.Application;
using Cv.Domain;
using Microsoft.AspNetCore.Components.WebAssembly.Http;

namespace Cv.Web.Services;

/// <summary>
/// Loads the canonical CV document over HTTP and caches it for the session.
/// </summary>
/// <remarks>
/// In the browser there is no filesystem — <c>data/cv.json</c> is fetched as a static
/// asset. Every renderer goes through this one service so the single-source-of-truth
/// guarantee holds at runtime and not merely in the design.
/// </remarks>
public sealed class CvDataService(HttpClient httpClient)
{
    private const string DataPath = "data/cv.json";
    private const string DecisionsPath = "data/decisions.json";

    private Task<CvDocument>? pending;
    private Task<IReadOnlyList<DecisionRecord>>? pendingDecisions;

    /// <summary>The canonical document, fetched once per session.</summary>
    public Task<CvDocument> GetAsync(CancellationToken cancellationToken = default)
    {
        // The cache holds the in-flight task, not the result. Blazor WebAssembly is
        // single-threaded, so a lock would be ceremony — but callers await, and two of
        // them can both evaluate `??=` before either assignment lands, each starting
        // its own request. The network trace showed a duplicate cv.json download on
        // every cold load for exactly this reason. A failed fetch clears the slot so
        // the next caller retries instead of caching the exception.
        pending ??= Fetch(cancellationToken);
        return pending;

        async Task<CvDocument> Fetch(CancellationToken ct)
        {
            try { return await GetFreshAsync<CvDocument>(DataPath, ct); }
            catch { pending = null; throw; }
        }
    }

    /// <summary>
    /// Fetches a data file, forcing the browser to revalidate it rather than serve a
    /// cached copy.
    /// </summary>
    /// <remarks>
    /// The framework's assets carry a fingerprint in their URL, and the prerenderer
    /// appends a content hash to the stylesheets — but these files are fetched by path
    /// from here, so neither mechanism reaches them. Without this, a returning browser
    /// runs new application code against an old CV: the site showed a job title that had
    /// already been replaced, and silently dropped the profile fields added alongside it.
    ///
    /// NoCache revalidates rather than re-downloads. An unchanged file answers 304 and
    /// costs a conditional request; only a changed one is transferred. Staleness on a
    /// document whose entire purpose is being current is not worth saving that.
    /// </remarks>
    private async Task<T> GetFreshAsync<T>(string path, CancellationToken cancellationToken)
    {
        using var request = new HttpRequestMessage(HttpMethod.Get, path);
        request.SetBrowserRequestCache(BrowserRequestCache.NoCache);

        using var response = await httpClient.SendAsync(request, cancellationToken);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<T>(CvJson.Options, cancellationToken)
               ?? throw new InvalidOperationException($"'{path}' deserialized to null.");
    }

    /// <summary>
    /// The architecture decision records, fetched once per session.
    /// </summary>
    /// <remarks>
    /// Held separately from the CV rather than folded into it. They are a different kind
    /// of document with a different audience — nothing here belongs on a printed CV or
    /// in an ATS — and keeping them apart means the CV's schema, its validator and its
    /// text-extraction gate stay about the CV.
    /// </remarks>
    public Task<IReadOnlyList<DecisionRecord>> GetDecisionsAsync(
        CancellationToken cancellationToken = default)
    {
        pendingDecisions ??= FetchDecisions(cancellationToken);
        return pendingDecisions;

        async Task<IReadOnlyList<DecisionRecord>> FetchDecisions(CancellationToken ct)
        {
            try
            {
                var file = await GetFreshAsync<DecisionFile>(DecisionsPath, ct);
                return file.Decisions;
            }
            catch { pendingDecisions = null; throw; }
        }
    }

    private sealed record DecisionFile(IReadOnlyList<DecisionRecord> Decisions);

    /// <summary>Replaces the in-memory document. Used by the editor's live preview.</summary>
    /// <remarks>
    /// This changes only the current session. The committed <c>data/cv.json</c> stays
    /// canonical; the editor's export is what makes a change permanent.
    /// </remarks>
    public void Replace(CvDocument document) => pending = Task.FromResult(document);
}
