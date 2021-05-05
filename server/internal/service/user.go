package service

import (
	"errors"

	"fingerServer/internal/model"

	"fingerServer/pkg/app"
	"fingerServer/pkg/finger"
)

type UserLoginRequest struct {
	UserName string `json:"username" validate:"required"`
}

type UserRegistRequest struct {
	UserName string `json:"username" validate:"required"`
	Password string `json:"password" validate:"required"`
}

type UserAuthenticationRequest struct {
	UserName string `json:"username" validate:"required"`
	BioCode  string `json:"biocode" validate:"required,len=640"`
}

type UserChangePasswordRequest struct {
	UserName    string `json:"username" validate:"required"`
	Password    string `json:"password" validate:"required"`
	NewPassword string `json:"newpassword" validate:"required"`
}

type UserUpdateRequest struct {
	UserName string `json:"username"`
	Password string `json:"password"`
	BioCode  string `json:"biocode"`
}

func (svc *Service) UserLogin(param *UserLoginRequest) error {
	userID, err := svc.dao.CheckUser(param.UserName)
	if err != nil {
		return errors.New("内部错误")
	}
	if userID != 0 {
		return nil
	}
	return errors.New("用户不存在")
}
func (svc *Service) UserRegist(param *UserRegistRequest) error {
	userID, _ := svc.dao.CheckUser(param.UserName)
	if userID != 0 {
		return errors.New("用户名重复")
	}
	user := &model.User{
		UserName: param.UserName,
		Password: param.Password,
	}
	err := svc.dao.CreateUser(user)
	if err != nil {
		return errors.New("内部错误")
	}
	svc.dao.CreateLogByName(param.UserName, "用户注册")
	return nil
}

func (svc *Service) UserAuthentication(param *UserAuthenticationRequest) (string, error) {
	b1 := []byte(param.BioCode)
	if len(b1) != 640 {
		return "", errors.New("指纹较验失败")
	}
	b2, err := svc.dao.CheckUserBioCode(param.UserName)
	if err != nil {
		return "", errors.New("内部错误")
	}
	if b2 == "" {
		return "", errors.New("用户没有注册指纹")
	}
	b := []byte(b2)
	result := finger.HammingDistance(b, b1)
	if !result {
		svc.dao.CreateLogByName(param.UserName, "认证失败")
		return "", errors.New("指纹校验失败")
	}
	svc.dao.CreateLogByName(param.UserName, "认证成功")
	jwt, _ := app.GenerateToken(param.UserName)
	return jwt, nil
}
func (svc *Service) UserUpdate(param *UserUpdateRequest) error {
	user := &model.User{
		UserName: param.UserName,
		Password: param.Password,
	}
	userID, err := svc.dao.CheckUserAdmin(user)
	if err != nil {
		return errors.New("内部错误")
	}
	if userID == 0 {
		return errors.New("用户名或密码错误")
	}
	err = svc.dao.UpdateBioCode(userID, param.BioCode)
	if err != nil {
		return errors.New("内部错误")
	}
	svc.dao.CreateLogByID(userID, "修改指纹")
	return nil
}

func (svc *Service) ChangePassword(param *UserChangePasswordRequest) error {
	user := &model.User{
		UserName: param.UserName,
		Password: param.Password,
	}
	userID, err := svc.dao.CheckUserAdmin(user)
	if err != nil {
		return errors.New("内部错误")
	}
	if userID == 0 {
		return errors.New("用户名或密码错误")
	}
	err = svc.dao.UpdatePassword(userID, param.NewPassword)
	if err != nil {
		return errors.New("内部错误")
	}
	svc.dao.CreateLogByID(userID, "修改密码")
	return nil
}
