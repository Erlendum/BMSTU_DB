copy witcher.religions FROM '/docker-entrypoint-initdb.d/religions.csv' DELIMITER ',' CSV HEADER;

copy witcher.countries FROM '/docker-entrypoint-initdb.d/countries.csv' DELIMITER ',' CSV HEADER;

copy witcher.quests FROM '/docker-entrypoint-initdb.d/quests.csv' DELIMITER ',' CSV HEADER;

copy witcher.locations FROM '/docker-entrypoint-initdb.d/locations.csv' DELIMITER ',' CSV HEADER;

copy witcher.species FROM '/docker-entrypoint-initdb.d/species.csv' DELIMITER ',' CSV HEADER;

copy witcher.appearances FROM '/docker-entrypoint-initdb.d/appearances.csv' DELIMITER ',' CSV HEADER;

copy witcher.characters FROM '/docker-entrypoint-initdb.d/characters.csv' DELIMITER ',' CSV HEADER;

copy witcher.locations_quests FROM '/docker-entrypoint-initdb.d/locations_quests.csv' DELIMITER ',' CSV HEADER;

copy witcher.appearances_locations FROM '/docker-entrypoint-initdb.d/appearances_locations.csv' DELIMITER ',' CSV HEADER;