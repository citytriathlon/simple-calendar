from ics import Calendar
import requests

def camel_string(string):
    string = string.capitalize()
    return string

def get_names(description):
    names = []
    for i in description.split(" "):
        if i.startswith("@"):
           name = i.lstrip("@")
           names.append(name)
    return names

def name_mod(name_in):
    name_out_list = []
    for i in name_in.split(" "):
        name_out_list.append(i.capitalize())
    name_out = " ".join(name_out_list)
    return name_out

def get_next_item():
    url = "https://calendar.google.com/calendar/ical/c_6lojl9vcji7jf4i5epk10b70f0%40group.calendar.google.com/private-5f248df38c67864be13c6704c932a764/basic.ics"
    c = Calendar(requests.get(url).text)
    output = {}
    for i in range(len(list(c.timeline))):
        e = list(c.timeline)[i]
        output[i] = {}
        output[i]["begin"] = e.begin.format('DD-MM-YYYY')
        output[i]["begin"] = e.begin.format('HH:mm')
        output[i]["end"] = e.end.format('HH:mm')
        output[i]["name"] = e.name
        output[i]["description"] = e.description
        output[i]["location"] = e.location
        names = get_names(e.description)
        if names:
            output[i]["organizer"] = ", ".join(names)
        elif "@citytriathlon.cz" in str(e.organizer).split(':')[-1]:
            email = str(e.organizer).split(':')[-1]
            name = " ".join(email.split('@')[0].split('.'))
            output[i]["organizer"] = name_mod(name)
        else:
            output[i]["organizer"] = str(e.organizer).split(':')[-1]
  
    return output

# get_next_item()