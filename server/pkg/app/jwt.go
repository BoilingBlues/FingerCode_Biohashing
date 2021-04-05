package app

import (
	"fingerServer/global"
	"time"

	"github.com/dgrijalva/jwt-go"
)

type Claims struct {
	AppKey string `json:"app_key"`
	jwt.StandardClaims
}

func GetJWTSecret() []byte {
	return []byte(global.JWTSetting.Secret)
}

// func GetJWTTSecret() []byte {
// 	return []byte(global.JWTTSetting.Secret)
// }

func GenerateToken(appKey string) (string, error) {
	nowTime := time.Now()
	expireTime := nowTime.Add(global.JWTSetting.Expire)
	claims := Claims{
		AppKey: appKey,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expireTime.Unix(),
			Issuer:    global.JWTSetting.Issuer,
		},
	}

	tokenClaims := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	token, err := tokenClaims.SignedString(GetJWTSecret())
	return token, err
}

func ParseToken(token string) (*Claims, error) {
	tokenClaims, err := jwt.ParseWithClaims(token, &Claims{}, func(token *jwt.Token) (interface{}, error) {
		return GetJWTSecret(), nil
	})
	if err != nil {
		return nil, err
	}
	if tokenClaims != nil {
		claims, ok := tokenClaims.Claims.(*Claims)
		if ok && tokenClaims.Valid {
			return claims, nil
		}
	}

	return nil, err
}

// func GenerateTokenT(appKey string) (string, error) {
// 	nowTime := time.Now()
// 	expireTime := nowTime.Add(global.JWTTSetting.Expire)
// 	claims := Claims{
// 		AppKey: appKey,
// 		StandardClaims: jwt.StandardClaims{
// 			ExpiresAt: expireTime.Unix(),
// 			Issuer:    global.JWTTSetting.Issuer,
// 		},
// 	}

// 	tokenClaims := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
// 	token, err := tokenClaims.SignedString(GetJWTTSecret())
// 	return token, err
// }

// func ParseTokenT(token string) (*Claims, error) {
// 	tokenClaims, err := jwt.ParseWithClaims(token, &Claims{}, func(token *jwt.Token) (interface{}, error) {
// 		return GetJWTTSecret(), nil
// 	})
// 	if err != nil {
// 		return nil, err
// 	}
// 	if tokenClaims != nil {
// 		claims, ok := tokenClaims.Claims.(*Claims)
// 		if ok && tokenClaims.Valid {
// 			return claims, nil
// 		}
// 	}

// 	return nil, err
// }
