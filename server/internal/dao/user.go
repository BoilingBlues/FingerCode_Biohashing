package dao

import (
	"database/sql"
	"fingerServer/internal/model"
	"fmt"
)

func (d Dao) CheckUser(username string) (uint32, error) {
	stmtSelect, errT := d.engine.Prepare("select user_id from users where username = ?")
	if errT != nil {
		fmt.Println(errT)
	}
	defer stmtSelect.Close()
	row := stmtSelect.QueryRow(username)
	var userID uint32
	err := row.Scan(&userID)
	if err != nil {
		if err == sql.ErrNoRows {
			return 0, nil
		}
		return 0, err
	}
	return userID, nil
}

func (d Dao) CreateUser(user *model.User) error {
	stmtInsert, _ := d.engine.Prepare("insert into users(username,password) values (?,?)")
	defer stmtInsert.Close()
	_, err := stmtInsert.Exec(user.UserName, user.Password)
	if err != nil {
		return err
	}
	return nil
}
func (d Dao) CheckUserAdmin(user *model.User) (uint32, error) {
	stmtSelect, _ := d.engine.Prepare("select user_id from users where username = ? and password = ?")
	defer stmtSelect.Close()
	row := stmtSelect.QueryRow(user.UserName, user.Password)
	var userID uint32
	err := row.Scan(&userID)
	if err != nil {
		if err == sql.ErrNoRows {
			return 0, nil
		}
		return 0, err
	}
	return userID, nil
}
func (d Dao) CheckUserBioCode(username string) (string, error) {
	stmtSelect, _ := d.engine.Prepare("select biocode from users where username = ?")
	defer stmtSelect.Close()
	row := stmtSelect.QueryRow(username)
	var biocode string
	err := row.Scan(&biocode)
	if err != nil {
		if err == sql.ErrNoRows {
			return "", nil
		}
		return "", err
	}
	return biocode, nil
}

func (d Dao) UpdatePassword(userID uint32, password string) error {
	stmtUpdate, _ := d.engine.Prepare("update users set password = ? where user_id = ?")
	defer stmtUpdate.Close()
	_, err := stmtUpdate.Exec(password, userID)
	if err != nil {
		return err
	}
	return nil
}

func (d Dao) UpdateBioCode(userID uint32, BioCode string) error {
	stmtUpdate, _ := d.engine.Prepare("update users set biocode = ? where user_id = ?")
	defer stmtUpdate.Close()
	_, err := stmtUpdate.Exec(BioCode, userID)
	if err != nil {
		return err
	}
	return nil
}
