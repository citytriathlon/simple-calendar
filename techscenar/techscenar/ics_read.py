from ics import Calendar
import requests
import re
import os


def get_names(description):
    names = re.findall(r'@(\w*)(?!\.)(?![a-z]{1,3})',description)
    return names


def name_mod(name_in):
    name_out_list = []
    z = 0
    for i in name_in.split(" "):
        if z == 0:
            name_out_list.append(i.capitalize())
            z += 1
        else:
            fam_name_short = f'{list(i)[0]}.'
            name_out_list.append(fam_name_short.capitalize())
    name_out = " ".join(name_out_list)
    return name_out

def get_next_item():
    url = os.environ['ICS_URL']
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
        entry_dict["begin"] = e.begin.to('local').format("HH:mm")
        entry_dict["end"] = e.end.to('local').format("HH:mm")
        end_epoch = e.end.to('local').int_timestamp
        entry_dict["end_epoch"] = int(end_epoch) * 1000
        begin_epoch = e.begin.to('local').int_timestamp
        entry_dict["begin_epoch"] = int(begin_epoch) * 1000
        entry_dict["name"] = e.name
        entry_dict["description"] = e.description
        entry_dict["location"] = e.location
        entry_dict["hue"] = random_hue
        names = get_names(e.description)
        if names:
            entry_dict["organizer"] = ", ".join([x.capitalize() for x in names])
        elif "@citytriathlon.cz" in str(e.organizer).split(':')[-1]:
            email = str(e.organizer).split(':')[-1]
            name = " ".join(email.split('@')[0].split('.'))
            entry_dict["organizer"] = name_mod(name)
        else:
            entry_dict["organizer"] = str(e.organizer).split(':')[-1]
        all_strings = [e.name,e.description,e.location,entry_dict["organizer"],entry_dict["begin"],entry_dict["end"],date]
        entry_dict["all_strings"] = " ".join(all_strings)
        output[date].append(entry_dict)
        if "all_strings_date" in output[date][0]:
            output[date][0]["all_strings_date"] = f'{output[date][0]["all_strings_date"]} {entry_dict["all_strings"]}'
        else:
            output[date][0]["all_strings_date"] = entry_dict["all_strings"]
  
    return output
