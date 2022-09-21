import csv
import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup

src = 'https://vedmak.fandom.com'

def get_country_id_by_name(name):
    results = []
    with open('countries.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)

    for el in results:
        if name in el['country_name']:
            return el['country_id']

def get_species_id_by_name(name):
    results = []
    with open('species.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)

    for el in results:
        if name in el['species_name']:
            return el['species_id']

def append_one_elem(quest, id, names, sexes, ages, occupations, lives, species, countries, appearances):
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

    soup_list[3] = soup_list[3].replace(',', '')
    name = soup_list[3][:soup_list[3].find('|') - 1]
    if 'Участник' in name or 'Категория' in name:
        return None

    names.append(name)
    appearances.append(id)

    sex_flag, occupation_flag, live_flag, species_flag, country_flag = False, False, False, False, False
    for j in range(len(soup_list) - 1):
        soup_list[j + 1] = soup_list[j + 1].replace(',', '')
        soup_list[j + 1] = soup_list[j + 1].replace(';', '')
        if soup_list[j] == 'Пол' and not sex_flag:
            sex_flag = True
            sexes.append(soup_list[j + 1])
        elif soup_list[j] == 'Род занятий' and not occupation_flag:
            occupation_flag = True
            occupations.append(soup_list[j + 1])
        elif soup_list[j] == 'Смерть' and not live_flag:
            live_flag = True
            lives.append(False)
        elif soup_list[j] == 'Раса' and not species_flag:
            species_flag = True
            specie = get_species_id_by_name(soup_list[j + 1][:4])
            if specie is None:
                species_flag = False
                continue
            species.append(specie)
        elif soup_list[j] == 'Народность' and not country_flag:
            country_flag = True
            country = get_country_id_by_name(soup_list[j+1][:4])
            if country is None:
                country_flag = False
                continue
            countries.append(country)

    ages.append(random.randint(15, 70))
    if not sex_flag:
        sexes.append('X')
    if not occupation_flag:
        occupations.append('')
    if not live_flag:
        lives.append(True)
    if not species_flag:
        species.append(8)
    if not country_flag:
        countries.append(33)

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

names = ['character_name']
sexes = ['character_sex']
ages = ['character_age']
occupations = ['character_occupation']
lives = ['character_is_alive']
species = ['species_id']
countries = ['country_id']
appearances = ['appearance_id']

id = 1
for quest in quests_list:
    if append_one_elem(quest, id, names, sexes, ages, occupations, lives, species, countries, appearances) is None:
        id -= 1
    print(str(id) + '/' + str(len(quests_list)) + '\r', end='')
    id += 1

np.savetxt('characters.csv', [p for p in zip(names, sexes, ages, occupations, lives, species, countries, appearances)], delimiter=',', fmt='%s')
