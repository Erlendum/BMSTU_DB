using menu_system;

namespace lab_07
{
    class Program
    {
        static void Main(string[] args)
        {
			List<MenuOption> menuOptions = new List<MenuOption>()
			{
				new MenuOptionWithAction("Количество персонажей, старших 50 лет", () => { App.PrintCountCharactersOlder50();
					Console.ReadKey();
				}),
				new MenuOptionWithAction("Живые персонажи-женщины", () => { App.PrintFemaleAliveWitches();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Персонажи, появляющиеся в книгах", () => { App.PrintCharactersAppearingInBooks();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Количество живых персонажей по полу", () => { App.PrintCountAliveBySex();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Краснолюды с возрастом, большим, чем средний возраст всех персонажей", () => { App.PrintKrasnoludsWithAgeMoreThanAvg();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Короли из Цинтры", () => { App.PrintKingsFromCintra();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Добавить 10 лет к возрасту королей из Цинтры", () => { App.Add10YearsOldtoKingsFromCintra();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Добавить персонажа JSON", () => { App.AddCharacter();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Количество квестов, выданных Йеннифэр", () => { App.PrintCountQuestBYennefer();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Язык указанного персонажа", () => { App.PrintLanguageOfCharacter();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Добавить персонажа SQL", () => { App.AddCharacterSQL();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Изменить возраст персонажа", () => { App.UpdateAgeOfCharacter();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Удалить указанный квест", () => { App.RemoveQuest();
					Console.ReadKey();
                
				}),
                new MenuOptionWithAction("Удалить указанного персонажа", () => { App.RemoveCharacter();
					Console.ReadKey();
                
				}),
			};

			Menu menu = new Menu(menuOptions, true, "Главное меню", "LINQ", true);
			
			menu.Run();
			
			Console.WriteLine("");
        }

    }
}
