copy witcher.religions FROM '/var/lib/postgresql/data/religions.csv' DELIMITER ',' CSV HEADER;

copy witcher.countries FROM '/var/lib/postgresql/data/countries.csv' DELIMITER ',' CSV HEADER;

copy witcher.quests FROM '/var/lib/postgresql/data/quests.csv' DELIMITER ',' CSV HEADER;

copy witcher.locations FROM '/var/lib/postgresql/data/locations.csv' DELIMITER ',' CSV HEADER;

copy witcher.species FROM '/var/lib/postgresql/data/species.csv' DELIMITER ',' CSV HEADER;

copy witcher.appearances FROM '/var/lib/postgresql/data/appearances.csv' DELIMITER ',' CSV HEADER;

copy witcher.characters FROM '/var/lib/postgresql/data/characters.csv' DELIMITER ',' CSV HEADER;

copy witcher.locations_quests FROM '/var/lib/postgresql/data/locations_quests.csv' DELIMITER ',' CSV HEADER;

copy witcher.appearances_locations FROM '/var/lib/postgresql/data/appearances_locations.csv' DELIMITER ',' CSV HEADER;
