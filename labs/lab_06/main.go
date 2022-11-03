package main

import (
	"fmt"
	_ "github.com/lib/pq"
	"lab_06/internal/app"
	"os"
)

func main() {
	dsn := "user=erlendum password=parasha dbname=Witcher sslmode=disable"

	a, err := app.New(dsn)
	if err != nil {
		fmt.Printf("Ошибка инициализации приложения: %s\n", err)
		os.Exit(1)
	}

	if err := a.Run(); err != nil {
		fmt.Printf("Ошибка запуска приложения: %s\n", err)
		os.Exit(1)
	}
}
