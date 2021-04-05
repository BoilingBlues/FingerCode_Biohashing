package model

import "time"

type Log struct {
	CreateTime time.Time
	Content    string
}
