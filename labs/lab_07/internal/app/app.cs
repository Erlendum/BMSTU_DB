public class App
{
    public static void PrintCountCharactersOlder50()
    {
        Console.Write("\nКоличество персонажей, старших 50 лет: " + Linq.LinqToObjects.CountCharactersOlder50());
    }
    public static void PrintFemaleAliveWitches()
    {
        Console.WriteLine("\nЖивые персонажи-женщины:");
        Console.WriteLine(String.Format("|{0,55}|{1,55}|", "Имя", "Возраст"));
        foreach (var i in Linq.LinqToObjects.FemaleAliveWitches())
            Console.WriteLine(String.Format("|{0,55}|{1,55}|", i.character_name, i.character_age));
    }
    public static void PrintCharactersAppearingInBooks()
    {
        Console.WriteLine("\nПерсонажи, появлявшиеся в книгах:");
        Console.WriteLine(String.Format("|{0,55}|{1,55}|", "Имя", "Возраст"));
        foreach (var i in Linq.LinqToObjects.CharactersAppearingInBooks())
            Console.WriteLine(String.Format("|{0,55}|{1,55}|", i.character_name, i.character_age));
    }
    public static void PrintCountAliveBySex()
    {
        Console.WriteLine("\nКоличество живых персонажей по полу:");
        Console.WriteLine(String.Format("|{0,15}|{1,15}|", "Мужской", "Женский"));
        var res = Linq.LinqToObjects.CountAliveBySex();
        Console.WriteLine(String.Format("|{0,15}|{1,15}|", res.Item1, res.Item2));
    }
    public static void PrintKrasnoludsWithAgeMoreThanAvg()
    {
        Console.WriteLine("\nКраснолюды с возрастом, большим, чем средний возраст всех персонажей:");
        Console.WriteLine(String.Format("|{0,55}|{1,55}|", "Имя", "Возраст"));
        foreach (var i in Linq.LinqToObjects.KrasnoludsWithAgeMoreThanAvg())
            Console.WriteLine(String.Format("|{0,55}|{1,55}|", i.character_name, i.character_age));
    }
    public static void PrintKingsFromCintra()
    {
        Console.WriteLine("\nКороли из Цинтры:");
        Console.WriteLine(String.Format("|{0,55}|{1,55}|", "Имя", "Возраст"));
        foreach (var i in Linq.LinqToJson.KingsFromCintra())
            Console.WriteLine(String.Format("|{0,55}|{1,55}|", i.character_name, i.character_age));
    }
    public static void Add10YearsOldtoKingsFromCintra()
    {
        Linq.LinqToJson.Add10YearsOldtoKingsFromCintra();
        Console.WriteLine("\nОперация успешно выполнена");
    }
    public static void AddCharacter()
    {
        Console.Write("\nВведите имя персонажа: ");
        string? _character_name = Console.ReadLine();

        Console.Write("Введите пол персонажа: ");
        string? _character_sex = Console.ReadLine();

        Console.Write("Введите возраст персонажа: ");
        int _character_age = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите род деятельности персонажа: ");
        string? _character_occupation = Console.ReadLine();
        
        Console.Write("Введите, жив ли персонаж (true - жив, false - мёртв): ");
        bool _character_is_alive = Convert.ToBoolean(Console.ReadLine());

        Console.Write("Введите id расы персонажа: ");
        int _species_id = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите id государства персонажа: ");
        int _country_id = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите id появления персонажа: ");
        int _appearance_id = Convert.ToInt32(Console.ReadLine());

        Linq.LinqToJson.AddCharacter(new data_access.Witcher.Character
        {
            character_name = _character_name,
            character_sex = _character_sex,
            character_age = _character_age,
            character_occupation = _character_occupation,
            character_is_alive = _character_is_alive,
            species_id = _species_id,
            country_id = _country_id,
            appearance_id = _appearance_id
        });
        Console.WriteLine("Операция успешно выполнена");
    }

    public static void RemoveCharacterJSON()
    {
        Console.Write("\nВведите имя персонажа: ");
        string? _character_name = Console.ReadLine();

        
        Linq.LinqToJson.RemoveCharacterJSON(_character_name);
        Console.WriteLine("Операция успешно выполнена");
    }

    public static void PrintCountQuestBYennefer()
    {
        Console.WriteLine("\nКоличество квестов, выданных Йеннифэр: " + Linq.LinqToSql.CountQuestBYennefer());
    }
    public static void PrintLanguageOfCharacter()
    {
        Console.Write("\nВведите имя персонажа: ");
        string? _character_name = Console.ReadLine();

        Console.WriteLine(String.Format("Язык персонажа {0}: ", _character_name) + Linq.LinqToSql.LanguageOfCharacter(_character_name));
    }
    public static void AddCharacterSQL()
    {
        Console.Write("\nВведите имя персонажа: ");
        string? _character_name = Console.ReadLine();

        Console.Write("Введите пол персонажа: ");
        string? _character_sex = Console.ReadLine();

        Console.Write("Введите возраст персонажа: ");
        int _character_age = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите род деятельности персонажа: ");
        string? _character_occupation = Console.ReadLine();
        
        Console.Write("Введите, жив ли персонаж (true - жив, false - мёртв): ");
        bool _character_is_alive = Convert.ToBoolean(Console.ReadLine());

        Console.Write("Введите id расы персонажа: ");
        int _species_id = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите id государства персонажа: ");
        int _country_id = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите id появления персонажа: ");
        int _appearance_id = Convert.ToInt32(Console.ReadLine());

        Linq.LinqToSql.AddCharacter(new data_access.Witcher.Character
        {
            character_name = _character_name,
            character_sex = _character_sex,
            character_age = _character_age,
            character_occupation = _character_occupation,
            character_is_alive = _character_is_alive,
            species_id = _species_id,
            country_id = _country_id,
            appearance_id = _appearance_id
        });
        Console.WriteLine("Операция успешно выполнена");
    }
    public static void UpdateAgeOfCharacter()
    {
        Console.Write("\nВведите имя персонажа: ");
        string? _character_name = Console.ReadLine();

        Console.Write("Введите новый возраст персонажа: ");
        int _character_age = Convert.ToInt32(Console.ReadLine());

       
        Linq.LinqToSql.UpdateAgeOfCharacter(_character_name, _character_age);
        Console.WriteLine("Операция успешно выполнена");
    }
    public static void RemoveQuest()
    {
        Console.Write("\nВведите имя квеста: ");
        string? _quest_name = Console.ReadLine();

        Linq.LinqToSql.RemoveQuest(_quest_name);
        Console.WriteLine("Операция успешно выполнена");
    }
    public static void RemoveCharacter()
    {
        Console.Write("\nВведите имя персонажа: ");
        string? _character_name = Console.ReadLine();

        Linq.LinqToSql.RemoveCharacter(_character_name);
        Console.WriteLine("Операция успешно выполнена");
    }


}