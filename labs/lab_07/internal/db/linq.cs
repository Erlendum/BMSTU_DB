using Newtonsoft.Json.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;

namespace Linq
{
    public class LinqToObjects
    {
        public static int CountCharactersOlder50()
        {
            int result = 0;
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var characters = db.characters.ToList();
                result = (
                          from c
                          in characters
                          where c.character_age > 50
                          select c
                         ).Count();
            }
            return result;
        }

        public static List<data_access.Witcher.Character> FemaleAliveWitches()
        {
            List<data_access.Witcher.Character> result = new List<data_access.Witcher.Character>();
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var characters = db.characters.ToList();
                var query = from c
                            in characters
                            where (c.character_sex == "Женский") &&
                                  (c.character_occupation == null || c.character_occupation.Contains("Чародейка")) &&
                                  (c.character_is_alive)
                            select c;
                foreach (var i in query)
                {
                    result.Add(i);
                }
            }
            return result;
        }

        public static List<data_access.Witcher.Character> CharactersAppearingInBooks()
        {
            List<data_access.Witcher.Character> result = new List<data_access.Witcher.Character>();
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var characters = db.characters.ToList();
                var appearances = db.appearances.ToList();
                var query = from c
                            in characters
                            join a in appearances
                            on c.appearance_id equals a.appearance_id
                            where a.appearance_type == "Книга"
                            orderby a.appearance_replicas_number
                            select c;
                foreach (var i in query)
                {
                    result.Add(i);
                }
            }
            return result;
        }

        public static (int, int) CountAliveBySex()
        {
            (int, int) result = default!;
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var characters = db.characters.ToList();
                var query = from c
                            in characters
                            where c.character_is_alive
                            group c by c.character_sex into g
                            select new { Name = g.Key, Count = g.Count() };
                foreach (var i in query)
                {
                    if (i.Name == "Мужской")
                        result.Item1 = i.Count;
                    else if (i.Name == "Женский")
                        result.Item2 = i.Count;
                }
            }
            return result;
        }

        public static List<data_access.Witcher.Character> KrasnoludsWithAgeMoreThanAvg()
        {
            List<data_access.Witcher.Character> result = new List<data_access.Witcher.Character>();
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var characters = db.characters.ToList();
                List<int> characters_ages = new List<int>();
                foreach (var c in characters)
                {
                    characters_ages.Add(c.character_age);
                }
                var query = from c
                            in characters
                            let avg = characters_ages.Average()
                            where c.species_id == 5 && c.character_age > avg
                            select c;
                foreach (var i in query)
                {
                    result.Add(i);
                }
            }
            return result;
        }
    }
    public class LinqToJson
    {
        public static List<data_access.Witcher.Character> KingsFromCintra()
        {
            JObject o = JObject.Parse(File.ReadAllText(@"../characters.json"));
            List<data_access.Witcher.Character> result = new List<data_access.Witcher.Character>();
            var query = from c
                        in o["items"]
                        where c["character_occupation"] != null && c["country_id"] != null && c["character_occupation"].ToString().Contains("Король") && c["country_id"].ToObject<int>() == 33
                        select c;
            foreach (var i in query)
            {
                var character = JsonSerializer.Deserialize<data_access.Witcher.Character>(i.ToString())!;
                result.Add(character);
            }
            return result;
        }
        public static void Add10YearsOldtoKingsFromCintra()
        {
            JObject o = JObject.Parse(File.ReadAllText(@"../characters.json"));
            List<data_access.Witcher.Character> result = new List<data_access.Witcher.Character>();
            var query = from c
                        in o["items"]
                        select c;
            var q = query.Select(c => { c["character_age"] = c["character_age"].ToObject<int>() + 10; return c; });

            File.AppendAllText(@"../characters.json", "{ \"items\" : [\n");
            foreach (var i in q)
            {
                File.AppendAllText(@"../characters.json", i.ToString() + ",\n");
            }
            File.AppendAllText(@"../characters.json", "]\n}");
        }

        public static void AddCharacter(data_access.Witcher.Character character)
        {
            JObject o = JObject.Parse(File.ReadAllText(@"../characters.json"));
            List<data_access.Witcher.Character> result = new List<data_access.Witcher.Character>();
            var query = from c
                        in o["items"]
                        select c;

            File.AppendAllText(@"../characters.json", "{ \"items\" : [\n");
            foreach (var i in query)
            {
                File.AppendAllText(@"../characters.json", i.ToString() + ",\n");
            }

            JsonSerializerOptions options = new JsonSerializerOptions
            {
                Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                WriteIndented = true
            };
            string adding_character = JsonSerializer.Serialize(character, options);

            File.AppendAllText(@"../characters.json", adding_character + ",\n");
            File.AppendAllText(@"../characters.json", "]\n}");
        }

    }

    public class LinqToSql
    {
        public static int CountQuestBYennefer()
        {
            int result = 0;
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var quests = db.quests;
                result = (
                          from q
                          in quests
                          where q.quest_issuing != null && q.quest_issuing.Contains("Йеннифэр")
                          select q
                         ).Count();
            }
            return result;
        }


        public static string LanguageOfCharacter(string character_name)
        {
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var characters = db.characters;
                var countries = db.countries;
                var query = (
                          from ca
                          in characters
                          join co
                          in countries
                          on ca.country_id equals co.country_id
                          where ca.character_name == String.Format("{0}", character_name)
                          select co.country_name
                         );
                if (query.Count() == 0)
                    return "";
                foreach (var i in query)
                    return i;
            }
            return "";
        }

        public static void AddCharacter(data_access.Witcher.Character character)
        {
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                db.characters.Add(character);
                db.SaveChanges();
            }
        }

        public static void UpdateAgeOfCharacter(string character_name, int character_age)
        {
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var character = db.characters.Find(character_name);
                if (character != null)
                {
                    character.character_age = character_age;
                    db.characters.Update(character);
                    db.SaveChanges();
                }
            }
        }

        public static void RemoveQuest(string quest_name)
        {
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                var quest = db.quests.Find(quest_name);
                if (quest != null)
                {
                    db.quests.Remove(quest);
                    db.SaveChanges();
                }
            }
        }

        public static void RemoveCharacter(string character_name)
        {
            using (data_access.PSQLContext db = new data_access.PSQLContext())
            {
                db.RemoveCharacter(character_name);
            }
        }

    }
}