import csv
import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup

src = 'https://vedmak.fandom.com'

dictionary = {'Предательство': ['Комикс', 1230],
              'Ведьмак:Проклятиеворонов': ['Книга', 1230],
              'ВладычицаОзера': ['Книга', 1260],
              'Крайсвета': ['Книга', 1250],
              'КровьиВино': ['Игра', 1275],
              'Маг-Отступник': ['Книга', 1244],
              'Пределвозможного': ['Книга', 1248],
              'Книги:Башняласточки': ['Книга', 1259],
              'Осколокльда': ['Книга', 1252],
              'Когтииклыки': ['Книга', 1233],
              'Крещениеогнем': ['Книга', 1246],
              'Книги:Последнеежелание': ['Книга', 1253],
              'Что-токончается': ['Книга', 1253],
              'Каменныесердца': ['Игра', 1273],
              'Немногожертвенности': ['Книга', 1256],
              'Крупицаистины': ['Книга', 1249],
              'Гвинт:ВедьмакКарточнаяИгра': ['Игра', 1278],
              'Книги:Часпрезрения': ['Книга', 1257],
              'Угрызениясовести': ['Книга', 1244],
              'Ведьмак:Домвитражей': ['Книга', 1233],
              'Ведьмак:Благонарода': ['Книга', 1235],
              'Книги:МечПредназначения': ['Книга', 1254],
              'Генеалогии': ['Картинка', 1254],
              'КровьЭльфов': ['Книга', 1255],
              'Сезонгроз': ['Книга', 1266],
              'СезонГроз': ['Книга', 1266],
              'Гласрассудка': ['Книга', 1244],
              'Вечныйогонь': ['Книга', 1247],
              'Охотникначудовищ': ['Книга', 1243],
              'Книги:ВопросценыИгры:Ведьмак': ['Книга', 1244],
              'TheWitcherAdventureGame': ['Игра', 1262],
              'Ведьмак:ИграВоображения': ['Книга', 1266],
              'Меньшеезло': ['Книга', 1264],
              'БоеваяАрена': ['Книга', 1266],
              'Ведьмак:Убиваячудовищ': ['Книга', 1263],
              'Лисьидети': ['Книга', 1244],
              'Нечтобольшее': ['Книга', 1256],
              'Ведьмак:Изплотиипламени': ['Книга', 1255],
              'Дорогабезвозврата': ['Книга', 1259],
              'Ведьмак:Проклятьеворонов': ['Книга', 1244],
              'Ведьмак:НастольнаяРолеваяИгра': ['Игра', 1272],
              'Ведьмак3:ДикаяОхота': ['Игра', 1272],
              'Ведьмак2:УбийцаКоролей' : ['Игра', 1270]
              }


def get_type_and_name_by_s(s):
    for key in dictionary:
        if s in key:
            return dictionary[key]
    return 'Книга', 1230

def remove_quotes_and_spaces(s):
    s = s.replace("«", '')
    s = s.replace(",", '')
    s = s.replace(";", '')
    s = s.replace("»", '')
    s = s.replace("\"", '')
    s = s.replace(" ", '')
    return s


def get_location_id_by_name(name):
    results = []
    with open('locations.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)

    for el in results:
        if name in el['location_name']:
            return el['location_id']

def truncate_by_quotes(s):
    for i in range(len(s)):
        if i != 0 and s[i] == '«' and s[i - 1] == '»':
            return s[:i]
        elif i != 0 and s[i].isupper() and s[i - 1] != ' ' and s[i - 1].islower():
            return s[:i]
        elif s[i] == ',' or s[i] == ';':
            return s[:i]
    return s


def append_one_elem(quest, id, ids, years, types, names, locations, replicas_numbers):
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

    name = soup_list[3][:soup_list[3].find('|') - 1]
    if 'Участник' in name or 'Категория' in name:
        return None

    # print(soup_list)

    soup_list[3] = soup_list[3].replace(',', '')

    ids.append(id)

    appearance_flag, location_flag = False, False
    for j in range(len(soup_list) - 1):
        soup_list[j + 1] = soup_list[j + 1].replace(',', '')
        soup_list[j + 1] = soup_list[j + 1].replace(';', '')

        if soup_list[j] == 'Появления' and not appearance_flag:
            appearance_flag = True
            name = truncate_by_quotes(soup_list[j + 3])
            names.append(name)
            params = get_type_and_name_by_s(remove_quotes_and_spaces(name[:10]))
            types.append(params[0])
            years.append(params[1])
        if soup_list[j] == 'Локация' and not location_flag:
            location_flag = True
            location = get_location_id_by_name(soup_list[j + 1][:5])
            if location is None:
                location_flag = False
                continue
            locations.append(location)
    replicas_numbers.append(random.randint(0, 300))
    if not appearance_flag:
        names.append('')
        types.append('')
        years.append('')
    if not location_flag:
        locations.append('')

    return True


quests_list = []
with open('characters_links.txt') as f:
    quest_links = f.readlines()

for i in range(len(quest_links)):
    quest_links[i] = quest_links[i][:-1]

for quest_link in quest_links:
    response = requests.get(quest_link)
    soup = BeautifulSoup(response.text, 'lxml')
    quests = soup.find_all('a', class_='category-page__member-link', href=True)
    for quest in quests:
        quests_list.append(quest)

ids = ['appearance_id']
years = ['appearance_year']
types = ['appearance_type']
names = ['appearance_name']
locations = ['location_id']
replicas_numbers = ['appearance_replicas_number']

id = 1

for quest in quests_list:

    if append_one_elem(quest, id, ids, years, types, names, locations, replicas_numbers) is None:
        id -= 1
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

ids_connection = ['appearances_locations_id']
appearances_ids_connection = ['appearance_id']
locations_ids_connection = ['location_id']

j = 0
for i in range(1, len(ids)):
    if locations[i] != '':
        j += 1
        ids_connection.append(j)
        appearances_ids_connection.append(ids[i])
        locations_ids_connection.append(locations[i])

np.savetxt('appearances.csv', [p for p in zip(ids, years, types, names, replicas_numbers)], delimiter=',', fmt='%s')

np.savetxt('appearances_locations.csv', [p for p in zip(ids_connection, appearances_ids_connection, locations_ids_connection)], delimiter=',', fmt='%s')
