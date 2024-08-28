# calendar_data.py
import asyncio
import aiohttp
import os
from ics import Calendar
from datetime import datetime, timedelta, timezone
import re


class CalendarData:
    def __init__(self, update_interval: int = 30) -> None:
        self.data = {}
        self.update_interval = update_interval
        self.url = os.environ.get("ICS_URL")

    async def start(self) -> None:
        await self.update_data()

    async def update_data(self) -> None:
        while True:
            new_data = await self.fetch_calendar_data()
            self.data = new_data
            await asyncio.sleep(self.update_interval)

    async def fetch_calendar_data(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                text = await response.text()
                calendar = Calendar(text)

        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        output = {}

        for event in calendar.timeline:
            event_date = event.begin.datetime
            if event_date > one_day_ago:
                date_str = event_date.astimezone(timezone.utc).strftime("%d. %m. %Y")
                entry_dict = self.process_event(event)
                output.setdefault(date_str, []).append(entry_dict)
        return output

    def process_event(self, event) -> dict:
        day = event.begin.day
        random_hue = day * 10 if (day % 2) == 0 else 360 - (day * 10)
        organizer = self.extract_organizer(event.organizer, event.description)
        end_epoch = int(event.end.timestamp()) * 1000
        begin_epoch = int(event.begin.timestamp()) * 1000

        search_day = event.begin.format("DD. MM. YYYY")

        entry_dict = {
            "begin": event.begin.astimezone(timezone.utc).strftime("HH:mm") or "",
            "end": event.end.astimezone(timezone.utc).strftime("HH:mm") or "",
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
    def extract_organizer(organizer, description: str) -> str:
        names = CalendarData.get_names(description)
        if names:
            return ", ".join(names)

        if "@citytriathlon.cz" in str(organizer).split(":")[-1]:
            email = str(organizer).split(":")[-1]
            name = " ".join(email.split("@")[0].split("."))
            return CalendarData.name_mod(name)
        else:
            return (
                str(organizer).split(":")[-1]
                if organizer
                else "Unknown Organizer"
            )

    @staticmethod
    def get_names(description: str) -> list:
        pattern = r"(?<!\w)@(\w+)"
        matches = re.findall(pattern, description, re.MULTILINE)
        return [match.capitalize() for match in matches]

    @staticmethod
    def name_mod(name_in: str) -> str:
        name_out_list = []
        z = 0
        for i in name_in.split(" "):
            if z == 0:
                name_out_list.append(i.capitalize())
                z += 1
            else:
                fam_name_short = f"{list(i)[0]}."
                name_out_list.append(fam_name_short.capitalize())
        return " ".join(name_out_list)

    def get_recent_events(self) -> dict:
        return self.data.copy()
