from faker import Faker
from random import randint
from random import uniform
from random import choice
import datetime
import sys
import json
import psycopg2
N = 10

quest_types = ["Основной", "Второстепенный"]
quest_issuings = ["Йеннифэр", "Доска объявлений", "Письмо", "Трисс Меригольд"]

def num_of_quests():
    try:

        con = psycopg2.connect(
            database="Witcher",
            user="erlendum",
            password="parasha",
            host="localhost",
            port="5432"		   
        )
    except:
        print("Ошибка при подключении к Базе Данных")
        return
    cur = con.cursor()

    cur.execute("SELECT max(quest_id) from witcher.quests;")

    rows = cur.fetchall()

    cur.close()
    con.close()
    return rows[0][0]


def generate_quests(num):
    faker = Faker(locale="ru_RU")
    f = open(str(sys.argv[1]) + '_quests_' + str(datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")) + '.json', 'w', encoding='utf8')
    f.write('[\n')
    for i in range(N):
        quest_type_id = randint(0, len(quest_types) - 1)
        quest_issuing_id = randint(0, len(quest_issuings) - 1)
        obj = {}
        obj['quest_id'] = num + i + 1
        obj['quest_name'] = faker.text()
        obj['quest_type'] = quest_types[quest_type_id]
        obj['quest_issuing'] = quest_issuings[quest_issuing_id]
        obj['quest_reward'] = str(randint(0, 500)) + ' оренов'

        if i != N - 1:
            f.write(json.dumps(obj, ensure_ascii=False) + ', \n')
        else:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    f.write(']')
    f.close()

num = num_of_quests()
generate_quests(num)