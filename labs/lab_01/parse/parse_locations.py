import csv
import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup

src = 'https://vedmak.fandom.com'


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


def append_one_elem(quest, id, ids, names, types, places, quest_ids, squares):
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
    squares.append(random.random() * 2500)
    if not type_flag:
        types.append('Хитроумная конструкция')
    if not place_flag:
        places.append('Неизвестно')
    if not quest_id_flag:
        quest_ids.append('')


quests_list = []

with open('locations_links.txt') as f:
    quest_links = f.readlines()

for i in range(len(quest_links)):
    quest_links[i] = quest_links[i][:-1]

for quest_link in quest_links:
    response = requests.get(quest_link)
    soup = BeautifulSoup(response.text, 'lxml')
    quests = soup.find_all('a', class_='category-page__member-link', href=True)
    for quest in quests:
        quests_list.append(quest)

ids = ['location_id']
names = ['location_name']
types = ['location_type']
places = ['location_place']
quest_ids = ['quest_id']
squares = ['location_square']

id = 1
for quest in quests_list:
    append_one_elem(quest, id, ids, names, types, places, quest_ids, squares)
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

# добавление случайных значений
extra_n = 300
for i in range(extra_n):
    quest = quests_list[random.randint(1, extra_n % len(quests_list))]
    append_one_elem(quest, id, ids, names, types, places, quest_ids, squares)
    id += 1
    print('EXTRA ' + str(id) + '/' + str(extra_n + len(quests_list)) + '\r', end='')


ids_connection = ['locations_quests_id']
locations_ids_connection = ['location_id']
quests_ids_connection = ['quest_id']

j = 0
for i in range(1, len(ids)):
    if quest_ids[i] != '':
        j += 1
        ids_connection.append(j)
        locations_ids_connection.append(ids[i])
        quests_ids_connection.append(quest_ids[i])

np.savetxt('locations.csv', [p for p in zip(ids, names, types, places, squares)], delimiter=',', fmt='%s')

np.savetxt('locations_quests.csv', [p for p in zip(ids_connection, locations_ids_connection, quests_ids_connection)], delimiter=',', fmt='%s')
