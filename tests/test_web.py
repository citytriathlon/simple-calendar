from datetime import UTC, datetime, timedelta

import pytest


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("ICS_URL", "http://example.invalid/cal.ics")
    import app as app_module

    app_module.app.config.update(TESTING=True)
    return app_module


def test_health_reports_starting_before_first_fetch(client):
    client.calendar_data.started_at = datetime.now(UTC)
    client.calendar_data.last_success = None

    response = client.app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "starting"


def test_health_goes_stale_if_the_feed_is_never_reached(client):
    """A feed we have never reached must not look healthy forever."""
    client.calendar_data.last_success = None
    client.calendar_data.started_at = datetime.now(UTC) - timedelta(days=1)

    response = client.app.test_client().get("/health")
    assert response.status_code == 503
    assert response.get_json()["status"] == "stale"


def test_health_goes_stale_when_the_feed_ages_out(client):
    client.calendar_data.last_success = datetime.now(UTC) - timedelta(days=1)

    response = client.app.test_client().get("/health")
    assert response.status_code == 503
    assert response.get_json()["status"] == "stale"


def test_description_from_the_feed_is_escaped(client):
    """The feed is untrusted: anyone who can add an event must not inject script."""
    client.calendar_data.data = {
        "11. 08. 2026": [
            {
                "begin": "10:00",
                "end": "11:00",
                "all_day": False,
                "name": "Briefing",
                "description": "<img src=x onerror=alert(1)>",
                "location": "",
                "hue": 110,
                "organizer": "Jan N.",
                "begin_epoch": 0,
                "end_epoch": 1,
                "all_strings": "Briefing",
                "all_strings_date": "Briefing 11. 08. 2026",
            }
        ]
    }

    body = client.app.test_client().get("/").get_data(as_text=True)

    assert "<img src=x onerror=alert(1)>" not in body
    assert "&lt;img src=x onerror=alert(1)&gt;" in body


def test_start_updater_refuses_without_ics_url(monkeypatch):
    monkeypatch.delenv("ICS_URL", raising=False)
    import app as app_module

    monkeypatch.setattr(app_module.calendar_data, "url", None)
    with pytest.raises(RuntimeError, match="ICS_URL"):
        app_module.start_updater()
