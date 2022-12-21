-- Создать таблицы:
-- • Table1{id: integer, var1: string, valid_from_dttm: date, valid_to_dttm: date}
-- • Table2{id: integer, var2: string, valid_from_dttm: date, valid_to_dttm: date}
-- Версионность в таблицах непрерывная, разрывов нет (если valid_to_dttm =
-- '2018-09-05', то для следующей строки соответствующего ID valid_from_dttm =
-- '2018-09-06', т.е. на день больше). Для каждого ID дата начала версионности и
-- дата конца версионности в Table1 и Table2 совпадают.
-- Выполнить версионное соединение двух талиц по полю id.

drop table if exists table1, table2

create table if not exists table1
(
    id              integer,
    var1            text,
    valid_from_dttm date,
    valid_to_dttm   date
);

create table if not exists table2
(
    id              integer,
    var2            text,
    valid_from_dttm date,
    valid_to_dttm   date
);

insert into table1(id, var1, valid_from_dttm, valid_to_dttm)
values (1, 'A', '2018-09-01', '2018-09-15'),
       (1, 'B', '2018-09-16', '5999-12-31');

insert into table2(id, var2, valid_from_dttm, valid_to_dttm)
values (1, 'A', '2018-09-01', '2018-09-18'),
       (1, 'B', '2018-09-19', '5999-12-31');

select *
from table1;

select *
from table2;
                                              
WITH times AS (
    SELECT DISTINCT t1.id, var1, var2, greatest(t1.valid_from_dttm, t2.valid_from_dttm) AS valid_from_dttm,
    least(t1.valid_to_dttm, t2.valid_to_dttm) AS valid_to_dttm
    FROM table1 t1
    JOIN table2 t2
    ON t1.id = t2.id
)
SELECT *
FROM times
WHERE valid_from_dttm <= valid_to_dttm
ORDER BY valid_from_dttm


