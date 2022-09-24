-- 1. Инструкция SELECT, использующая предикат сравнения.
-- Вывести все локации типа Дом с площадью более 1000 квадратных метров.
select L.location_name, L.location_type, L.location_square
from witcher.locations as L
where L.location_type = 'Дом' and L.location_square > 1000.0


-- 2. Инструкция SELECT, использующая предикат BETWEEN.
-- Вывести всех персонажей, возраст которых от 18 до 30 лет.
select C.character_name, C.character_age
from witcher.characters as C
where C.character_age between 18 and 30


-- 3. Инструкция SELECT, использующая предикат LIKE.
-- Вывести все квесты, в награду за которые дают орены.
select Q.quest_name, Q.quest_reward
from witcher.quests as Q
where Q.quest_reward like '%оренов%'


-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
-- Вывести всех персонажей, которые способны говорить на Старшей Речи.
select C.character_name, C.character_occupation
from witcher.characters as C
where C.country_id in (select country_id from witcher.countries where country_language like '%Старшая Речь%')


-- 5.Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
-- Вывести все государства с культовой религией.
select C.country_name, C.country_status
from witcher.countries as C
where exists (select religion_id from witcher.religions where religion_type = 'Культ')


-- 6. Инструкция SELECT, использующая предикат сравнения с квантором.
-- Вывести персонажей, у которых возраст меньше, чем у всех гномов.
select C.character_name, C.character_age, C.character_occupation 
from witcher.characters as C
where C.character_age < all 
(select C1.character_age
from witcher.characters as C1
where C1.species_id in (select species_id from witcher.species where species_name = 'Гномы'))


-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
-- Вывести количество и средний возраст центрийских проституток.
select count(*), avg(character_age)
from witcher.characters
where character_occupation = 'Проститутка' and country_id in
(select country_id
from witcher.countries
where country_name = 'Цинтра')

-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов.
-- Вывести максимальную и среднюю площадь для каждого типа локации.
select distinct L.location_type,
	   ( select max(location_square) 
	   	 from witcher.locations
	   	 where locations.location_type = L.location_type
	   ) as max_square,
	   ( select avg(location_square)
	     from witcher.locations
	     where locations.location_type = L.location_type
	   ) as avg_square
from witcher.locations as  L


-- 9. Инструкция SELECT, использующая простое выражение CASE.
-- Вывести пояснение к полу персонажа.
select character_name,
	   case character_sex
	   		when 'Мужской' then 'Готов к мобилизации'
	   		when 'Женский' then 'Готов к воспитанию детей'
	   		else 'Готов к казни'
	   end as sex_characteristic
from witcher.characters


-- 10. Инструкция SELECT, использующая поисковое выражение CASE.
-- Вывести временную характеристику каждого появления персонажа.
select appearance_id, appearance_year, appearance_type, appearance_name, appearance_replicas_number,
	   case
	   		when appearance_year between 1230 and 1250 then 'Ранние события'
	   		when appearance_year between 1251 and 1272 then 'Основные события'
	   		when appearance_year between 1261 and 1278 then 'Поздние события'
	   end as time_characteristic
from witcher.appearances





