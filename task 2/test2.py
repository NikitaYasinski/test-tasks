import requests
import json

def get_work_days(working_hours):
    work = list()
    workdays = working_hours["workdays"]

    workdays_str = "пн-пт " + workdays["startStr"] + "-" + workdays["endStr"] 
    work.append(workdays_str)

    saturday = working_hours["saturday"]
    if saturday["isDayOff"] is False:
        saturday_str = "сб " + saturday["startStr"] + "-" + saturday["endStr"]
    else:
        saturday_str = "сб выходной"

    sunday = working_hours["sunday"]
    if sunday["isDayOff"] is False:
        sunday_str = "вс " + sunday["startStr"] + "-" + sunday["endStr"]
    else:
        sunday_str = "вс выходной"

    if saturday_str.split(" ")[1] == sunday_str.split(" ")[1]:
        weekend_str = ""
        if saturday_str.find("выходной") != -1:
            weekend_str = "сб-вс выходной"
        else:
            weekend_str = "сб-" + sunday_str
        work.append(weekend_str)
    else:
        work.append(saturday_str)
        work.append(sunday_str)
    
    return work

response = requests.get("https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false")
info = response.text

result_list = list()
office_dict = dict()

data = json.loads(info)
offices = data["offices"]

for office in offices:
    office_dict["address"] = office["address"]
    office_dict["latlon"] = [office["latitude"], office["longitude"]]
    office_dict["name"] = office["name"]
    office_dict["phones"] = office["phone"].split("; ")
    office_dict["working_hours"] = get_work_days(office["hoursOfOperation"])

    result_list.append(office_dict)
    office_dict = {}

with open("data.json", "w", encoding = "utf-8") as write_file:
    json.dump(result_list, write_file, indent = 4,
               ensure_ascii = False)

