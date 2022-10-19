-- 1. Из таблиц базы данных, созданной в первой лабораторной работе, извлечь
-- данные в XML (MSSQL) или JSON(Oracle, Postgres). Для выгрузки в XML
-- проверить все режимы конструкции FOR XML.
drop procedure if exists backup();

create or replace procedure backup()
    language plpgsql
as
$$
declare
    t     text;
    query text;
begin
    for t in
        select table_name
        from information_schema."tables"
        where table_schema = 'witcher'
        LOOP
            query := 'copy (select row_to_json(r) from witcher.' || t ||
                     ' as r) to ''/var/lib/postgresql/data/' || t ||
                     '.json''';
            raise notice '%', query;
            execute query;
        end loop;
end
$$;

call backup();

-- 2. Выполнить загрузку и сохранение XML или JSON файла в таблицу.
-- Созданная таблица после всех манипуляций должна соответствовать таблице
-- базы данных, созданной в первой лабораторной работе.
drop table if exists witcher.quests_copy;

create table witcher.quests_copy
(
    quest_id      INT PRIMARY KEY,
    quest_name    text not null,
    quest_type    text not null,
    quest_issuing text,
    quest_reward  TEXT
);

create temp table json_table
(
    json_t json
);

copy json_table from '/var/lib/postgresql/data/quests.json';

insert into witcher.quests_copy
SELECT j.*
FROM json_table
         cross join json_populate_record(null::witcher.quests_copy, json_t) AS j;

select *
from witcher.quests_copy;

-- 3. Создать таблицу, в которой будет атрибут(-ы) с типом XML или JSON, или
-- добавить атрибут с типом XML или JSON к уже существующей таблице.
-- Заполнить атрибут правдоподобными данными с помощью команд INSERT
-- или UPDATE.
alter table witcher.species
    add example json;

update witcher.species
set example = ('{
  "creature": {
    "name": "Зжин",
    "age": 45
  },
  "info": "полководец-боболак, ведший армию своего народа из Пустульских гор на бой с людьми"
}'::json)
where species_id = 1;

update witcher.species
set example = ('{
  "creature": {
    "name": "Детлафф ван дер Эретайн",
    "age": 522
  },
  "info": "один из центральных персонажей и антагонист дополнения Кровь и Вино к игре Ведьмак 3: Дикая Охота, могущественный высший вампир"
}'::json)
where species_id = 2;

update witcher.species
set example = ('{
  "creature": {
    "name": "Слуга Дагона",
    "age": 23
  },
  "info": "Жрец-водяной, поклоняющийся Дагону, обитает в его храме на отмели. Изначально настроен по отношению к ведьмаку нейтрально, но по ходу битвы становится враждебным."
}'::json)
where species_id = 3;

update witcher.species
set example = ('{
  "creature": {
    "name": "Страж",
    "age": 53
  },
  "info": "персонаж в игре Ведьмак 2: Убийцы Королей, призрак-охранник древнего меча вранов."
}'::json)
where species_id = 4;

update witcher.species
set example = ('{
  "creature": {
    "name": "Альфред Набель",
    "age": 66
  },
  "info": "упоминаемый персонаж в играх Ведьмак и Ведьмак 2: Убийцы Королей, учёный-гном, создатель взрывчатого вещества, способного разорвать на куски крепчайший гранит."
}'::json)
where species_id = 5;

update witcher.species
set example = ('{
  "creature": {
    "name": "Виллентретенмерт",
    "age": 300
  },
  "info": "уникальный золотой дракон, умеющий менять свой облик на человеческий или любой другой. В облике рыцаря Борха дракон путешествует в компании двух преданных ему зерриканских воительниц — Тэи и Вэи."
}'::json)
where species_id = 6;

update witcher.species
set example = ('{
  "creature": {
    "name": "Золтан Хивай",
    "age": 52
  },
  "info": "деловитый предприниматель-краснолюд, наемник, один из лучших друзей Геральта, а также герой множества трактирных баек и пересудов."
}'::json)
where species_id = 7;

update witcher.species
set example = ('{
  "creature": {
    "name": "Калантэ Фиона Рианнон",
    "age": 45
  },
  "info": "королева Цинтры из рода Кербинов, правившая в середине XIII века, мать Паветты и бабушка Цири."
}'::json)
where species_id = 8;

update witcher.species
set example = ('{
  "creature": {
    "name": "Отто Бамбер",
    "age": 38
  },
  "info": "травник, живущий на севере от Новиградских Ворот Оксенфурта."
}'::json)
where species_id = 9;

update witcher.species
set example = ('{
  "creature": {
    "name": "Эитнэ",
    "age": 200
  },
  "info": "повелительница дриад и могущественная владычица Брокилона."
}'::json)
where species_id = 10;

update witcher.species
set example = ('{
  "creature": {
    "name": "Эредин Бреакк Глас",
    "age": 300
  },
  "info": "эльф высокого социального статуса из народа Aen Elle, командир Dearg Ruadhri."
}'::json)
where species_id = 11;

select *
from witcher.species;

-- 4.1 Извлечь XML/JSON фрагмент из XML/JSON документа.
select example -> 'creature' as name
from witcher.species;

-- 4.2 Извлечь значения конкретных узлов или атрибутов XML/JSON
-- документа.
select example -> 'creature' -> 'name', example -> 'info'
from witcher.species

-- 4.3 Выполнить проверку существования узла или атрибута.
         drop function if exists is_key(text, json);

create or replace function is_key(k text, j json)
    returns boolean
    language plpgsql
as
$$
begin
    return j -> k is not null;
end;
$$;

select example -> 'creature' -> 'name' as name, is_key('lname', example) as lname_key
from witcher.species;

select example -> 'creature' -> 'name' as name, is_key('info', example) as lname_key
from witcher.species;

-- 4.4 Изменить XML/JSON документ.
update witcher.species
set example = ('{
  "creature": {
    "name": "Сирисса",
    "age": 100
  },
  "info": "персонаж в книге «Меч Предназначения», брокилонская дриада, отличающаяся редкой красотой."
}'::json)
where species_id = 10;

-- 4.5 Разделить XML/JSON документ на несколько строк по узлам.
with records as (select json_agg(example) as arr
                   from witcher.species)
select json_array_elements(records.arr)
from records



