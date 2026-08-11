from datetime import UTC, datetime

from conftest import make_ics

TIMED_EVENT = """
    BEGIN:VEVENT
    UID:timed@test
    DTSTAMP:20260810T120000Z
    DTSTART:20260811T090000Z
    DTEND:20260811T100000Z
    SUMMARY:Morning briefing
    LOCATION:Tent A
    END:VEVENT
"""

# Started three days ago, still running - the event a "what's on now" board
# most needs, and the one the old start-based filter dropped.
IN_PROGRESS_MULTIDAY = """
    BEGIN:VEVENT
    UID:multiday@test
    DTSTAMP:20260805T120000Z
    DTSTART:20260808T080000Z
    DTEND:20260813T180000Z
    SUMMARY:Race week
    END:VEVENT
"""

FINISHED_EVENT = """
    BEGIN:VEVENT
    UID:finished@test
    DTSTAMP:20260101T120000Z
    DTSTART:20260101T090000Z
    DTEND:20260101T100000Z
    SUMMARY:Last year
    END:VEVENT
"""

ALL_DAY_EVENT = """
    BEGIN:VEVENT
    UID:allday@test
    DTSTAMP:20260810T120000Z
    DTSTART;VALUE=DATE:20260812
    DTEND;VALUE=DATE:20260813
    SUMMARY:Setup day
    END:VEVENT
"""

NOW = datetime(2026, 8, 11, 10, 0, tzinfo=UTC)


def test_name_mod_shortens_to_first_name_and_initials(calendar_data):
    assert calendar_data.name_mod("jan drozd novak") == "Jan D. N."
    assert calendar_data.name_mod("jan") == "Jan"
    assert calendar_data.name_mod("") == ""


def test_get_names_extracts_mentions(calendar_data):
    assert calendar_data.get_names("ping @jan and @petra") == ["Jan", "Petra"]
    assert calendar_data.get_names("mail me at foo@bar.com") == []
    assert calendar_data.get_names("") == []


def test_extract_organizer_shortens_configured_domain(calendar_data):
    organizer = "mailto:jan.novak@citytriathlon.cz"
    assert calendar_data.extract_organizer(organizer, "") == "Jan N."


def test_extract_organizer_passes_through_other_domains(calendar_data):
    assert calendar_data.extract_organizer("mailto:someone@example.com", "") == (
        "someone@example.com"
    )


def test_extract_organizer_falls_back_when_absent(calendar_data):
    assert calendar_data.extract_organizer(None, "") == "Unknown Organizer"


def test_finished_events_are_dropped(calendar_data):
    events = calendar_data.build_events(make_ics(FINISHED_EVENT), NOW)
    assert events == {}


def test_in_progress_multiday_event_is_kept(calendar_data):
    events = calendar_data.build_events(make_ics(IN_PROGRESS_MULTIDAY), NOW)
    names = [e["name"] for day in events.values() for e in day]
    assert names == ["Race week"]


def test_timed_event_is_grouped_and_formatted(calendar_data):
    events = calendar_data.build_events(make_ics(TIMED_EVENT), NOW)
    assert list(events) == ["11. 08. 2026"]

    entry = events["11. 08. 2026"][0]
    # 09:00Z is 11:00 in Europe/Prague (CEST).
    assert entry["begin"] == "11:00"
    assert entry["end"] == "12:00"
    assert entry["all_day"] is False
    assert entry["location"] == "Tent A"
    assert "11. 08. 2026" in entry["all_strings_date"]


def test_all_day_event_has_no_time_range_and_keeps_its_date(calendar_data):
    events = calendar_data.build_events(make_ics(ALL_DAY_EVENT), NOW)
    assert list(events) == ["12. 08. 2026"]

    entry = events["12. 08. 2026"][0]
    assert entry["all_day"] is True
    assert entry["begin"] == ""
    assert entry["end"] == ""


def test_epoch_values_are_millisecond_precision(calendar_data):
    events = calendar_data.build_events(make_ics(TIMED_EVENT), NOW)
    entry = events["11. 08. 2026"][0]
    assert entry["end_epoch"] - entry["begin_epoch"] == 3600 * 1000


def test_unknown_timezone_falls_back_rather_than_raising(monkeypatch):
    monkeypatch.setenv("TIMEZONE", "Not/AZone")
    from calendar_data import CalendarData

    assert str(CalendarData().local_tz) == "Europe/Prague"
