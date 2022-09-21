DROP SCHEMA IF EXISTS witcher CASCADE;

CREATE SCHEMA witcher

CREATE TABLE witcher.Quests
(
	quest_id INT PRIMARY KEY,
	quest_name text not null,
	quest_type text not null,
	quest_issuing text,
	quest_reward TEXT
);	

CREATE TABLE witcher.Locations
(
	location_id INT PRIMARY KEY,
	location_name TEXT,
	location_type text,
	location_place text,
	location_square numeric
	
);

CREATE TABLE witcher.Appearances
(
	appearance_id INT PRIMARY KEY,
	appearance_year INT,
	appearance_type text,
    appearance_name text,
    appearance_replicas_number int
);

CREATE TABLE witcher.Religions
(
	religion_id INT PRIMARY KEY,
	religion_name text,
	religion_type text,
    religion_symbol text,
    religion_gods text,
    religion_leaders text
);

CREATE TABLE witcher.Countries
(
	country_id INT PRIMARY KEY,
	country_name text,
	country_capital text,
    country_status text,
    country_currency text,
    country_polity text,
    country_leaders text,
    country_language text,
	religion_id INT not null,
	FOREIGN KEY (religion_id) references witcher.Religions(religion_id) on delete cascade
);

CREATE TABLE witcher.Species
(
	species_id INT PRIMARY KEY,
	species_name text,
	species_types text,
    species_features text,
    location_id INT not null,
	FOREIGN KEY (location_id) references witcher.Locations(location_id) on delete cascade
);

CREATE TABLE witcher.Characters
(
	character_name text primary KEY,
	character_sex text,
    character_age int,
    character_occupation text,
    character_is_alive bool,
	species_id int not null,
	country_id int not null,
	appearance_id int not null,
	FOREIGN KEY (species_id) references witcher.Species(species_id) on delete cascade,
	FOREIGN KEY (country_id) references witcher.Countries(country_id) on delete cascade,
	FOREIGN KEY (appearance_id) references witcher.Appearances(appearance_id) on delete cascade
);

CREATE TABLE witcher.locations_quests (
    locations_quests_id int PRIMARY KEY,
    location_id int not null,
    quest_id int not null,
    FOREIGN KEY (location_id) references witcher.Locations(location_id) on delete cascade,
    FOREIGN KEY (quest_id) references witcher.Quests(quest_id) on delete cascade
);

CREATE TABLE witcher.appearances_locations (
    appearances_locations_id int primary key,
    appearance_id int not null,
    location_id int not null,
    FOREIGN KEY (location_id) references witcher.Locations(location_id) on delete cascade,
    FOREIGN KEY (appearance_id) references witcher.Appearances(appearance_id) on delete cascade
);


