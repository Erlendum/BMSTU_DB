import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup

src = 'https://vedmak.fandom.com'


def append_one_elem(quest, id, ids, names, types, issuings, rewards):
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

    type_flag, issuing_flag, reward_flag = False, False, False
    for j in range(len(soup_list) - 1):
        soup_list[j + 1] = soup_list[j + 1].replace(',', '')
        soup_list[j + 1] = soup_list[j + 1].replace(';', '')
        if soup_list[j] == 'Тип':
            type_flag = True
            if 'Основной' in soup_list[j + 1]:
                types.append('Основной')
            else:
                types.append('Второстепенный')
        elif soup_list[j] == 'Выдаётся':
            issuing_flag = True
            issuings.append(soup_list[j + 1])
        elif soup_list[j] == 'Награда':
            reward_flag = True
            rewards.append(soup_list[j + 1])
            break

    if not type_flag:
        types.append('Второстепенный')
    if not issuing_flag:
        issuings.append('Доска объявлений')
    if not reward_flag:
        rewards.append('')


quests_list = []

with open('quests_links.txt') as f:
    quest_links = f.readlines()

for i in range(len(quest_links)):
    quest_links[i] = quest_links[i][:-1]

for quest_link in quest_links:
    response = requests.get(quest_link)
    soup = BeautifulSoup(response.text, 'lxml')
    quests = soup.find_all('a', class_='category-page__member-link', href=True)
    for quest in quests:
        quests_list.append(quest)

ids = ['quest_id']
names = ['quest_name']
types = ['quest_type']
issuings = ['quest_issuing']
rewards = ['quest_reward']

id = 1
for quest in quests_list:
    append_one_elem(quest, id, ids, names, types, issuings, rewards)
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

# добавление случайных значений
extra_n = 400
for i in range(extra_n):
    quest = quests_list[random.randint(1, extra_n % len(quests_list))]
    append_one_elem(quest, id, ids, names, types, issuings, rewards)
    id += 1
    print('EXTRA ' + str(id) + '/' + str(extra_n + len(quests_list)) + '\r', end='')

np.savetxt('quests.csv', [p for p in zip(ids, names, types, issuings, rewards)], delimiter=',', fmt='%s')
