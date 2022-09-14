DROP SCHEMA IF EXISTS witcher CASCADE ;

CREATE SCHEMA witcher

CREATE TABLE witcher.Quest
(
	quest_id INT PRIMARY KEY,
	quest_name TEXT,
	quest_type text,
	quest_issuing text,
	quest_reward TEXT
);