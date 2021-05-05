package main

import (
	"fingerServer/pkg/app"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"testing"
)

var num int
var wg sync.WaitGroup
var Token string
var url = "http://47.102.198.54:8080"

func getToken() {
	setupSetting()
	token, err := app.GenerateToken("langge12")
	if err != nil {
		fmt.Printf("Token generate failed: %v", err)
	}
	Token = token
}
func TestLog(t *testing.T) {
	getToken()
	PostLog()
}

func PostLog() {
	_, err := http.Post(url+"/api/logs", "application/json", strings.NewReader(`{"token":"`+Token+`","page":1}`))
	if err != nil {
		num++
	}

	wg.Done()
}
func BenchmarkSprintf(b *testing.B) {
	getToken()
	b.ResetTimer()
	for i := 0; i < 5000; i++ {
		wg.Add(1)
		go PostTest()
	}
	wg.Wait()
	fmt.Println(num)
}
func PostLogin() {
	_, err := http.Post(url+"/api/logs", "application/json", strings.NewReader(`{"username":"langge"}`))
	if err != nil {
		num++
	}

	wg.Done()
}
func PostTest() {
	_, err := http.Get(url + "/api/test")
	if err != nil {
		num++
	}

	wg.Done()
}
func GetTest() {
	_, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		num++
	}
	wg.Done()
}
