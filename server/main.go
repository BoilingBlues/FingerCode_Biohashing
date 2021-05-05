package main

import (
	"context"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"fingerServer/global"
	"fingerServer/internal/model"
	"fingerServer/internal/routers"
	"fingerServer/pkg/logger"
	"fingerServer/pkg/setting"
	"fingerServer/pkg/tracer"

	"github.com/gin-gonic/gin"
	"gopkg.in/natefinch/lumberjack.v2"
)

func Init() {
	err := setupSetting()
	if err != nil {
		log.Fatalf("init.SetupSetting err : %v", err)
	}
	err = setupDBEngine()
	if err != nil {
		log.Fatalf("init.setupDBEngine err : %v", err)
	}
	err = setupLogger()
	if err != nil {
		log.Fatalf("init.setupLogger err : %v", err)
	}
	err = setupTracer()
	if err != nil {
		log.Fatalf("init.setupTracer err : %v", err)
	}
}

func main() {
	Init()
	gin.SetMode(global.ServerSetting.RunMode)
	router := routers.NewRouter()
	s := &http.Server{
		Addr:           ":" + global.ServerSetting.HttpPort,
		Handler:        router,
		ReadTimeout:    global.ServerSetting.ReadTimeout,
		WriteTimeout:   global.ServerSetting.WriteTimeout,
		MaxHeaderBytes: 1 << 20,
	}
	go func() {
		if err := s.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("s.ListenAndServe err: %v", err)
		}
	}()

	//下面是运行退出，不重要
	quit := make(chan os.Signal)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("shutting down server ... ")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := s.Shutdown(ctx); err != nil {
		log.Fatal("server forced to shutdown:", err)
	}

	log.Println("Server exiting")
}

func setupSetting() error {
	s, err := setting.NewSetting("configs")
	if err != nil {
		return err
	}
	err = s.ReadSection("Server", &global.ServerSetting)
	if err != nil {
		return err
	}
	err = s.ReadSection("JWT", &global.JWTSetting)
	if err != nil {
		return err
	}
	err = s.ReadSection("JWT-t", &global.JWTSetting)
	if err != nil {
		return err
	}
	err = s.ReadSection("JWT", &global.JWTSetting)
	if err != nil {
		return err
	}
	err = s.ReadSection("Database", &global.DatabaseSetting)
	if err != nil {
		return err
	}
	err = s.ReadSection("App", &global.AppSetting)
	global.JWTSetting.Expire *= time.Second
	global.ServerSetting.ReadTimeout *= time.Second
	global.ServerSetting.WriteTimeout *= time.Second
	return nil
}

func setupLogger() error {
	fileName := global.AppSetting.LogSavePath + "/" + global.AppSetting.LogFileName + global.AppSetting.LogFileExt
	global.Logger = logger.NewLogger(&lumberjack.Logger{
		Filename:  fileName,
		MaxSize:   500,
		MaxAge:    10,
		LocalTime: true,
	}, "", log.LstdFlags).WithCaller(2)
	return nil
}
func setupDBEngine() error {
	var err error
	global.DBEngine, err = model.NewDBEngine(global.DatabaseSetting)
	if err != nil {
		return err
	}
	file, err := ioutil.ReadFile("docs/sql/tables.sql")
	if err != nil {
		return err
	}
	sqlStr := strings.Replace(string(file), "\n", "", -1)
	sqlStr = strings.Replace(sqlStr, "\r", "", -1)
	sqlStr = strings.Replace(sqlStr, "	", "", -1)
	requests := strings.Split(sqlStr, ";")

	for _, request := range requests[:len(requests)-1] {
		_, err := global.DBEngine.Exec(request)
		if err != nil {
			return err
		}
	}
	return nil
}

func setupTracer() error {
	jaegerTracer, _, err := tracer.NewJaegerTracer("blog-service", "127.0.0.1:6831")
	if err != nil {
		return err
	}
	global.Tracer = jaegerTracer
	return nil
}
