import asyncio
import logging
import os
import re
from datetime import UTC, date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import aiohttp
from ics import Calendar, Event

logger = logging.getLogger(__name__)

DATE_FORMAT = "%d. %m. %Y"
DEFAULT_TIMEZONE = "Europe/Prague"


class CalendarData:
    def __init__(self, update_interval: int | None = None) -> None:
        self.data: dict[str, list[dict[str, Any]]] = {}
        self.update_interval = update_interval or int(os.environ.get("UPDATE_INTERVAL", "60"))
        self.url = os.environ.get("ICS_URL")
        # Domain whose organizer addresses get shortened to "First L.".
        self.organizer_domain = os.environ.get("ORGANIZER_DOMAIN", "")
        self.request_timeout = int(os.environ.get("FETCH_TIMEOUT", "30"))
        self.started_at = datetime.now(UTC)
        self.last_success: datetime | None = None
        self.timezone = os.environ.get("TIMEZONE", DEFAULT_TIMEZONE)
        self.local_tz = self.load_timezone(self.timezone)

    @staticmethod
    def load_timezone(name: str) -> ZoneInfo:
        """Resolve a tz name, falling back rather than crashing at import time."""
        try:
            return ZoneInfo(name)
        except (ZoneInfoNotFoundError, ValueError):
            logger.warning("Unknown TIMEZONE %r, falling back to %s", name, DEFAULT_TIMEZONE)
            return ZoneInfo(DEFAULT_TIMEZONE)

    async def update_data(self) -> None:
        while True:
            try:
                self.data = await self.fetch_calendar_data()
                self.last_success = datetime.now(UTC)
                logger.info("Calendar refreshed: %d day(s) of events", len(self.data))
            except Exception:
                # Keep serving the last good data rather than blanking the board.
                logger.exception("Failed to refresh calendar data from %s", self.url)
            await asyncio.sleep(self.update_interval)

    async def fetch_calendar_data(self) -> dict[str, list[dict[str, Any]]]:
        if not self.url:
            raise RuntimeError("ICS_URL is not set")

        timeout = aiohttp.ClientTimeout(total=self.request_timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(self.url) as response:
                response.raise_for_status()
                text = await response.text()

        # Parsing is CPU-bound; do it after the connection is released.
        return self.build_events(text, datetime.now(UTC))

    def build_events(self, ics_text: str, now: datetime) -> dict[str, list[dict[str, Any]]]:
        cutoff = now - timedelta(days=1)
        output: dict[str, list[dict[str, Any]]] = {}

        for event in Calendar(ics_text).timeline:
            # Filter on the end so multi-day events still in progress survive.
            if event.end.datetime <= cutoff:
                continue
            day_key, entry = self.process_event(event)
            output.setdefault(day_key, []).append(entry)

        return output

    def process_event(self, event: Event) -> tuple[str, dict[str, Any]]:
        all_day = bool(getattr(event, "all_day", False))
        begin = event.begin.astimezone(self.local_tz)
        end = event.end.astimezone(self.local_tz)

        # All-day events carry no meaningful time, and converting them across
        # zones can push them onto the wrong calendar day.
        key_date: date = event.begin.date() if all_day else begin.date()
        day_key = key_date.strftime(DATE_FORMAT)

        hue = key_date.day * 10 if key_date.day % 2 == 0 else 360 - key_date.day * 10
        organizer = self.extract_organizer(event.organizer, event.description)

        entry: dict[str, Any] = {
            "begin": "" if all_day else begin.strftime("%H:%M"),
            "end": "" if all_day else end.strftime("%H:%M"),
            "all_day": all_day,
            "name": event.name or "",
            "description": event.description or "",
            "location": event.location or "",
            "hue": hue,
            "organizer": organizer,
            "begin_epoch": int(begin.timestamp() * 1000),
            "end_epoch": int(end.timestamp() * 1000),
        }

        all_strings = " ".join(
            str(entry[k]) for k in ("name", "location", "organizer", "begin", "end", "description")
        )
        entry["all_strings"] = all_strings
        entry["all_strings_date"] = f"{all_strings} {day_key}"

        return day_key, entry

    def extract_organizer(self, organizer: str | None, description: str | None) -> str:
        names = self.get_names(description or "")
        if names:
            return ", ".join(names)

        if not organizer:
            return "Unknown Organizer"

        address = str(organizer).split(":")[-1]
        if self.organizer_domain and self.organizer_domain in address:
            name = " ".join(address.split("@")[0].split("."))
            return self.name_mod(name)

        return address

    @staticmethod
    def get_names(description: str) -> list[str]:
        if not description:
            return []
        matches = re.findall(r"(?<!\w)@(\w+)", description, re.MULTILINE)
        return [match.capitalize() for match in matches]

    @staticmethod
    def name_mod(name_in: str) -> str:
        parts = [p for p in name_in.split(" ") if p]
        if not parts:
            return ""
        first_name = parts[0].capitalize()
        last_initials = [f"{p[0].upper()}." for p in parts[1:]]
        return " ".join([first_name] + last_initials)

    def get_recent_events(self) -> dict[str, list[dict[str, Any]]]:
        return self.data
