from datetime import date
import holidays as hdays

# Victorian school holiday periods (dates inclusive).
# Source: Victorian Department of Education published term dates.
# 2026+ dates are approximate based on the standard 4-term calendar.
SCHOOL_HOLIDAYS = [
    # 2023
    (date(2023,  1,  1), date(2023,  1, 29), "Summer"),
    (date(2023,  4,  1), date(2023,  4, 17), "Autumn"),
    (date(2023,  6, 24), date(2023,  7,  9), "Winter"),
    (date(2023,  9, 16), date(2023, 10,  1), "Spring"),
    (date(2023, 12, 22), date(2023, 12, 31), "Summer"),
    # 2024
    (date(2024,  1,  1), date(2024,  1, 28), "Summer"),
    (date(2024,  3, 28), date(2024,  4, 14), "Autumn"),
    (date(2024,  6, 29), date(2024,  7, 14), "Winter"),
    (date(2024,  9, 21), date(2024, 10,  6), "Spring"),
    (date(2024, 12, 20), date(2024, 12, 31), "Summer"),
    # 2025
    (date(2025,  1,  1), date(2025,  1, 27), "Summer"),
    (date(2025,  4,  5), date(2025,  4, 22), "Autumn"),
    (date(2025,  6, 28), date(2025,  7, 13), "Winter"),
    (date(2025,  9, 20), date(2025, 10,  5), "Spring"),
    (date(2025, 12, 19), date(2025, 12, 31), "Summer"),
    # 2026 (approximate)
    (date(2026,  1,  1), date(2026,  1, 26), "Summer"),
    (date(2026,  4,  4), date(2026,  4, 19), "Autumn"),
    (date(2026,  6, 27), date(2026,  7, 12), "Winter"),
    (date(2026,  9, 19), date(2026, 10,  4), "Spring"),
    (date(2026, 12, 18), date(2026, 12, 31), "Summer"),
]


def get_holiday_info(d: date) -> dict:
    """
    Returns public and school holiday info for a given date in Victoria.

    Public holidays: national Australian holidays + VIC-specific holidays.
    holidays.Australia(state='VIC') covers both; other states' exclusive
    holidays (e.g. QLD Ekka, WA Foundation Day) are not included.
    """
    vic_holidays = hdays.Australia(state="VIC", years=d.year)
    holiday_name = vic_holidays.get(d)
    is_public = holiday_name is not None

    is_school = False
    school_holiday_name = None
    for start, end, period in SCHOOL_HOLIDAYS:
        if start <= d <= end:
            is_school = True
            school_holiday_name = f"{period} school holidays"
            break

    return {
        "is_public_holiday":    int(is_public),
        "holiday_name":         holiday_name or "",
        "is_school_holiday":    int(is_school),
        "school_holiday_name":  school_holiday_name or "",
    }
