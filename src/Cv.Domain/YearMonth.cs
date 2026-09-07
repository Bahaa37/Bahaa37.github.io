using System.Globalization;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Cv.Domain;

/// <summary>
/// A month-precision point in time, stored as "YYYY-MM".
/// </summary>
/// <remarks>
/// CV dates are never day-precise, and storing them as display text ("March 2023")
/// makes them impossible to sort, compare, or compute durations from. This type keeps
/// the data numeric so the timeline and the "years of experience" figure are both
/// derived rather than typed by hand — which is what stops them going stale.
/// </remarks>
[JsonConverter(typeof(YearMonthJsonConverter))]
public readonly record struct YearMonth : IComparable<YearMonth>
{
    public int Year { get; }

    public int Month { get; }

    public YearMonth(int year, int month)
    {
        if (year is < 1900 or > 2200)
        {
            throw new ArgumentOutOfRangeException(nameof(year), year, "Year must be between 1900 and 2200.");
        }

        if (month is < 1 or > 12)
        {
            throw new ArgumentOutOfRangeException(nameof(month), month, "Month must be between 1 and 12.");
        }

        Year = year;
        Month = month;
    }

    public static YearMonth Parse(string value) =>
        TryParse(value, out var result)
            ? result
            : throw new FormatException($"Expected a date in 'YYYY-MM' format but received '{value}'.");

    public static bool TryParse(string? value, out YearMonth result)
    {
        result = default;

        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        var parts = value.Split('-');
        if (parts.Length != 2)
        {
            return false;
        }

        if (!int.TryParse(parts[0], NumberStyles.None, CultureInfo.InvariantCulture, out var year) ||
            !int.TryParse(parts[1], NumberStyles.None, CultureInfo.InvariantCulture, out var month))
        {
            return false;
        }

        if (year is < 1900 or > 2200 || month is < 1 or > 12)
        {
            return false;
        }

        result = new YearMonth(year, month);
        return true;
    }

    public static YearMonth FromDateTime(DateTime value) => new(value.Year, value.Month);

    /// <summary>Total months since year zero. Used for comparisons and durations.</summary>
    private int AbsoluteMonths => (Year * 12) + Month;

    /// <summary>Whole months from this point up to <paramref name="later"/>, never negative.</summary>
    public int MonthsUntil(YearMonth later) => Math.Max(0, later.AbsoluteMonths - AbsoluteMonths);

    public int CompareTo(YearMonth other) => AbsoluteMonths.CompareTo(other.AbsoluteMonths);

    public static bool operator <(YearMonth left, YearMonth right) => left.CompareTo(right) < 0;

    public static bool operator >(YearMonth left, YearMonth right) => left.CompareTo(right) > 0;

    public static bool operator <=(YearMonth left, YearMonth right) => left.CompareTo(right) <= 0;

    public static bool operator >=(YearMonth left, YearMonth right) => left.CompareTo(right) >= 0;

    /// <summary>The storage form: "YYYY-MM".</summary>
    public override string ToString() => $"{Year:D4}-{Month:D2}";

    /// <summary>The display form: "March 2023".</summary>
    public string ToDisplayString() =>
        $"{CultureInfo.InvariantCulture.DateTimeFormat.GetMonthName(Month)} {Year}";

    /// <summary>The compact display form: "Mar 2023".</summary>
    public string ToShortDisplayString() =>
        $"{CultureInfo.InvariantCulture.DateTimeFormat.GetAbbreviatedMonthName(Month)} {Year}";
}

internal sealed class YearMonthJsonConverter : JsonConverter<YearMonth>
{
    public override YearMonth Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options) =>
        YearMonth.Parse(reader.GetString() ?? string.Empty);

    public override void Write(Utf8JsonWriter writer, YearMonth value, JsonSerializerOptions options) =>
        writer.WriteStringValue(value.ToString());
}
