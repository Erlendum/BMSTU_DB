package main

import (
	"flag"
	"fmt"
	"lab_09/internal/app"
	"os"
)

var mode = flag.Bool("mode", false, "mode: true - benchmark, false - usual mode")
var benchType = flag.String("benchType", "select", "benchType: select, insert, delete, update")
var benchShow = flag.String("benchShow", "DbAndRedis", "show only Db or only Redis bench results or db and redis")

func main() {
	flag.Parse()
	dsn := "host=localhost user=erlendum password=parasha dbname=Witcher port=5432"

	a, err := app.New(dsn, *benchShow)
	if err != nil {
		fmt.Printf("Ошибка инициализации приложения: %s\n", err)
		os.Exit(1)
	}
	if !(*mode) {
		if err := a.Run(); err != nil {
			fmt.Printf("Ошибка запуска приложения: %s\n", err)
			os.Exit(1)
		}
	} else {
		switch *benchType {
		case "Select":
			err := a.BenchmarkSelect()
			if err != nil {
				fmt.Printf("%s\n", err)
			}
		case "Insert":
			err := a.BenchmarkInsert()
			if err != nil {
				fmt.Printf("%s\n", err)
			}
		case "Delete":
			err := a.BenchmarkDelete()
			if err != nil {
				fmt.Printf("%s\n", err)
			}
		case "Update":
			err := a.BenchmarkUpdate()
			if err != nil {
				fmt.Printf("%s\n", err)
			}
		}

	}

}
