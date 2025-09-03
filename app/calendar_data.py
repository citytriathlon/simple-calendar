import asyncio
import aiohttp
import os
import logging
from ics import Calendar, Event
from datetime import datetime, timedelta, timezone
import pytz
import re
from typing import Optional, Dict, List, Any


class CalendarData:
    def __init__(self, update_interval: int = 30) -> None:
        self.data = {}
        self.update_interval = update_interval
        self.url = os.environ.get("ICS_URL")
        self.timezone = os.environ.get("TIMEZONE","Europe/Prague")
        self.local_tz = pytz.timezone(self.timezone)
        if not self.url:
            logging.error("ICS_URL environment variable not set.")

    async def update_data(self) -> None:
        while True:
            if self.url:
                try:
                    new_data = await self.fetch_calendar_data()
                    self.data = new_data
                except aiohttp.ClientError as e:
                    logging.error(f"Error fetching calendar data: {e}")
                except Exception as e:
                    logging.error(f"An unexpected error occurred: {e}")
            await asyncio.sleep(self.update_interval)

    async def fetch_calendar_data(self) -> Dict[str, List[Dict[str, Any]]]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                text = await response.text()
                calendar = Calendar(text)

        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        output = {}

        for event in calendar.timeline:
            event_date = event.begin.datetime.astimezone(self.local_tz)
            if event_date > one_day_ago:
                date_str = event_date.strftime("%d. %m. %Y")
                entry_dict = self.process_event(event)
                output.setdefault(date_str, []).append(entry_dict)
        return output

    def process_event(self, event: Event) -> Dict[str, Any]:
        event_begin = event.begin.astimezone(self.local_tz)
        event_end = event.end.astimezone(self.local_tz)
        day = event_begin.day
        random_hue = day * 10 if (day % 2) == 0 else 360 - (day * 10)
        organizer = self.extract_organizer(event.organizer, event.description)
        end_epoch = int(event_end.timestamp()) * 1000
        begin_epoch = int(event_begin.timestamp()) * 1000

        search_day = event_begin.strftime("%d. %m. %Y")

        entry_dict = {
            "begin": event_begin.strftime("%H:%M") or "",
            "end": event_end.strftime("%H:%M") or "",
            "name": event.name or "",
            "description": event.description or "",
            "location": event.location or "",
            "hue": random_hue,
            "organizer": organizer,
            "end_epoch": end_epoch,
            "begin_epoch": begin_epoch,
        }

        all_strings = [
            str(entry_dict["name"]),
            str(entry_dict["location"]),
            str(organizer),
            str(entry_dict["begin"]),
            str(entry_dict["end"]),
            str(entry_dict["description"]),
        ]
        entry_dict["all_strings"] = " ".join(all_strings)
        entry_dict["all_strings_date"] = f'{entry_dict["all_strings"]} {search_day}'

        return entry_dict

    @staticmethod
    def extract_organizer(organizer: Optional[str], description: Optional[str]) -> str:
        names = CalendarData.get_names(description or "")
        if names:
            return ", ".join(names)

        if "@citytriathlon.cz" in str(organizer).split(":")[-1]:
            email = str(organizer).split(":")[-1]
            name = " ".join(email.split("@")[0].split("."))
            return CalendarData.name_mod(name)
        
        if organizer:
            return str(organizer).split(":")[-1]

        return "Unknown Organizer"

    @staticmethod
    def get_names(description: str) -> List[str]:
        if not description:
            return []
        pattern = r"(?<!\w)@(\w+)"
        matches = re.findall(pattern, description, re.MULTILINE)
        return [match.capitalize() for match in matches]

    @staticmethod
    def name_mod(name_in: str) -> str:
        parts = name_in.split(" ")
        if not parts:
            return ""
        first_name = parts[0].capitalize()
        last_initials = [f"{p[0].upper()}." for p in parts[1:] if p]
        return " ".join([first_name] + last_initials)

    def get_recent_events(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.data.copy()
