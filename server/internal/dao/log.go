package dao

import (
	"database/sql"
	"fingerServer/internal/model"
	"fmt"
)

type LogUnit struct {
	model.Log
}

func (d Dao) CreateLogByID(userID uint32, content string) error {
	stmtInsert, _ := d.engine.Prepare("insert into logs (user_id,content) values(?,?)")
	defer stmtInsert.Close()
	_, err := stmtInsert.Exec(userID, content)
	if err != nil {
		return err
	}
	return nil
}
func (d Dao) CreateLogByName(userName string, content string) error {
	stmtInsert, _ := d.engine.Prepare("insert into logs (user_id,content) select user_id,? from users where username = ?")
	defer stmtInsert.Close()
	_, err := stmtInsert.Exec(content, userName)
	if err != nil {
		return err
	}
	return nil
}
func (d Dao) GetLogList(userID uint32, page uint32) ([]LogUnit, error) {
	stmtSelect, errT := d.engine.Prepare("select content,createtime from logs where user_id = ? order by log_id desc limit ?,20")
	if errT != nil {
		fmt.Println(errT)
	}

	defer stmtSelect.Close()
	var rows *sql.Rows
	var err error
	rows, err = stmtSelect.Query(userID, page*20)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	res := []LogUnit{}
	for rows.Next() {
		var logUnit LogUnit
		err = rows.Scan(&logUnit.Content, &logUnit.CreateTime)
		if err != nil {
			return nil, err
		}
		res = append(res, logUnit)
	}
	return res, nil
}
