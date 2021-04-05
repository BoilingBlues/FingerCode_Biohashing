package global

import (
	"fingerServer/pkg/logger"
	"fingerServer/pkg/setting"

	"github.com/gin-gonic/gin"
)

var (
	ServerSetting   *setting.ServerSettingS
	JWTSetting      *setting.JWTSettingS
	DatabaseSetting *setting.DatabaseSettingS
	AppSetting      *setting.AppSettingS
	Logger          *logger.Logger
)
var SuccessStruct = gin.H{"code": 00000000, "msg": "success"}
