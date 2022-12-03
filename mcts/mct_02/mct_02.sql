-- Вариант 4.
-- Задание 1. Создать базу данных RK2. Создать в ней структуру соответсвующую указаннрой на ER-диаграмме.
-- Заполнить таблицы тестовыми значениями (не менее 10 в каждой таблице).

create database RK2;

drop table if exists regions;
drop table if exists sanatoriums;
drop table if exists vacationers;
drop table if exists sanatoriums_vacationers;

create table if not exists regions
(
	region_id serial primary key,
	region_name text,
	region_description text
);

create table if not exists sanatoriums
(
	sanatorium_id serial primary key,
	sanatorium_name text,
	sanatorium_year int,
	sanatorium_description text,
	region_id int not null,
	foreign key (region_id) references regions(region_id) on delete cascade
);

create table if not exists vacationers
(
	vacationer_id serial primary key,
	vacanioner_fio text,
	vacanioner_birth_year int,
	vacanioner_address text,
	vacanioner_email text
);

create table if not exists sanatoriums_vacationers
(
	sanatoriums_regions serial primary key,
	sanatorium_id int not null,
	vacationer_id int not null,
	foreign key (sanatorium_id) references sanatoriums(sanatorium_id) on delete cascade,
	foreign key (vacationer_id) references vacationers(vacationer_id) on delete cascade
);

insert into regions(region_name, region_description)
values
('Москва', 'Красиво, но грязно'),
('Московская область', 'Красиво, но много таджиков'),
('Краснодарский край', 'Жарко'),
('Республика Крым', 'Много гор'),
('Хабаровский край', 'Ужасный часовой пояс'),
('Хантымансийский автономный округ', 'Рядом тюрьмы'),
('Ростовская область', 'Рядом Донбасс'),
('Республика Татарстан', 'Есть куда сходить'),
('Саратовская область', 'Худшее место на земле'),
('Ленинградская область', 'Часто дожди');

insert into sanatoriums(sanatorium_name, sanatorium_year, sanatorium_description, region_id)
values
('Чайка', 1966, 'Бесплатные напитки у пляжа', 4),
('Мальва', 1988, 'Вкуснейшная шаурма на западе', 1),
('Природа', 2001, 'Много бабочек (не ночных)', 2),
('Фея', 2003, 'Есть аквпарк', 8),
('Профессорский уголок', 2005, 'Завтраки включены в стоимость', 9),
('У Рустема', 1988, 'Вкусный шашлык каждый вечер', 7),
('Инкогнито', 1976, 'Ракеты почти не прилетают', 7),
('Паруса', 1999, 'Массаж включён в стоимость', 3),
('Море', 1955, 'Бесплатные шезлонги и зонтики', 4),
('Пьяная черёмуха', 1984, 'Алкогольные напитки на любой вкус', 10);

insert into vacationers(vacanioner_fio, vacanioner_birth_year, vacanioner_address, vacanioner_email)
values
('Селиванова Софья Михайловна', 1984, '772595, Омская область, город Павловский Посад, шоссе Гоголя, 62', 'vesattussebroi-8260@yopmail.com'),
('Черный Фёдор Егорович', 1999, '562185, Московская область, город Лотошино, шоссе Славы, 64', 'reisseibauraffa-2994@yopmail.com'),
('Королев Михаил Вадимович', 2004, '306858, Читинская область, город Серпухов, спуск Гагарина, 06', 'breugrifebeutre-4537@yopmail.com'),
('Гончаров Филипп Арсентьевич', 1967, '758284, Пензенская область, город Коломна, въезд 1905 года, 14', 'gaunneuprajeuquo-4875@yopmail.com'),
('Фомина Софья Мироновна', 1991,'344506, Новгородская область, город Солнечногорск, въезд Бухарестская, 83',  'hulehellessi-6685@yopmail.com'),
('Дружинин Владислав Михайлович', 2002, '791776, Иркутская область, город Одинцово, бульвар Космонавтов, 59', 'wepeillacocre-3989@yopmail.com'),
('Островская Алиса Павловна', 2005, '977013, Смоленская область, город Лотошино, шоссе Славы, 06', 'dapraddossuxi-6494@yopmail.com'),
('Шмелев Александр Егорович', 1933, '121798, Рязанская область, город Клин, шоссе 1905 года, 74', 'frinebroiholla-8155@yopmail.com'),
('Жуков Александр Арсентьевич', 1959, '981712, Нижегородская область, город Видное, пер. Славы, 17', 'precrougoibroutroi-3162@yopmail.com'),
('Ларин Лев Маркович', 1965, '642537, Читинская область, город Серебряные Пруды, наб. Чехова, 41', 'rejoiddeddonu-1990@yopmail.com');

insert into sanatoriums_vacationers(sanatorium_id, vacationer_id)
values
(1, 2),
(2, 4),
(7, 1),
(8, 3),
(10, 10),
(5, 2),
(5, 9),
(4, 1),
(3, 3),
(6, 7);

-- Задание 2. Написать к разработанной базе данных 3 запроса, в комментарии указать, что этот запрос делает.

-- 1) Инструкция SELECT, использующая поисковое выражение CASE.
-- Вывести возрастную характеристику отдыхающих.

select vacanioner_fio,
case
	when vacanioner_birth_year < 1900 then 'Бессмертный'
	when vacanioner_birth_year between 1900 and 1920 then 'Древний'
	when vacanioner_birth_year between 1921 and 1950 then 'Старый'
	when vacanioner_birth_year between 1951 and 1980 then 'Нормальный'
	when vacanioner_birth_year between 1981 and 2000 then 'Молодой'
	when vacanioner_birth_year between 2001 and 2022 then 'Юнец'
	when vacanioner_birth_year > 2022 then 'Из будущего'
end as age_characteristic
from vacationers

-- 2) Инструкция UPDATE со скалярным подзапросом в предложении SET.
-- Минимизировать год основания санаториев (сделать годом основания каждого санатория минимальный из годов
-- основания всех санаториев).
update sanatoriums 
set sanatorium_year =
(
	select
	min(sanatorium_year)
	from sanatoriums 
);

-- 3) Инструкция SELECT, консолидирующая данные с помощью поредложения GROUP BY и предложения HAVING.
-- Вывести те регионы, количество санаториев в которых больше 1.

select rs.region_name, count(rs.sanatorium_id)
from (sanatoriums s join regions r on s.region_id = r.region_id) as rs
group by rs.region_name
having count(rs.sanatorium_id) > 1;

-- Задание 3. Создать хранимую процедуру с выходным параметром, которая уничтожает все представления
-- в текущей базе данных. Выхожной параметр возвращает количество уничтоженных представлений.
-- Созданную хранимую процедуру протестировать.

drop procedure if exists delete_views;
create or replace procedure delete_views(count_ inout int)
AS
$$
declare
    name_view record;
    cur cursor for 
        select viewname
        from pg_catalog.pg_views
        where schemaname <> 'pg_catalog'
        and schemaname <> 'information_schema';
begin
    open cur;
    loop 
        fetch cur into name_view;
        exit when not found;
        count_ = count_ + 1;
        execute 'drop view ' || name_view.viewname;
    end loop;
    close cur;
end
$$
language plpgsql;

-- Тестирование 

create view years_view as
  select *
  from sanatoriums
  where sanatorium_year > 1953;
 
 create view regions_with_rain_view as
  select *
  from regions
  where region_description like '%дожди%';
 
call delete_views(0);

