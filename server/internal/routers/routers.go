package routers

import (
	"fingerServer/global"
	"fingerServer/internal/middleware"
	"fingerServer/internal/routers/api"

	"github.com/gin-gonic/gin"
)

func NewRouter() *gin.Engine {
	r := gin.New()
	if global.ServerSetting.RunMode == "debug" {
		r.Use(gin.Logger())
		r.Use(gin.Recovery())
	}
	r.Use(middleware.Tracing())

	user := api.NewUser()
	logs := api.NewLog()

	r.POST("/regist", user.Regist)
	r.POST("/login", user.Login)
	r.POST("/changePassword", user.ChangePassword)
	api := r.Group("/api")
	{
		api.POST("/update", user.Update)
		api.POST("/authentication", user.Authentication)

		api.POST("/logs", logs.List)
	}
	return r
}
