package api

import (
	"fingerServer/global"
	"fingerServer/internal/service"
	"fingerServer/pkg/app"
	"fingerServer/pkg/errcode"

	"github.com/gin-gonic/gin"
)

type User struct{}

func NewUser() User {
	return User{}
}
func (u User) Regist(c *gin.Context) {
	param := service.UserRegistRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}
	svc := service.New(c)
	err := svc.UserRegist(&param)
	if err != nil {
		global.Logger.Errorf(c, "svc.UserRegist err: %v", err)
		response.ToErrorResponse(errcode.ErrorUserRegistFail.WithDetails(err.Error()))
		return
	}
	response.ToResponse(global.SuccessStruct)
}
func (u User) Login(c *gin.Context) {
	param := service.UserLoginRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}

	svc := service.New(c)
	err := svc.UserLogin(&param)
	if err != nil {
		global.Logger.Errorf(c, "svc.UserLogin err: %v", err)
		response.ToErrorResponse(errcode.ErrorUserLoginFail.WithDetails(err.Error()))
		return
	}
	response.ToResponse(global.SuccessStruct)
}
func (u User) Authentication(c *gin.Context) {
	param := service.UserAuthenticationRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}

	svc := service.New(c)
	token, err := svc.UserAuthentication(&param)
	if err != nil {
		global.Logger.Errorf(c, "svc.UserAuthentication err: %v", err)
		response.ToErrorResponse(errcode.ErrorUserAuthenticationFail.WithDetails(err.Error()))
		return
	}
	response.ToResponse(gin.H{"token": token})
}
func (u User) ChangePassword(c *gin.Context) {
	param := service.UserChangePasswordRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}

	svc := service.New(c)
	err := svc.ChangePassword(&param)
	if err != nil {
		global.Logger.Errorf(c, "svc.UserChangePassword err: %v", err)
		response.ToErrorResponse(errcode.ErrorUserAdminFail.WithDetails(err.Error()))
		return
	}
	response.ToResponse(global.SuccessStruct)
}

func (u User) Update(c *gin.Context) {
	param := service.UserUpdateRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}
	if len(param.BioCode) != 640 {
		global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
		return
	}
	for _, i := range param.BioCode {
		if i != '0' && i != '1' {
			global.Logger.Errorf(c, "app.BindAndValid errs: %v", errs)
			response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Error()))
			return
		}
	}
	svc := service.New(c)
	err := svc.UserUpdate(&param)
	if err != nil {
		global.Logger.Errorf(c, "svc.UserUpdate err: %v", err)
		response.ToErrorResponse(errcode.ErrorUserUpdateFail.WithDetails(err.Error()))
		return
	}
	response.ToResponse(global.SuccessStruct)
}
