ALTER TABLE witcher.quests
    ADD CONSTRAINT correct_quest_type CHECK (quest_type = 'Основной' OR quest_type = 'Второстепенный');

ALTER TABLE witcher.locations
    ADD CONSTRAINT correct_location_square CHECK (location_square > 0.0);

ALTER TABLE witcher.appearances
    ADD CONSTRAINT correct_appearance_year CHECK (appearance_year > 1200);
   
ALTER TABLE witcher.appearances
    ADD CONSTRAINT correct_appearance_replicas_number CHECK (appearance_replicas_number >= 0);
    
ALTER TABLE witcher.characters
    ADD CONSTRAINT correct_character_age CHECK (character_age >= 0 and character_age <= 100);