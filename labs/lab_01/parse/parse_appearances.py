import csv
import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup

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


def append_one_elem(quest, id, ids, years, types, names, locations):
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

    if not appearance_flag:
        names.append('')
        types.append('')
        years.append('')
    if not location_flag:
        locations.append('')

    return True


src = 'https://vedmak.fandom.com'
url1 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8"
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text, 'lxml')

url2 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%91%D0%B0%D1%80%D1%82"
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, 'lxml')

url3 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%92%D0%B8%D0%BB%D1%8C%D0%B1%D1%83%D1%80+%D0%B0%D1%8D%D0%BF+%D0%9C%D0%B8%D0%BB%D0%BB%D0%B8%D1%81+%D0%AD%D0%BF%D1%81%D0%B8%D0%B2%D0%B0%D1%80"
response3 = requests.get(url3)
soup3 = BeautifulSoup(response3.text, 'lxml')

url4 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%93%D1%80%D0%B5%D1%82%D0%B0+%D0%9E%D0%B1%D0%B5%D1%80%D1%82"
response4 = requests.get(url4)
soup4 = BeautifulSoup(response4.text, 'lxml')

url5 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%97%D0%B5%D0%BB%D0%B8"
response5 = requests.get(url5)
soup5 = BeautifulSoup(response5.text, 'lxml')

url6 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%9A%D0%B8%D1%81%D1%82%D1%80%D0%B8%D0%BD"
response6 = requests.get(url6)
soup6 = BeautifulSoup(response6.text, 'lxml')

url7 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%9B%D1%8E%D1%81%D1%8C%D0%B5%D0%BD+%D0%9C%D0%BE%D0%BD%D0%BD%D0%B0%D1%80"
response7 = requests.get(url7)
soup7 = BeautifulSoup(response7.text, 'lxml')

url8 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%9D%D0%B0%D1%80%D0%B0%D0%B4%D0%BA%D0%BE%D0%B2%D0%B0"
response8 = requests.get(url8)
soup8 = BeautifulSoup(response8.text, 'lxml')

url9 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%9F%D1%80%D0%B8%D0%B7%D1%80%D0%B0%D0%BA+%D0%B8%D0%B3%D1%80%D0%BE%D0%BA%D0%B0"
response9 = requests.get(url9)
soup9 = BeautifulSoup(response9.text, 'lxml')

url10 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%A1%D0%B8%D0%BD%D0%B3%D0%B0"
response10 = requests.get(url10)
soup10 = BeautifulSoup(response10.text, 'lxml')

url11 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%A4%D0%B5%D0%B4%D0%BE%D1%80%D0%B0+%D0%9A%D1%80%D0%B0%D0%BD%D0%BD"
response11 = requests.get(url11)
soup11 = BeautifulSoup(response11.text, 'lxml')

url12 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%AD%D0%B3%D0%BE%D0%BD"
response12 = requests.get(url12)
soup12 = BeautifulSoup(response12.text, 'lxml')

# print(soup)
# print(soup.text.split('\n'))

quests1 = soup1.find_all('a', class_='category-page__member-link', href=True)
quests2 = soup2.find_all('a', class_='category-page__member-link', href=True)
quests3 = soup3.find_all('a', class_='category-page__member-link', href=True)
quests4 = soup4.find_all('a', class_='category-page__member-link', href=True)
quests5 = soup5.find_all('a', class_='category-page__member-link', href=True)
quests6 = soup6.find_all('a', class_='category-page__member-link', href=True)
quests7 = soup7.find_all('a', class_='category-page__member-link', href=True)
quests8 = soup8.find_all('a', class_='category-page__member-link', href=True)
quests9 = soup9.find_all('a', class_='category-page__member-link', href=True)
quests10 = soup10.find_all('a', class_='category-page__member-link', href=True)
quests11 = soup11.find_all('a', class_='category-page__member-link', href=True)
quests12 = soup12.find_all('a', class_='category-page__member-link', href=True)

quests_list = []
for quest in quests1:
    quests_list.append(quest)

for quest in quests2:
    quests_list.append(quest)

for quest in quests3:
    quests_list.append(quest)

for quest in quests4:
    quests_list.append(quest)

for quest in quests5:
    quests_list.append(quest)

for quest in quests6:
    quests_list.append(quest)

for quest in quests7:
    quests_list.append(quest)

for quest in quests8:
    quests_list.append(quest)

for quest in quests9:
    quests_list.append(quest)

for quest in quests10:
    quests_list.append(quest)

for quest in quests11:
    quests_list.append(quest)

for quest in quests12:
    quests_list.append(quest)

ids = ['appearance_id']
years = ['appearance_year']
types = ['appearance_type']
names = ['appearance_names']
locations = ['location_id']

id = 1

for quest in quests_list:

    if append_one_elem(quest, id, ids, years, types, names, locations) is None:
        id -= 1
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

np.savetxt('appearances.csv', [p for p in zip(ids, years, types, names, locations)], delimiter=',', fmt='%s')
