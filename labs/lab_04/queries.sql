create extension if not exists plpython3u;

-- 1. Скалярная функция CLR.
-- Возвращает название локации по id локации, передающегося в качестве параметра.
drop function if exists get_location_name_by_id(int)

create or replace function get_location_name_by_id(loc_id int)
returns text
language plpython3u
as $$
	query = f"""
    select location_name
	from witcher.locations
	where location_id = {loc_id}
	"""
	res = plpy.execute(query)
	if res:
	    return res[0]['location_name']
$$

select *
from get_location_name_by_id(544) as "Location Name" 


-- 2. Пользовательская агрегатная функция CLR.
-- Возвращает максимальную площадь для типа локации, передающегося в качестве параметра.
drop function if exists get_max_location_square(text)

create or replace function get_max_location_square(loc_type text)
returns numeric
language plpython3u
as $$
	query = """
	select location_type, location_square
	from witcher.locations
	"""
	res = plpy.execute(query)
	if res:
		return max(row['location_square'] if row['location_type'] == loc_type else 0 for row in res)
$$

select *
from get_max_location_square('Дом') as "max_square"


-- 3. Табличная функция CLR.
-- Возвращает информацию о персонажах с характеристикой по возрасту.
drop function if exists get_characters_with_age_characteristic()

create or replace function get_characters_with_age_characteristic()
returns table
(
	character_name text,
	character_occupation text,
	age_characteristic text
)
language plpython3u
as $$
	def get_age_characteristic(age):
		if age is None:
			return 'No information'
		if age < 18:
			return 'Baby'
		if age >= 18 and age <= 30:
			return 'Mature'
		if age >= 30 and age <= 80:
			return 'Old'
		if age > 80:
			return 'God'
			
	query = """
	select character_name, character_occupation, character_age
	from witcher.characters
	"""
	res = plpy.execute(query)
	if res:
		for character in res:
			yield (character['character_name'], character['character_occupation'], get_age_characteristic(character['character_age']))
$$

select *
from get_characters_with_age_characteristic()
order by age_characteristic


-- 4. Хранимая процедура CLR.
-- Удаляет квесты, за которые не даётся никакая награда.
drop procedure if exists delete_quests_with_null_reward()

create or replace procedure delete_quests_with_null_reward()
language plpython3u
as $$
	query = """
	delete 
	from witcher.quests
	where quest_reward is null
	"""
	res = plpy.execute(query)
$$

select *
from witcher.quests
where quest_reward is null
call delete_quests_with_null_reward()


-- 5. Триггер CLR.
-- Если в таблицу добавили персонажа-ребёнка, то убить его.
drop function if exists kill_baby()

create or replace function kill_baby()
returns trigger
language plpython3u
as $$
	def is_baby(age):
		return age < 18
		
	age = TD["new"]["character_age"]
	is_alive = not is_baby(age)
	
	query = f"""
	insert into witcher.characters
	values ('{TD['new']['character_name']}', '{TD['new']['character_sex']}', '{TD['new']['character_age']}',
		'{TD['new']['character_occupation']}', '{is_alive}',
		'{TD['new']['species_id']}', '{TD['new']['country_id']}', '{TD['new']['appearance_id']}')
	"""
	plpy.execute(query)
	return None
$$

create or replace view character_view as
select *
from witcher.characters;

create trigger insert_baby
instead of insert on character_view
for row execute procedure kill_baby();

insert into witcher.appearances
values
	(2309, 1254, 'Книга', '«Меч Предназначения»', 80)

delete
from witcher.characters
where character_name = 'Кинжал'

insert into character_view (character_name, character_sex, character_age, character_occupation, character_is_alive, species_id, country_id, appearance_id)
values ('Кинжал', 'Мужской', 10, 'Пьяница', true, 8, 33, 2309)

select *
from witcher.characters
where character_name = 'Кинжал'


-- 6. Тип данных CLR.
-- Возвращает квесты и соответсвующие им локации.
create type quest_location as
(
	quest_name text,
	location_name text
)

drop function if exists get_quest_locations()

create or replace function get_quests_locations()
returns setof quest_location
language plpython3u
as $$
	query = """
	select t2.quest_name, t2.location_name
	from ((witcher.quests q join witcher.locations_quests lq on q.quest_id = lq.quest_id) as t1
		join witcher.locations l on l.location_id = t1.location_id)  as t2
	"""
	res = plpy.execute(query)
	return ([row for row in res])
$$

select *
from get_quests_locations()


