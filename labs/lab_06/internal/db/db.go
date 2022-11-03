package db

import (
	"database/sql"
)

type DB struct {
	db *sql.DB
}

func New(db *sql.DB) *DB {
	return &DB{db: db}
}

func (db *DB) MaxLocationSquare() (float64, error) {
	var res float64

	if err := db.db.QueryRow("select max(location_square) from witcher.locations").Scan(&res); err != nil {
		return -1.0, err
	}

	return res, nil
}

type LocationQuest struct {
	QuestName    string
	LocationName string
}

func (db *DB) LocationForEachQuest() ([]LocationQuest, error) {
	query := `
select lq.quest_name, lq.location_name
		from (witcher.quests q join witcher.locations_quests lq_buf
			  on q.quest_id = lq_buf.quest_id
			  join witcher.locations l
			  on l.location_id = lq_buf.location_id) as lq;
`
	rows, err := db.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	res := make([]LocationQuest, 0)

	for rows.Next() {
		var lq LocationQuest
		if err := rows.Scan(&lq.QuestName, &lq.LocationName); err != nil {
			return nil, err
		}
		res = append(res, lq)
	}
	return res, nil
}

type LocationStats struct {
	LocationType string
	MinSquare    float64
	MaxSquare    float64
	AvgSquare    float64
}

func (db *DB) LocationsStats() ([]LocationStats, error) {
	query := `
with locations_stats as (select distinct l.location_type,
						 				 min(location_square) over (partition by location_type) as min_square,
						 				 max(location_square) over (partition by location_type) as max_square,
										 avg(location_square) over (partition by location_type) as avg_square
						from witcher.locations l
						order by l.location_type)
select * from locations_stats;
`
	rows, err := db.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	res := make([]LocationStats, 0)

	for rows.Next() {
		var l LocationStats
		if err := rows.Scan(&l.LocationType, &l.MinSquare, &l.MaxSquare, &l.AvgSquare); err != nil {
			return nil, err
		}
		res = append(res, l)
	}
	return res, nil
}

func (db *DB) Tables(schema string) ([]string, error) {
	query := `
select table_name from information_schema.tables
where table_schema = $1
`
	rows, err := db.db.Query(query, schema)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	res := make([]string, 0)
	for rows.Next() {
		var s string
		if err := rows.Scan(&s); err != nil {
			return nil, err
		}

		res = append(res, s)
	}

	return res, nil
}

func (db *DB) AvgLocationSquare(locationType string) (float64, error) {
	var res float64

	if err := db.db.QueryRow("select avg_location_square from witcher.avg_location_square($1)", locationType).Scan(&res); err != nil {
		return -1.0, err
	}

	return res, nil
}

type Quest struct {
	QuestId   int64
	QuestName string
	QuestType string
}

func (db *DB) QuestsByIssuingAndReward(issuing string, reward string) ([]Quest, error) {
	rows, err := db.db.Query("select * from witcher.quests_by_issuing_and_reward($1, $2)", issuing, reward)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	res := make([]Quest, 0)
	for rows.Next() {
		var q Quest
		if err := rows.Scan(&q.QuestId, &q.QuestName, &q.QuestType); err != nil {
			return nil, err
		}

		res = append(res, q)
	}

	return res, nil
}

func (db *DB) DeleteByName(name string) error {
	_, err := db.db.Exec("call witcher.delete_by_name($1)", name)
	return err
}

func (db *DB) CurrentDB() (string, error) {
	var res string

	if err := db.db.QueryRow("select  current_database()").Scan(&res); err != nil {
		return "", err
	}

	return res, nil
}

type WitcherSchool struct {
	SchoolId     int
	SchoolName   string
	SchoolLeader string
	LocationId   int
}

func (db *DB) CreateWitcherSchoolsTable() error {
	query := `
drop table if exists witcher.schools;
create table witcher.schools(
    school_id serial primary key,
    school_name text,
    school_leader text,
    location_id int references witcher.locations on delete cascade
);
`
	_, err := db.db.Exec(query)
	return err
}

func (db *DB) InsertIntoWitcherSchoolsTable(s WitcherSchool) error {
	_, err := db.db.Exec("insert into witcher.schools(school_id, school_name, school_leader, location_id) values ($1, $2, $3, $4)", s.SchoolId, s.SchoolName, s.SchoolLeader, s.LocationId)
	return err
}
