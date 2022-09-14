import time

import requests
import numpy as np
from bs4 import BeautifulSoup


def append_one_elem(quest, id, ids, names, types, symbols, gods, leaders):
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
        name += ' {:d}'.format(names.count(name) + 1)
    names.append(name)

    type_flag, symbol_flag, god_flag, leader_flag = False, False, False, False
    for j in range(len(soup_list) - 1):
        soup_list[j + 1] = soup_list[j + 1].replace(',', '')
        soup_list[j + 1] = soup_list[j + 1].replace(';', '')
        if soup_list[j] == 'Тип':
            type_flag = True
            types.append(soup_list[j + 1])
        elif soup_list[j] == 'Символы':
            symbol_flag = True
            symbols.append(soup_list[j + 1])
        elif soup_list[j] == 'Боги':
            god_flag = True
            gods.append(soup_list[j + 1])
        elif soup_list[j] == 'Лидеры':
            leader_flag = True
            leaders.append(soup_list[j + 1])

    if not type_flag:
        types.append('')
    if not symbol_flag:
        symbols.append('')
    if not god_flag:
        gods.append('')
    if not leader_flag:
        leaders.append('')


src = 'https://vedmak.fandom.com'
url1 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D0%B5%D0%BB%D0%B8%D0%B3%D0%B8%D1%8F"
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text, 'lxml')

quests1 = soup1.find_all('a', class_='category-page__member-link', href=True)

quests_list = []
for quest in quests1:
    quests_list.append(quest)

ids = ['religion_id']
names = ['religion_name']
types = ['religion_type']
symbols = ['religion_symbol']
gods = ['religion_gods']
leaders = ['religion_leaders']

id = 1
for quest in quests_list:
    append_one_elem(quest, id, ids, names, types, symbols, gods, leaders)
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

np.savetxt('religions.csv', [p for p in zip(ids, names, types, symbols, gods, leaders)], delimiter=',', fmt='%s')
