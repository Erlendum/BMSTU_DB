drop table if exists employees;

create table if not exists employees (
	id int,
    fio text,
    status text,
    date_of_status date
);

insert into employees values
(1, 'Иванов Иван Иванович', 'Работа offline', '2022-12-12'),
(1, 'Иванов Иван Иванович', 'Работа offline', '2022-12-13'),
(1, 'Иванов Иван Иванович', 'Больничный', '2022-12-14'),
(1, 'Иванов Иван Иванович', 'Больничный', '2022-12-15'),
(1, 'Иванов Иван Иванович', 'Удаленная работа', '2022-12-16'),
(2, 'Петров Петр Петрович', 'Работа offline', '2022-12-12'),
(2, 'Петров Петр Петрович', 'Работа offline', '2022-12-13'),
(2, 'Петров Петр Петрович', 'Удаленная работа', '2022-12-14'),
(2, 'Петров Петр Петрович', 'Удаленная работа', '2022-12-15'),
(2, 'Петров Петр Петрович', 'Работа offline', '2022-12-16');

select * from employees;

with numerate as (
    select row_number() over(
        partition by id, fio, status
        order by date_of_status
    ) as i, id, fio, status, date_of_status
    from employees
)
select id, fio, status, min(date_of_status) as date_start,
max(date_of_status) as date_stop
from numerate
group by id, fio, status, date_of_status - make_interval(days => i::int)
order by fio, date_start;




