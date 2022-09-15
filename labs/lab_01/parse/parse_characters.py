import csv
import random
import time

import requests
import numpy as np
from bs4 import BeautifulSoup


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
        countries.append('')

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
