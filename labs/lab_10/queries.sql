select quest_name as quest, quest_issuing as Issuing from witcher.quests;

select location_square
from witcher.locations l;

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
limit 10;

select
now() as time_sec,
character_occupation as metric,
count(*) as value
from
witcher.characters
where character_occupation is not null
group by metric
order by value desc
limit 10;


select cc.country_name, count(*)
from (witcher.characters cha join witcher.countries co on cha.country_id = co.country_id) cc
where character_occupation like '%Проститутка%' or character_occupation like '%Куртизанка%'
group by cc.country_name;
