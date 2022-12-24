-- 1.1) Скалярная функция.
-- Возвращает среднюю площадь для типа локации, предающегося в качестве параметра.
drop function witcher.avg_location_square(text)
create or replace function witcher.avg_location_square(loc_type text)
returns int
language plpgsql
as $$
begin
	return (select avg(location_square)
			from witcher.locations
			where location_type = loc_type
			group by location_type);
end
$$

select avg_location_square
from avg_location_square('Банк')


-- 1.2) Подставляемая табличная функция.
-- Возвращает появление персонажа с именем, передающимся в качестве параметра.
drop function appearance_by_name(text)

create or replace function appearance_by_name(c_name text)
returns table
(
	appearance_year int,
	apperance_type text,
	appearance_name text
)
language plpgsql
as $$
begin
	return query
		select ca.appearance_year, ca.appearance_type, ca.appearance_name
		from (witcher.characters c
			join witcher.appearances a
			on c.appearance_id = a.appearance_id) as ca
		where ca.character_name = c_name;
end
$$

select *
from appearance_by_name('Калантэ')


-- 1.3) Многооператорная табличная функция.
-- Возвращает квесты с выдающим и наградой, передающимися в качестве параметров.
drop function witcher.quests_by_issuing_and_reward(text, text)

create or replace function witcher.quests_by_issuing_and_reward(issuing text, reward text)
returns table
(
	quest_id int,
	quest_name text,
	quest_type text
)
language plpgsql
as $$
begin
	return query
		select q.quest_id, q.quest_name, q.quest_type
		from witcher.quests q
		where q.quest_issuing like issuing;
	
	return query
		select q.quest_id, q.quest_name, q.quest_type
		from witcher.quests q
		where q.quest_reward like reward;
end
$$

select *
from witcher.quests_by_issuing_and_reward('Йенифэр', '%крон%')


-- 1.4) Функция с рекурсивным с рекурсивным ОТВ.
-- Возвращает всех персонажей с уровнем, передающимся в качестве параметра.
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

drop function characters_by_lvl(text)

create or replace function characters_by_lvl(lvl int)
returns table
(
	character_name text,
	character_species int,
	character_occupation text
)
language plpgsql
as $$
begin
	return query
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
		select c.character_name, c.species_id, c.character_occupation
		from witcher.characters c
			join character_lvls cl on c.species_id = cl.species_id
		where cl.id = lvl;
end
$$

select *
from characters_by_lvl(11)


-- 2.1) Хранимая процедура с параметрами.
-- Удаляет персонажа с именем, передающимся в качестве параметра.
drop procedure witcher.delete_by_name(text)

create or replace procedure witcher.delete_by_name(c_name text)
language plpgsql
as $$
begin
	delete
	from witcher.characters
	where character_name = c_name;
end
$$

select *
from witcher.characters
where character_name = 'Сериал:Геральт'

call delete_by_name('Сериал:Геральт')


-- 2.2) Рекурсивная хранимая процедура.
-- Вычисление i-ого члена последовательности Фибоначчи.
drop procedure fibonacci(inout int, int, int, int)

create or replace procedure fibonacci
(
	res inout int,
	index_  int,
	start_ int default 1, 
	end_ int default 1
)
language plpgsql
as $$
begin
	if index_ > 0 then
		raise notice 'elem = %', res;
		res = start_ + end_;
		call fibonacci(res, index_ - 1, end_, start_ + end_);
	end if;
end
$$

call fibonacci(1, 4)


with recursive factorial (n, factorial) AS (
    select 1, 1 
    union all
    select n + 1, (n + 1) * factorial
    from factorial 
    where n < 5 
)
select n,factorial from factorial;

-- 2.3) Хранимая процедура с курсором.
-- Вывести локацию для каждого квеста.
drop location_foreach_quest()

create or replace procedure location_foreach_quest()
language plpgsql
as $$
declare
	rec record;
	cur cursor for
		select lq.quest_name, lq.location_name
		from (witcher.quests q join witcher.locations_quests lq_buf
			  on q.quest_id = lq_buf.quest_id
			  join witcher.locations l
			  on l.location_id = lq_buf.location_id) as lq;
	 	
begin 
	open cur;
	loop
		fetch cur into rec;
		if found then
			raise notice e'q: % l: %', rec.quest_name, rec.location_name;
		end if;
		exit when not found;
	end loop;
	close cur;
end
$$

call location_foreach_quest()


-- 2.4) Хранимая процедура доступа к метаданным.
-- Вывести атрибуты и их типы таблицы, название которой предаётся в качестве параметра.
drop procedure table_attributes(text)

create or replace procedure table_attributes(table_n text)
language plpgsql
as $$
declare 
	attribute_name text;
	attribute_type text;
begin
	raise notice 'Table % has attributes:', table_n;
	
	for attribute_name, attribute_type in
		select column_name, data_type
		from information_schema."columns"
		where table_name = table_n
	loop
		raise notice '% %', attribute_name, attribute_type;
	end loop;
end
$$

call table_attributes('characters')



-- 3.1) Триггер AFTER.
-- После удаления расы удаление всех персонажей, которые относились к этой расе.
drop function delete_characters_after_delete_species()

create or replace function delete_characters_after_delete_species()
returns trigger
language plpgsql
as $$
begin 
	delete
	from witcher.characters
	where species_id = old.species_id;
	return old;
end
$$

create trigger delete_species
after delete on witcher.species
for each row execute procedure delete_characters_after_delete_species();

delete from witcher.characters
where species_id = 8

select * from witcher."characters" c 


-- 3.2) Триггер INSTEAD OF.
-- При вствке персонажа несоответсвующего пола, его пол заменяется на 'X'.
drop function correct_sex()

create or replace function correct_sex()
returns trigger
language plpgsql
as $$
declare
sexes text[] := array[
			'Мужской',
			'Женский',
			'X'
					];
sex text;
begin
	sex := new.character_sex;

	if array_position(sexes, sex) is null
	then
		sex := 'X';
	end if;

	insert into witcher.characters
	values (new.character_name, sex, new.character_age,
			new.character_occupation, new.character_is_alive,
			new.species_id, new.country_id, new.appearance_id);
		
	return new;
end
$$

create or replace view character_view as
select *
from witcher.characters;

create trigger insert_correct_sex
instead of insert on character_view
for row execute procedure correct_sex();

insert into witcher.appearances
values
	(2309, 1254, 'Книга', '«Меч Предназначения»', 80)
	
insert into character_view (character_name, character_sex, character_age, character_occupation, character_is_alive, species_id, country_id, appearance_id)
values ('Кинжал', 'Трасгендер', 10, 'Пьяница', false, 8, 33, 2309)

select *
from witcher.characters
where character_name = 'Кинжал'