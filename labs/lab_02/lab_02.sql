select distinct c1.name, c1.occupation
from witcher.characters c1 join witcher.characters as c2 on c2.country_id != c1.country_id
where c2.character_age != c1.character_age
	  and c1.species_id == 8
order by c1.name, c1.occupation