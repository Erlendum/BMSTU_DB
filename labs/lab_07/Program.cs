namespace lab_07
{
    class Program
    {
        static void Main(string[] args)
        {
            // Linq.LinqToSql.AddCharacter(new data_access.Witcher.Character
            // {
            //     character_name = "Параша",
            //     character_sex = "Мужской",
            //     character_age = 26,
            //     character_occupation = "Знахарь",
            //     character_is_alive = true,
            //     species_id = 8,
            //     country_id = 33,
            //     appearance_id = 2187
            // });
            // foreach (var i in  Linq.LinqToJson.KingsFromCintra())
            //     Console.WriteLine(i.character_age);
            // Console.WriteLine(Linq.LinqtoSql.LanguageOfCharacter("Геральт из Ривии"));
            Linq.LinqToSql.RemoveCharacter("Адалия");
        }

    }
}
