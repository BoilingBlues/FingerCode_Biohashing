package model

import (
	"database/sql"
	"fingerServer/pkg/setting"
	"fmt"

	_ "github.com/go-sql-driver/mysql" // 调用mysql数据库驱动
)

//NewDBEngine 新建数据库引擎
func NewDBEngine(databaseSetting *setting.DatabaseSettingS) (*sql.DB, error) {
	connectString := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=%s&parseTime=%t&loc=Local",
		databaseSetting.UserName,
		databaseSetting.Password,
		databaseSetting.Host,
		databaseSetting.DBName,
		databaseSetting.Charset,
		databaseSetting.ParseTime,
	)
	db, err := sql.Open(databaseSetting.DBType, connectString)
	if err != nil {
		return nil, err
	}
	return db, nil
}
