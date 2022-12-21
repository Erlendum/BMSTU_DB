package app

import (
	"fmt"
	"github.com/go-redis/redis/v8"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"lab_09/internal/db"
	"os"
)

type App struct {
	database  *db.DB
	resolvers []resolver
	rdb       *redis.Client
	benchShow string
}

func New(dsn string, benchShow string) (*App, error) {
	database, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, err
	}
	database.Exec("SET search_path TO Witcher")

	a := &App{
		database: db.New(database),
		rdb: redis.NewClient(&redis.Options{
			Addr:     "localhost:6379",
			Password: "sOmE_sEcUrE_pAsS",
			DB:       0,
		}),
		benchShow: benchShow,
	}

	a.resolvers = []resolver{
		{
			name: "Получить топ 10 локаций по площади",
			f:    a.TopLocations,
		},
		{
			name: "Получить сравнительную характеристику запросов к БД и Redis без изменения данных в БД",
			f:    a.BenchmarkSelect,
		},
		{
			name: "Получить сравнительную характеристику запросов к БД и Redis при добавлении новых строк каждые 10 секунд",
			f:    a.BenchmarkInsert,
		},
		{
			name: "Получить сравнительную характеристику запросов к БД и Redis при удалении строк каждые 10 секунд",
			f:    a.BenchmarkDelete,
		},
		{
			name: "Получить сравнительную характеристику запросов к БД и Redis при изменении строк каждые 10 секунд",
			f:    a.BenchmarkUpdate,
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
