import asyncio
import logging
import os
import threading
from datetime import UTC, datetime

from flask import Flask, jsonify, render_template

from calendar_data import CalendarData
from i18n import DEFAULT_LANG, get_strings

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
calendar_data = CalendarData()
strings = get_strings(os.environ.get("APP_LANG", DEFAULT_LANG))

# The refresh loop must start under gunicorn too, not just `python app.py`,
# so it lives at module scope behind an idempotent guard.
_updater_lock = threading.Lock()
_updater_started = False


def start_updater() -> None:
    global _updater_started

    if not calendar_data.url:
        raise RuntimeError(
            "ICS_URL environment variable is not set - refusing to start. "
            "Point it at the ICS feed you want to display."
        )

    with _updater_lock:
        if _updater_started:
            return
        _updater_started = True

    threading.Thread(
        target=lambda: asyncio.run(calendar_data.update_data()),
        daemon=True,
        name="ics-updater",
    ).start()
    logger.info("Started ICS updater (every %ss)", calendar_data.update_interval)


@app.route("/")
def mainpage():
    return render_template("index.html", data=calendar_data.get_recent_events(), s=strings)


@app.route("/health")
def health():
    """Reports feed freshness, not just process liveness."""
    grace = calendar_data.update_interval * 10

    if calendar_data.last_success is None:
        # A feed we have never reached must not look healthy forever.
        waiting = int((datetime.now(UTC) - calendar_data.started_at).total_seconds())
        if waiting > grace:
            return jsonify(status="stale", age_seconds=None, days=0), 503
        return jsonify(status="starting", age_seconds=None, days=0), 200

    age = int((datetime.now(UTC) - calendar_data.last_success).total_seconds())
    stale = age > grace
    payload = jsonify(
        status="stale" if stale else "ok",
        age_seconds=age,
        days=len(calendar_data.data),
    )
    return payload, 503 if stale else 200


if __name__ == "__main__":
    start_updater()
    app.run(host="0.0.0.0", port=5000)
