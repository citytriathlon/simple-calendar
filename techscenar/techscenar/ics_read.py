from ics import Calendar
import requests

def get_next_item():
    url = "https://calendar.google.com/calendar/ical/c_6lojl9vcji7jf4i5epk10b70f0%40group.calendar.google.com/private-5f248df38c67864be13c6704c932a764/basic.ics"
    c = Calendar(requests.get(url).text)
    output = {}
    for i in range(len(list(c.timeline))):
        e = list(c.timeline)[i]
        output[i] = {}
        output[i]["name"] = e.name
        output[i]["description"] = e.description
        output[i]["location"] = e.location
        output[i]["organizer"] = str(e.organizer).split(':')[-1]
  
    return output

# get_next_item()