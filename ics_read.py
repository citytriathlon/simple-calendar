from ics import Calendar
import requests

url = "https://calendar.google.com/calendar/ical/c_nou5qhv9n5vjsv4a63gctnjm6o%40group.calendar.google.com/private-16ca0c7762eeacb1f056cecb5640f29d/basic.ics"
c = Calendar(requests.get(url).text)
# print(list(c.timeline)

# c
# print(c.events)
# print(len(list(c.timeline)))

for i in range(len(list(c.timeline))):
    # print(list(c.timeline)[i])
    e = list(c.timeline)[i]
    # print(e.attendees)
    print(e.name)
    print(e.description)
    print(e.location)

    print(str(e.organizer).split(':')[-1])
    # print(e.creator)
    print('\n\n')