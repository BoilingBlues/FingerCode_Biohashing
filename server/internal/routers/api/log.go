package api

import (
	"fingerServer/global"
	"fingerServer/internal/service"
	"fingerServer/pkg/app"
	"fingerServer/pkg/errcode"

	"github.com/gin-gonic/gin"
)

type Log struct{}

func NewLog() Log {
	return Log{}
}
func (l Log) List(c *gin.Context) {
	param := service.LogListRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}

	svc := service.New(c)
	res, err := svc.LogList(&param)
	if err != nil {
		global.Logger.Errorf(c, "svc.ListAll err: %v", err)
		response.ToErrorResponse(errcode.ErrorLogListFail.WithDetails(err.Error()))
		return
	}
	response.ToResponse(gin.H{"list": res})
}
