import textwrap

import pytest


def make_ics(*events: str) -> str:
    body = "\n".join(textwrap.dedent(e).strip() for e in events)
    return (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//simple-calendar tests//EN\n"
        f"{body}\n"
        "END:VCALENDAR\n"
    )


@pytest.fixture
def calendar_data(monkeypatch):
    """A CalendarData bound to a fixed timezone and organizer domain."""
    monkeypatch.setenv("TIMEZONE", "Europe/Prague")
    monkeypatch.setenv("ORGANIZER_DOMAIN", "@citytriathlon.cz")
    from calendar_data import CalendarData

    return CalendarData()
