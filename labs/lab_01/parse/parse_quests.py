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

# src = 'https://vedmak.fandom.com'
# url1 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B2%D0%B5%D1%81%D1%82%D1%8B"
# response1 = requests.get(url1)
# soup1 = BeautifulSoup(response1.text, 'lxml')
#
# url2 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B2%D0%B5%D1%81%D1%82%D1%8B?from=%D0%97%D0%B0%D0%BA%D0%B0%D0%B7%3A+%D0%9B%D0%B5%D1%88%D0%B0%D1%87%D0%B8%D1%85%D0%B0"
# response2 = requests.get(url2)
# soup2 = BeautifulSoup(response2.text, 'lxml')
#
# url3 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B2%D0%B5%D1%81%D1%82%D1%8B?from=%D0%9D%D0%B0%D1%88%D0%BB%D0%B8%2C+%D0%B0+%D0%BD%D0%B5+%D1%83%D0%BA%D1%80%D0%B0%D0%BB%D0%B8"
# response3 = requests.get(url3)
# soup3 = BeautifulSoup(response3.text, 'lxml')
#
# url4 = src + "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B2%D0%B5%D1%81%D1%82%D1%8B?from=%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA+%D0%B1%D0%BB%D1%83%D0%B4%D0%BD%D0%B8%D1%86"
# response4 = requests.get(url4)
# soup4 = BeautifulSoup(response4.text, 'lxml')
#
# quests1 = soup1.find_all('a', class_='category-page__member-link', href=True)
# quests2 = soup2.find_all('a', class_='category-page__member-link', href=True)
# quests3 = soup3.find_all('a', class_='category-page__member-link', href=True)
# quests4 = soup4.find_all('a', class_='category-page__member-link', href=True)

quest_links = []

with open('quests_links.txt') as f:
    quest_links = f.readlines()


for i in range(len(quest_links)):
    quest_links[i] = quest_links[i][:-1]

print(quest_links)

exit()
quests_list = []
for quest in quests1:
    quests_list.append(quest)

for quest in quests2:
    quests_list.append(quest)

for quest in quests3:
    quests_list.append(quest)

for quest in quests4:
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
