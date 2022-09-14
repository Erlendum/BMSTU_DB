import time

import requests
import numpy as np
from bs4 import BeautifulSoup


def append_one_elem(quest, id, ids, names, capitals, statuses, currencies, polities, leaders):
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

    capital_flag, status_flag, currency_flag, polity_flag, leader_flag = False, False, False, False, False
    for j in range(len(soup_list) - 1):
        soup_list[j + 1] = soup_list[j + 1].replace(',', '')
        soup_list[j + 1] = soup_list[j + 1].replace(';', '')
        if soup_list[j] == 'Столица':
            type_flag = True
            capitals.append(soup_list[j + 1])
        elif soup_list[j] == 'Статус':
            status_flag = True
            statuses.append(soup_list[j + 1])
        elif soup_list[j] == 'Валюта' or soup_list[j] == 'Денежная единица':
            currency_flag = True
            currencies.append(soup_list[j + 1])
        elif soup_list[j] == 'Форма правления':
            polity_flag = True
            polities.append(soup_list[j + 1])
        elif soup_list[j] == 'Правитель':
            leader_flag = True
            leaders.append(soup_list[j + 1])

    if not capital_flag:
        capitals.append('')
    if not status_flag:
        statuses.append('')
    if not currency_flag:
        currencies.append('')
    if not leader_flag:
        leaders.append('')
    if not polity_flag:
        polities.append('')


src = 'https://vedmak.fandom.com'
url1 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B0"
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text, 'lxml')

quests1 = soup1.find_all('a', class_='category-page__member-link', href=True)

quests_list = []
for quest in quests1:
    quests_list.append(quest)

ids = ['country_id']
names = ['country_name']
capitals = ['country_capital']
statuses = ['country_status']
currencies = ['country_currency']
polities = ['country_polity']
leaders = ['country_leaders']

id = 1
for quest in quests_list:
    append_one_elem(quest, id, ids, names, capitals, statuses, currencies, polities, leaders)
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

np.savetxt('countries.csv', [p for p in zip(ids, names, capitals, statuses, currencies, polities, leaders)], delimiter=',', fmt='%s')
