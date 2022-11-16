using Microsoft.EntityFrameworkCore;
using NpgsqlTypes;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace data_access
{
    namespace Witcher
    {
        [Table("quests", Schema = "witcher")]
        public class Quest
        {
            [Key] public int quest_id { get; set; }
            public string? quest_name { get; set; }
            public string? quest_type { get; set; }
            public string? quest_issuing { get; set; }
            public string? quest_reward { get; set; }

        }

        [Table("locations", Schema = "witcher")]
        public class Location
        {
            [Key] public int location_id { get; set; }
            public string? location_name { get; set; }
            public string? location_type { get; set; }
            public string? location_place { get; set; }
            public double location_square { get; set; }

        }

        [Table("appearances", Schema = "witcher")]
        public class Appearance
        {
            [Key] public int appearance_id { get; set; }
            public int? appearance_year { get; set; }
            public string? appearance_type { get; set; }
            public string? appearance_name { get; set; }
            public int appearance_replicas_number { get; set; }

        }

        [Table("religions", Schema = "witcher")]
        public class Religion
        {
            [Key] public int religion_id { get; set; }
            public string? religion_name { get; set; }
            public string? religion_type { get; set; }
            public string? religion_symbol { get; set; }
            public string? religion_gods { get; set; }
            public string? religion_leaders { get; set; }

        }

        [Table("countries", Schema = "witcher")]
        public class Country
        {
            [Key] public int country_id { get; set; }
            public string? country_name { get; set; }
            public string? country_capital { get; set; }
            public string? country_status { get; set; }
            public string? country_currency { get; set; }
            public string? country_polity { get; set; }
            public string? country_leaders { get; set; }
            public string? country_language { get; set; }
            public int religion_id { get; set; }

        }

        [Table("species", Schema = "witcher")]
        public class Species
        {
            [Key] public int species_id { get; set; }
            public string? species_name { get; set; }
            public string? species_types { get; set; }
            public string? species_features { get; set; }
            public int location_id { get; set; }

        }

        [Table("characters", Schema = "witcher")]
        public class Character
        {
            [Key] public string? character_name { get; set; }
            public string? character_sex { get; set; }
            public int character_age { get; set; }
            public string? character_occupation { get; set; }
            public bool character_is_alive { get; set; }
            public int species_id { get; set; }
            public int country_id { get; set; }
            public int appearance_id { get; set; }
        }

        [Table("locations_quests", Schema = "witcher")]
        public class LocationQuest
        {
            [Key] public int locations_quests_id { get; set; }
            public int location_id { get; set; }
            public int quest_id { get; set; }
        }

        [Table("appearances_locations", Schema = "witcher")]
        public class AppearanceLocation
        {
            [Key] public int appearances_locations_id { get; set; }
            public int appearance_id { get; set; }
            public int location_id { get; set; }
        }
    }
}
namespace data_access
{
    public class PSQLContext : DbContext
    {

        public DbSet<Witcher.Quest> quests { get; set; } = default!;

        public DbSet<Witcher.Location> locations { get; set; } = default!;

        public DbSet<Witcher.Appearance> appearances { get; set; } = default!;

        public DbSet<Witcher.Religion> religions { get; set; } = default!;

        public DbSet<Witcher.Country> countries { get; set; } = default!;

        public DbSet<Witcher.Species> species { get; set; } = default!;

        public DbSet<Witcher.Character> characters { get; set; } = default!;

        public DbSet<Witcher.LocationQuest> locations_quests { get; set; } = default!;
        public DbSet<Witcher.AppearanceLocation> appearances_locations { get; set; } = default!;
        public PSQLContext()
        {
            Database.EnsureCreated();
        }
        public void RemoveCharacter(string character_name)
        {
            var query = this.Database.SqlQueryRaw<int>($"call witcher.delete_by_name('{character_name}')");
            foreach (var i in query)
            {

            }
        }
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=Witcher;Username=erlendum;Password=parasha");
        }
    }
}