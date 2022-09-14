import csv
import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup


def truncate_by_upper_letter(s):
    for i in range(len(s)):
        if s[i].isupper() and s[i - 1] != ' ' and s[i - 1].islower() and i != 0:
            return s[:i]
    return s


def get_id_by_name(name):
    results = []
    with open('quests.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)

    for el in results:
        if name in el['quest_name']:
            return el['quest_id']


def append_one_elem(quest, id, ids, names, types, places, quest_ids):
    url = src + quest['href']

    response = ''
    while response == '':
        try:
            response = requests.get(url)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    soup = BeautifulSoup(response.text, 'lxml')

    soup_list = soup.text.split('\n')

    ids.append(id)

    soup_list[3] = soup_list[3].replace(',', '')
    name = soup_list[3][:soup_list[3].find('|') - 1]
    if name in names:
        name += ' (строение {:d})'.format(names.count(name) + 1)
    names.append(name)

    type_flag, place_flag, quest_id_flag = False, False, False
    for j in range(len(soup_list) - 1):
        soup_list[j + 1] = soup_list[j + 1].replace(',', '')
        soup_list[j + 1] = soup_list[j + 1].replace(';', '')
        if soup_list[j] == 'Тип':
            type_flag = True
            types.append(soup_list[j + 1])
        elif soup_list[j] == 'Расположение':
            place_flag = True
            places.append(soup_list[j + 1])
        elif soup_list[j] == 'Квесты' and soup_list[j + 1] != ' ' and soup_list[j + 1] != '':
            quest_id_flag = True
            soup_list[j + 1] = truncate_by_upper_letter(soup_list[j + 1])

            quest_id = get_id_by_name(soup_list[j + 1])
            quest_id_flag = quest_id is not None
            if not quest_id_flag:
                continue
            quest_ids.append(get_id_by_name(soup_list[j + 1]))

    if not type_flag:
        types.append('Хитроумная конструкция')
    if not place_flag:
        places.append('Неизвестно')
    if not quest_id_flag:
        quest_ids.append('')


src = 'https://vedmak.fandom.com'
url1 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9B%D0%BE%D0%BA%D0%B0%D1%86%D0%B8%D0%B8"
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text, 'lxml')

url2 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9B%D0%BE%D0%BA%D0%B0%D1%86%D0%B8%D0%B8?from=%D0%94%D1%80%D0%B5%D0%B2%D0%BD%D1%8F%D1%8F+%D0%B3%D1%80%D0%BE%D0%B1%D0%BD%D0%B8%D1%86%D0%B0+%28%D0%92%D0%B5%D0%B4%D1%8C%D0%BC%D0%B0%D0%BA+3%29"
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, 'lxml')

url3 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9B%D0%BE%D0%BA%D0%B0%D1%86%D0%B8%D0%B8?from=%D0%9D%D0%B5%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BD%D0%B0%D1%8F+%D0%BF%D0%BE%D0%BB%D1%8F%D0%BD%D0%B0"
response3 = requests.get(url3)
soup3 = BeautifulSoup(response3.text, 'lxml')

url4 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9B%D0%BE%D0%BA%D0%B0%D1%86%D0%B8%D0%B8?from=%D0%A1%D0%BE%D0%B6%D0%B6%D1%91%D0%BD%D0%BD%D0%B0%D1%8F+%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BD%D1%8F+%28%D0%91%D0%B5%D0%BB%D1%8B%D0%B9+%D0%A1%D0%B0%D0%B4%29"
response4 = requests.get(url4)
soup4 = BeautifulSoup(response4.text, 'lxml')

# print(soup)
# print(soup.text.split('\n'))

quests1 = soup1.find_all('a', class_='category-page__member-link', href=True)
quests2 = soup2.find_all('a', class_='category-page__member-link', href=True)
quests3 = soup3.find_all('a', class_='category-page__member-link', href=True)
quests4 = soup4.find_all('a', class_='category-page__member-link', href=True)

quests_list = []
for quest in quests1:
    quests_list.append(quest)

for quest in quests2:
    quests_list.append(quest)

for quest in quests3:
    quests_list.append(quest)

for quest in quests4:
    quests_list.append(quest)

ids = ['location_id']
names = ['location_name']
types = ['location_type']
places = ['location_place']
quest_ids = ['quest_id']

id = 1
for quest in quests_list:
    append_one_elem(quest, id, ids, names, types, places, quest_ids)
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

# добавление случайных значений
extra_n = 300
for i in range(extra_n):
    quest = quests_list[random.randint(1, extra_n % len(quests_list))]
    append_one_elem(quest, id, ids, names, types, places, quest_ids)
    id += 1
    print('EXTRA ' + str(id) + '/' + str(extra_n + len(quests_list)) + '\r', end='')


np.savetxt('locations.csv', [p for p in zip(ids, names, types, places, quest_ids)], delimiter=',', fmt='%s')
