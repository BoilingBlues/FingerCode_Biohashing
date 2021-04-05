package service

import (
	"errors"
	"fingerServer/internal/dao"
	"fingerServer/pkg/app"
	"fingerServer/pkg/errcode"
	"fmt"

	"github.com/dgrijalva/jwt-go"
)

type LogListRequest struct {
	Token string `josn:"token"`
	Page  uint32 `json:"page"`
}

func (svc *Service) LogList(param *LogListRequest) ([]dao.LogUnit, error) {
	var (
		ecode = errcode.Success
	)
	var claim *app.Claims
	var err error
	if param.Token == "" {
		ecode = errcode.InvalidParams
	} else {
		claim, err = app.ParseToken(param.Token)
		if err != nil {
			switch err.(*jwt.ValidationError).Errors {

			case jwt.ValidationErrorExpired:
				ecode = errcode.UnauthorizedTokenTimeout
			default:
				ecode = errcode.UnauthorizedTokenError
				fmt.Println(err)
			}
		}

	}
	if ecode != errcode.Success {
		return nil, errors.New("鉴权无效")
	}
	userName := claim.AppKey
	userID, err := svc.dao.CheckUser(userName)
	if err != nil {
		return nil, errors.New("内部错误")
	}
	if userID == 0 {
		return nil, errors.New("鉴权失败")
	}
	list, err := svc.dao.GetLogList(userID, param.Page)
	if err != nil {
		return nil, errors.New("内部错误")
	}
	return list, nil
}
