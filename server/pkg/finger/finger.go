package finger

import (
	"fingerServer/global"
	"log"
)

func HammingDistance(a, b []byte) bool {
	count := 0
	for i := 0; i < len(b); i++ {
		if a[i] != b[i] {
			count++
		}
	}
	log.Printf("HammingDistance :%d\n", count)
	if count > global.AppSetting.FingerThreshold {
		return false
	}
	return true
}
