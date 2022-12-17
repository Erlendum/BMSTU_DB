create extension if not exists plpython3u;

drop database if exists RK3;
create database RK3;

drop table if exists employees;
drop table if exists ins_outs;

create table if not exists employees
(
	employee_id serial primary key,
	employee_fio text not null,
	employee_birth_date date not null,
	employee_dep text not null
);

create table if not exists ins_outs
(
	employee_id int not null,
	ins_outs_date date not null,
	ins_outs_day text not null,
	ins_outs_time time not null,
	ins_outs_type int not null,
	foreign key (employee_id) references employees(employee_id) on delete cascade 
);

insert into employees(employee_fio, employee_birth_date, employee_dep) VALUES
('Иванов Иван Иванович', '1990-09-25', 'ИТ'),
('Петров Петр Петрович', '1987-11-12', 'Бухгалтерия'),
('Кострицкий Александр Сергеевич', '1993-05-14', 'Отдел тайн'),
('Глотов Илья Анатольевич', '2003-01-22', 'Бухгалтерия'),
('Княжев Алексей Викторович', '2002-06-23', 'Обслуживание параш')

insert into ins_outs (employee_id, ins_outs_date, ins_outs_day, ins_outs_time, ins_outs_type) VALUES
(1, '2018-12-14', 'Суббота', '9:00', 1),
(1, '2018-12-14', 'Суббота', '9:20', 2),
(1, '2018-12-14', 'Суббота', '9:25', 1),
(2, '2018-12-14', 'Суббота', '9:05', 1),
(3, '2018-12-14', 'Суббота', '9:25', 1),
(1, '2018-12-14', 'Суббота', '10:00', 2),
(1, '2018-12-14', 'Суббота', '10:10', 1),
(1, '2018-12-14', 'Суббота', '10:20', 2),
(1, '2018-12-14', 'Суббота', '10:30', 1),
(1, '2018-12-14', 'Суббота', '10:40', 2),
(1, '2018-12-14', 'Суббота', '10:50', 1);

drop function if exists min_age();

create or replace function min_age()
RETURNS real
AS $$
plan = plpy.prepare("""
select min(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM employee_birth_date)) as min_age
from employees
where employee_id in (
	with help_row_numbers as (
			select employee_id, ins_outs_date, ins_outs_time, ins_outs_type, row_number() over (partition by employee_id, ins_outs_date, ins_outs_type order by ins_outs_time) as r1
			from ins_outs
			order by employee_id, ins_outs_date, ins_outs_time, ins_outs_type)
		select employee_id
		from help_row_numbers
		where ins_outs_type = 1 and r1 = 1
		group by employee_id
		having max(ins_outs_time) - '09:00:00' > '00:10:00');""")

res = plpy.execute(plan)

if res:
	return res[0]['min_age']

$$ LANGUAGE plpython3u;

select * from min_age();



