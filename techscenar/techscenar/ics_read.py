from ics import Calendar
import requests

def camel_string(string):
    string = string.capitalize()
    return string

def get_names(description):
    names = []
    for i in description.split():
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
        date = e.begin.format('DD. MM. YYYY')
        day = int(e.begin.format('DD'))
        if (day % 2) == 0:
            random_hue = day * 10
        else:
            random_hue = 360 - (day * 10)
        if date not in output:
            output[date] = []
        entry_dict = {}
        if e.begin.format('HH:mm') == "00:00" and e.end.format('00:00'):
            entry_dict["timerange"] = "Celý den"
        else:
            entry_dict["timerange"] = f'{e.begin.format("HH:mm")} - {e.end.format("HH:mm")}'
        # entry_dict["begin"] = e.begin.format('HH:mm')
        # entry_dict["end"] = e.end.format('HH:mm')
        # entry_dict["timerange"] = e.end.format('HH:mm')
        entry_dict["name"] = e.name
        entry_dict["description"] = e.description
        entry_dict["location"] = e.location
        entry_dict["hue"] = random_hue
        names = get_names(e.description)
        if names:
            entry_dict["organizer"] = ", ".join(names)
        elif "@citytriathlon.cz" in str(e.organizer).split(':')[-1]:
            email = str(e.organizer).split(':')[-1]
            name = " ".join(email.split('@')[0].split('.'))
            entry_dict["organizer"] = name_mod(name)
        else:
            entry_dict["organizer"] = str(e.organizer).split(':')[-1]
        all_strings = [e.name,e.description,e.location,entry_dict["organizer"],entry_dict["timerange"],date]
        entry_dict["all_strings"] = " ".join(all_strings)
        output[date].append(entry_dict)
        if "all_strings_date" in output[date][0]:
            output[date][0]["all_strings_date"] = f'{output[date][0]["all_strings_date"]} {entry_dict["all_strings"]}'
        else:
            output[date][0]["all_strings_date"] = entry_dict["all_strings"]
  
    return output

# output = get_next_item()
# print(output)
