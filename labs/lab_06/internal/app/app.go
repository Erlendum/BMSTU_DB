package app

import (
	"database/sql"
	"fmt"
	"lab_06/internal/db"
	"os"
)

type App struct {
	database  *db.DB
	resolvers []resolver
}

func New(dsn string) (*App, error) {
	database, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, err
	}

	a := &App{
		database: db.New(database),
	}

	a.resolvers = []resolver{
		{
			name: "Получить максимальную площадь локации",
			f:    a.MaxLocationSquare,
		},
		{
			name: "Получить локацию для каждого квеста",
			f:    a.LocationForEachQuest,
		},
		{
			name: "Получить минимальную, максимальную и среднюю площади для каждого типа локаций",
			f:    a.LocationsStats,
		},
		{
			name: "Получить названия таблиц в схеме",
			f:    a.Tables,
		},
		{
			name: "Получить среднюю площадь для типа локаций",
			f:    a.AvgLocationSquare,
		},
		{
			name: "Получить квест по выдающему и награде",
			f:    a.QuestsByIssuingAndReward,
		},
		{
			name: "Удалить персонажа по имени",
			f:    a.DeleteByName,
		},
		{
			name: "Получить название текущей базы данных",
			f:    a.CurrentDB,
		},
		{
			name: "Создать таблицу ведьмачьих школ",
			f:    a.CreateWitcherSchoolsTable,
		},
		{
			name: "Добавить ведьмачую школу",
			f:    a.InsertIntoWitcherSchoolsTable,
		},
		{
			name: "Выход",
			f: func() error {
				os.Exit(0)
				return nil
			},
		},
	}

	return a, nil
}

func (a *App) printMenu() {
	fmt.Printf("\nРабота с базой данных Witcher\n\n")

	for i, r := range a.resolvers {
		fmt.Printf("%d - %s\n", i+1, r.name)
	}
}

func (a *App) Run() error {
	for {
		a.printMenu()

		fmt.Println()

		var n int
		fmt.Print("Введите номер пункта меню: ")
		if _, err := fmt.Scan(&n); err != nil {
			fmt.Println(err)
			continue
		}

		if n-1 < 0 || n-1 >= len(a.resolvers) {
			fmt.Printf("Ошибка: некорректный пункт меню\n")
			continue
		}

		if err := a.resolvers[n-1].f(); err != nil {
			fmt.Printf("Ошибка: %s\n", err)
			continue
		}

		fmt.Println()
	}
}
