using System.Net.Http.Json;
using Cv.Application;
using Cv.Domain;

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

    private CvDocument? cached;

    /// <summary>The canonical document, fetched once per session.</summary>
    public async Task<CvDocument> GetAsync(CancellationToken cancellationToken = default)
    {
        // Deliberately not thread-safe: Blazor WebAssembly is single-threaded, so a lock
        // here would be ceremony without benefit.
        cached ??= await httpClient.GetFromJsonAsync<CvDocument>(DataPath, CvJson.Options, cancellationToken)
                   ?? throw new InvalidOperationException($"'{DataPath}' deserialized to null.");

        return cached;
    }

    /// <summary>Replaces the in-memory document. Used by the editor's live preview.</summary>
    /// <remarks>
    /// This changes only the current session. The committed <c>data/cv.json</c> stays
    /// canonical; the editor's export is what makes a change permanent.
    /// </remarks>
    public void Replace(CvDocument document) => cached = document;
}
