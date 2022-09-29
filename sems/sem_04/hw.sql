drop table if exists hw;

create table hw
(
	id int,
	p_name text,
	p_value text
);

insert into hw 
values (1, 'name', 'Julia'), (1, 'gender', 'f'), (2, 'name', 'Ivan')

select * from hw

select id, 
    max(case p_name when 'name' then p_value else null end) name,
    max(case p_name when 'gender' then p_value else null end) gender
from hw
group by id
order by id
