package app

import (
	"fmt"
	"lab_06/internal/db"
	"lab_06/utils"
	"os"
	"text/tabwriter"
)

type resolver struct {
	name string
	f    func() error
}

func (a *App) MaxLocationSquare() error {
	res, err := a.database.MaxLocationSquare()
	if err != nil {
		return err
	}

	fmt.Printf("Максимальная площадь локации: %f\n", res)

	return nil
}

func (a *App) LocationForEachQuest() error {
	res, err := a.database.LocationForEachQuest()
	if err != nil {
		return err
	}

	w := tabwriter.NewWriter(os.Stdout, 1, 1, 1, ' ', 0)
	fmt.Fprintf(w, "%s\t%s\n", "Квест", "Локация")
	fmt.Println()
	for _, row := range res {
		fmt.Fprintf(w, "%s\t%s\n", row.QuestName, row.LocationName)
	}

	w.Flush()

	return nil
}

func (a *App) LocationsStats() error {
	res, err := a.database.LocationsStats()
	if err != nil {
		return err
	}

	w := tabwriter.NewWriter(os.Stdout, 1, 1, 1, ' ', 0)
	fmt.Fprintf(w, "%s\t%s\t%s\t%s\n", "Тип локации", "Минималная площадь", "Максимальная площадь", "Средняя площадь")
	fmt.Println()
	for _, row := range res {
		fmt.Fprintf(w, "%s\t%f\t%f\t%f\n", row.LocationType, row.MinSquare, row.MaxSquare, row.AvgSquare)
	}

	w.Flush()

	return nil
}

func (a *App) Tables() error {
	res, err := a.database.Tables("witcher")
	if err != nil {
		return err
	}

	fmt.Printf("\nТаблицы схемы witcher:\n")
	for _, row := range res {
		fmt.Printf("%s\n", row)
	}

	return nil
}

func (a *App) AvgLocationSquare() error {
	var locationType string

	fmt.Print("Введите тип локации: ")

	locationType = utils.Scan()

	res, err := a.database.AvgLocationSquare(locationType)
	if err != nil {
		return err
	}

	fmt.Printf("\nСредняя площадь для локации типа %s: %f", locationType, res)
	fmt.Println(res)

	return nil
}

func (a *App) QuestsByIssuingAndReward() error {
	var issuing string
	var reward string

	fmt.Print("Введите выдающего квест: ")

	issuing = utils.Scan()

	fmt.Print("Введите награду за квест: ")

	reward = utils.Scan()

	res, err := a.database.QuestsByIssuingAndReward(issuing, reward)
	if err != nil {
		return err
	}

	w := tabwriter.NewWriter(os.Stdout, 1, 1, 1, ' ', 0)
	fmt.Fprintf(w, "%s\t%s\t%s\n", "Id квеста", "Название квеста", "Тип квеста")
	fmt.Println()
	for _, row := range res {
		fmt.Fprintf(w, "%d\t%s\t%s\n", row.QuestId, row.QuestName, row.QuestType)
	}

	w.Flush()

	return nil
}

func (a *App) DeleteByName() error {
	var name string

	fmt.Print("Введите имя персонажа: ")

	name = utils.Scan()

	err := a.database.DeleteByName(name)
	if err != nil {
		return err
	}

	fmt.Println("\nОперация завершена без ошибок (удаление выполнено или удалять нечего)")

	return nil
}

func (a *App) CurrentDB() error {
	res, err := a.database.CurrentDB()
	if err != nil {
		return err
	}

	fmt.Printf("\nТекущая база данных: %s\n", res)

	return nil
}

func (a *App) CreateWitcherSchoolsTable() error {
	err := a.database.CreateWitcherSchoolsTable()
	if err != nil {
		return err
	}

	fmt.Println("\nОперация успешно выполнена")

	return nil
}

func (a *App) InsertIntoWitcherSchoolsTable() error {
	var id int
	var name string
	var leader string
	var locationId int

	fmt.Print("Введите id ведьмачьей школы: ")

	if _, err := fmt.Scan(&id); err != nil {
		return err
	}

	fmt.Print("Введите название ведьмачьей школы: ")

	name = utils.Scan()

	fmt.Print("Введите лидера ведьмачьей школы: ")

	leader = utils.Scan()

	fmt.Print("Введите id локации ведьмачьей школы: ")

	if _, err := fmt.Scan(&locationId); err != nil {
		return err
	}

	err := a.database.InsertIntoWitcherSchoolsTable(db.WitcherSchool{
		id,
		name,
		leader,
		locationId})
	if err != nil {
		return err
	}

	fmt.Println("\nВедьмачья школа успешно добавлена")

	return nil
}
