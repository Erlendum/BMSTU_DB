ALTER TABLE witcher.quest
    ADD CONSTRAINT correct_quest_type CHECK (quest_type = 'Основной' OR quest_type = 'Второстепенный');