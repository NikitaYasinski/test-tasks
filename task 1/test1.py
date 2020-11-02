import requests
from bs4 import BeautifulSoup
import json

response = requests.get("https://www.mebelshara.ru/contacts")
soup = BeautifulSoup(response.text, 'lxml')

data = dict()
data_list = list()

info_list = soup.find_all("div", class_="shop-list-item")

address_list = list()
street_list = list()
latlon_list = list()
name_list = list()
phones_list = list()
working_hours_list = list()

for info in info_list:
    address_list.append(info.parent.parent.parent.parent.parent.parent.h4.text)
    street_list.append(info['data-shop-address'])
    latlon_list.append([info['data-shop-latitude'], info['data-shop-longitude']])
    name_list.append(info['data-shop-name'])
    phones_list.append([info['data-shop-phone']])
    days = info['data-shop-mode1']
    
    if days == 'Без выходных:' or days == 'Без выходных':
        days = 'пн - вс'
        working_hours_list.append([days + ' ' + info['data-shop-mode2']])
    else:
        working_hours_list.append([info['data-shop-mode1'], info['data-shop-mode2']])
        
for i in range(len(info_list)):
    data['address'] = address_list[i] + f', {street_list[i]}'
    data['latlon'] = latlon_list[i]
    data['name'] = name_list[i]
    data['phones'] = phones_list[i]
    data['working_hours'] = working_hours_list[i]
    
    data_list.append(data)
    data = {}

with open("data.json", "w", encoding = "utf-8") as write_file:
    json.dump(data_list, write_file, indent = 4,
               ensure_ascii = False)