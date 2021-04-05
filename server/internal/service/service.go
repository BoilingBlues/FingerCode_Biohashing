package service

import (
	"context"
	"fingerServer/global"
	"fingerServer/internal/dao"

	"github.com/gin-gonic/gin"
)

type Service struct {
	ctx context.Context
	dao *dao.Dao
	c   *gin.Context
}

func New(c *gin.Context) Service {
	svc := Service{
		ctx: c.Request.Context(),
		c:   c,
	}
	svc.dao = dao.New(global.DBEngine)
	return svc
}
