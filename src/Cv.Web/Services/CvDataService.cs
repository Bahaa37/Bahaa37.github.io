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

    private CvDocument? cached;
    private IReadOnlyList<DecisionRecord>? cachedDecisions;

    /// <summary>The canonical document, fetched once per session.</summary>
    public async Task<CvDocument> GetAsync(CancellationToken cancellationToken = default)
    {
        // Deliberately not thread-safe: Blazor WebAssembly is single-threaded, so a lock
        // here would be ceremony without benefit.
        cached ??= await GetFreshAsync<CvDocument>(DataPath, cancellationToken);

        return cached;
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
    public async Task<IReadOnlyList<DecisionRecord>> GetDecisionsAsync(
        CancellationToken cancellationToken = default)
    {
        cachedDecisions ??= (await GetFreshAsync<DecisionFile>(DecisionsPath, cancellationToken)).Decisions;

        return cachedDecisions;
    }

    private sealed record DecisionFile(IReadOnlyList<DecisionRecord> Decisions);

    /// <summary>Replaces the in-memory document. Used by the editor's live preview.</summary>
    /// <remarks>
    /// This changes only the current session. The committed <c>data/cv.json</c> stays
    /// canonical; the editor's export is what makes a change permanent.
    /// </remarks>
    public void Replace(CvDocument document) => cached = document;
}
