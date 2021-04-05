package dao

import "database/sql"

type Dao struct {
	engine *sql.DB
}

func New(engine *sql.DB) *Dao {
	return &Dao{engine: engine}
}
