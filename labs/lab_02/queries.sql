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

-- Защита.
select *
into temp spies
from witcher.characters
where character_occupation like '%Шпион%' and country_id in
(select country_id
from witcher.countries
where country_name = 'Цинтра' or country_name = 'Ковир и Повис' or country_name = 'Редания'
or country_name = 'Аэдирн' or country_name = 'Лирия и Ривия' or country_name = 'Тимерия'
or country_name = 'Каэдвен')

select *
from spies
union
select *
from spies
where character_sex = 'Женский'
--

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


-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT.
-- Сформировать временную таблицу государств (id + название) с их религиями (название + лидеры).
select ce.country_id, ce.country_name, ce.religion_name, ce.religion_leaders
into temp countries_with_religions
from (countries c
	join witcher.religions r on c.religion_id = r.religion_id) as ce

select * from countries_with_religions
order by religion_leaders


-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM.
-- Вывести десять персонажей с самым большим количеством реплик и десять персонажей с самым маленьким количество реплик.
select c.character_name, a.appearance_replicas_number
from witcher.characters c join
	(
		select appearance_id, appearance_replicas_number
		from witcher.appearances
		order by appearance_replicas_number desc
		limit 10
	) a on c.appearance_id = a.appearance_id
union
select c.character_name, a.appearance_replicas_number
from witcher.characters c join
	(
		select appearance_id, appearance_replicas_number
		from witcher.appearances
		order by appearance_replicas_number asc
		limit 10
	) a on c.appearance_id = a.appearance_id
	
	
-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
-- Вывести имена персонажей, которые появлялись в локациях, где происходили второстепенные квесты.
select character_name
from witcher.characters
where appearance_id  in
(
	select appearance_id 
	from appearances_locations al
	where al.location_id in
	(
		select location_id
		from locations_quests lq
		where lq.quest_id in
		(
			select quest_id
			from quests
			where quest_type = 'Второстепенный'
		)	
	)
)


-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING.
-- Для каждой религии вывести количество стран, которые её исповедуют.
select r.religion_name, count_countries
from witcher.religions r join
(
	select witcher.countries.religion_id, count(*) as count_countries
	from witcher.countries
	group by religion_id
) c on r.religion_id = c.religion_id


-- 15.Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING.
-- Вывести типы локаций, средняя площадь которых больше среднего значения средней площади всех локаций.
select location_type, avg(location_square) 
from witcher.locations
group by location_type
having avg(location_square) >
	(
		select avg(avg_locations_type_square)
		from
		(
			select avg(location_square) as avg_locations_type_square
			from witcher.locations
			group by location_type
		) as locations_type_square
		
	)


-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.
delete from witcher.appearances
where appearance_id = '2309'

delete from witcher.characters
where character_name = 'Катя'

insert into witcher.appearances
values
	(2309, 1254, 'Книга', '«Меч Предназначения»', 80)
	
insert into witcher.characters
values
	('Катя', 'Женский', 20, 'Эскорт Золотого Дракона', true, 10, 7, 2309)
	
select *
from witcher.characters
where character_name = 'Катя'


-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса.
insert into witcher.appearances (appearance_id, appearance_year, appearance_type, appearance_name, appearance_replicas_number)
select
	(
		select count(*) + 1
		from witcher.appearances
	),
	
	(
		1230
	),
	
	(
		'Книга'
	),
	
	(
		'Ведьмак'
	),
	
	(
		select max(appearance_replicas_number)
		from witcher.appearances
		where appearance_name like '%жертвенности%'
	)
	

-- 18. Простая инструкция UPDATE.
update witcher.appearances
set appearance_year = appearance_year + 1
where appearance_id = 2309


-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.
update witcher.appearances
set appearance_replicas_number = 
(
	select
	avg(appearance_replicas_number)
	from witcher.appearances
)
where appearance_id = 2309


-- 20. Простая инструкция DELETE.
delete from witcher.appearances
where appearance_id = 2309


-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE.
-- Удалить всех персонажей, которые не прикреплены к какой-либо локации (по сути, тех, кого не было в играх).
delete from witcher.characters c
where c.appearance_id not in
(
	select appearance_id
	from appearances a
	where a.appearance_id in
	(
		select appearance_id
		from appearances_locations 
	)
)


-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение.
-- Вывести для каждого рода деятельности персонажа среднее количество реплик.
with occupation_stats (occupation_name, replicas_number) as
(
	select c.character_occupation, avg(a.appearance_replicas_number)
	from witcher.characters c
		join witcher.appearances a
		on c.appearance_id = a.appearance_id 
	group by c.character_occupation
)
select *
from occupation_stats


-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение.
-- Вывести уровни персонажей по расе (самый высокий уровень -- дракон, самый низкий -- боболак).
drop table if exists species_lvl;

create table if not exists species_lvl
(
    id serial primary key,
    id_on int,
    species_id int

);

insert into species_lvl(id_on, species_id) values
(2, 1),
(3, 3),
(4, 4),
(5, 9),
(6, 5),
(7, 7),
(8, 8),
(9, 10),
(10, 2),
(11, 11),
(12, 6)

with recursive character_lvls (id, species_id, id_on) as
(
	select id, species_id, id_on
	from species_lvl as sl
	where sl.id = 1
	union all
	select sl.id, sl.species_id, sl.id_on
	from species_lvl as sl
		join character_lvls as rec on sl.id = rec.id_on
)
select c.character_name, c.species_id, cl.id as lvl
from witcher.characters c
	join character_lvls cl on c.species_id = cl.species_id
	
	
-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER()
-- Вывести локации и три характеристики типа локации (минимальная площадь, максимальная площадь, средняя площадь).
select l.location_id, l.location_name, l.location_type, l.location_square,
	min(location_square) over(partition by location_type) as min_square,
	max(location_square) over(partition by location_type) as max_square,
	avg(location_square) over(partition by location_type) as avg_square
from locations l
order by l.location_type


-- 25. Оконные функции для устранения дублей.
insert into witcher.characters
values
	('Ящер2', 'Мужской', 46, 'Кулачный боец', true, 8, 33, 2308)

with duplications as
(
	select *, row_number() over (partition by character_sex, character_age, character_occupation, character_is_alive, country_id, appearance_id) as num
	from witcher.characters
)
select *
from duplications
where num > 1







