package db

import (
	"database/sql"
	"fmt"
	"gorm.io/gorm"
)

type DB struct {
	db *gorm.DB
}

func New(db *gorm.DB) *DB {
	return &DB{db: db}
}

func rowsToString(rows *sql.Rows) string {
	cols, _ := rows.Columns()
	vals := make([]interface{}, len(cols))
	var res string
	for i := range cols {
		vals[i] = new(interface{})
	}
	for rows.Next() {
		rows.Scan(vals...)
		for _, v := range vals {
			res += fmt.Sprintf("%v ", *v.(*interface{}))
		}
		res += "\n"
	}

	return res
}

func (db *DB) TopLocations() (string, error) {
	rows, err := db.db.Raw("select location_name, location_square from witcher.locations order by location_square desc limit 10;").Rows()
	if err != nil {
		return "", err
	}
	res := rowsToString(rows)

	return res, nil
}

func (db *DB) Insert() (string, error) {
	rows, err := db.db.Raw("insert into witcher.schools (school_name, school_leader, location_id) values ('Школа Волка', 'Весемир', 263);").Rows()
	if err != nil {
		return "", err
	}
	res := rowsToString(rows)
	return res, nil
}

func (db *DB) Update() (string, error) {
	rows, err := db.db.Raw("update witcher.schools set school_leader = 'Геральт' where school_name = 'Школа Волка';").Rows()
	if err != nil {
		return "", err
	}
	res := rowsToString(rows)
	return res, nil
}

func (db *DB) Delete() (string, error) {
	rows, err := db.db.Raw("delete from witcher.schools where school_id = 1;").Rows()
	if err != nil {
		return "", err
	}
	res := rowsToString(rows)
	return res, nil
}

func (db *DB) Select() (string, error) {
	rows, err := db.db.Raw("select * from witcher.schools").Rows()
	if err != nil {
		return "", err
	}
	res := rowsToString(rows)
	return res, nil
}
