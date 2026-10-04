using System.Text.Json;
using System.Text.Json.Serialization;
using Cv.Domain;

namespace Cv.Application;

/// <summary>
/// The one place JSON settings are defined.
/// </summary>
/// <remarks>
/// Reading and writing must be exactly symmetrical: the editor exports a file that the
/// app then loads as canonical input. If the two used different options, a round-trip
/// through the editor would silently corrupt the CV.
/// </remarks>
public static class CvJson
{
    public static readonly JsonSerializerOptions Options = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Converters = { new JsonStringEnumConverter() },
    };

    public static CvDocument Deserialize(string json) =>
        JsonSerializer.Deserialize<CvDocument>(json, Options)
        ?? throw new InvalidOperationException("The CV document deserialized to null.");

    public static string Serialize(CvDocument document) =>
        JsonSerializer.Serialize(document, Options);
}
