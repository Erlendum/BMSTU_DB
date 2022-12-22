package app

import (
	"context"
	"fmt"
	"github.com/go-redis/redis/v8"
	"time"
)

const N = 100
const STEP = 10

type resolver struct {
	name string
	f    func() error
}

func (a *App) TopLocations() error {
	start := time.Now()
	ctx := context.Background()
	resRedis, err := a.rdb.Get(ctx, "topLocations").Result()
	if err != nil && err != redis.Nil {
		return err
	}
	if resRedis != "" {
		fmt.Printf("Топ 10 локаций по площади: \n%stime = %v", resRedis, time.Since(start))
		return nil
	}
	res, err := a.database.TopLocations()
	if err != nil {
		return err
	}
	fmt.Printf("Топ 10 локаций по площади: \n%stime = %v", res, time.Since(start))
	a.rdb.Set(ctx, "topLocations", res, 0)

	return nil
}

func (a *App) Insert() error {
	ctx := context.Background()
	_, err := a.database.Insert()
	if err != nil {
		return err
	}
	a.rdb.Expire(ctx, "WitcherSchools", 0)
	return nil
}

func (a *App) Update() error {
	ctx := context.Background()
	_, err := a.database.Update()
	if err != nil {
		return err
	}
	a.rdb.Expire(ctx, "WitcherSchools", 0)
	return nil
}

func (a *App) Delete() error {
	ctx := context.Background()
	_, err := a.database.Delete()
	if err != nil {
		return err
	}
	a.rdb.Expire(ctx, "WitcherSchools", 0)
	return nil
}

func (a *App) SelectDB() (string, error) {
	res, err := a.database.Select()
	if err != nil {
		return res, err
	}
	return res, nil
}

func (a *App) SelectRedis() (string, error) {
	ctx := context.Background()
	resRedis, err := a.rdb.Get(ctx, "WitcherSchools").Result()
	if err != nil && err != redis.Nil {
		return "", err
	}
	if resRedis != "" {
		return resRedis, nil
	}
	res, err := a.database.Select()
	if err != nil {
		return res, err
	}
	a.rdb.Set(ctx, "WitcherSchools", res, 0)
	return res, nil
}

func (a *App) BenchmarkSelect() error {
	for i := 0; i < N; i++ {
		startDB := time.Now()
		_, err := a.SelectDB()
		timeDB := time.Since(startDB).Nanoseconds()
		if err != nil {
			return err
		}

		startRedis := time.Now()
		_, err = a.SelectRedis()
		timeRedis := time.Since(startRedis).Nanoseconds()
		if err != nil {
			return err
		}
		switch a.benchShow {
		case "Db":
			fmt.Printf("%d %d\n", i, timeDB)
		case "Redis":
			fmt.Printf("%d %d\n", i, timeRedis)
		default:
			fmt.Printf("%d %d %d\n", i, timeDB, timeRedis)
		}
	}
	return nil
}

func (a *App) BenchmarkInsert() error {
	for i := 0; i < N; i++ {
		switch a.benchShow {
		case "Db":
			startDB := time.Now()
			_, err := a.SelectDB()
			timeDB := time.Since(startDB).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d\n", i, timeDB)
		case "Redis":
			startRedis := time.Now()
			_, err := a.SelectRedis()
			timeRedis := time.Since(startRedis).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d\n", i, timeRedis)
		default:
			startDB := time.Now()
			_, err := a.SelectDB()
			timeDB := time.Since(startDB).Nanoseconds()
			if err != nil {
				return err
			}
			startRedis := time.Now()
			_, err = a.SelectRedis()
			timeRedis := time.Since(startRedis).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d %d\n", i, timeDB, timeRedis)
		}

		if i%STEP == 0 {
			err := a.Insert()
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func (a *App) BenchmarkDelete() error {
	for i := 0; i < N; i++ {
		switch a.benchShow {
		case "Db":
			startDB := time.Now()
			_, err := a.SelectDB()
			timeDB := time.Since(startDB).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d\n", i, timeDB)
		case "Redis":
			startRedis := time.Now()
			_, err := a.SelectRedis()
			timeRedis := time.Since(startRedis).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d\n", i, timeRedis)
		default:
			startDB := time.Now()
			_, err := a.SelectDB()
			timeDB := time.Since(startDB).Nanoseconds()
			if err != nil {
				return err
			}
			startRedis := time.Now()
			_, err = a.SelectRedis()
			timeRedis := time.Since(startRedis).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d %d\n", i, timeDB, timeRedis)
		}

		if i%STEP == 0 {
			err := a.Delete()
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func (a *App) BenchmarkUpdate() error {
	for i := 0; i < N; i++ {
		switch a.benchShow {
		case "Db":
			startDB := time.Now()
			_, err := a.SelectDB()
			timeDB := time.Since(startDB).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d\n", i, timeDB)
		case "Redis":
			startRedis := time.Now()
			_, err := a.SelectRedis()
			timeRedis := time.Since(startRedis).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d\n", i, timeRedis)
		default:
			startDB := time.Now()
			_, err := a.SelectDB()
			timeDB := time.Since(startDB).Nanoseconds()
			if err != nil {
				return err
			}
			startRedis := time.Now()
			_, err = a.SelectRedis()
			timeRedis := time.Since(startRedis).Nanoseconds()
			if err != nil {
				return err
			}
			fmt.Printf("%d %d %d\n", i, timeDB, timeRedis)
		}

		if i%STEP == 0 {
			err := a.Update()
			if err != nil {
				return err
			}
		}
	}
	return nil
}
