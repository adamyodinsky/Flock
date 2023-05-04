package controllers

import (
	"fmt"
	"net/http"
)

func Health(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "OK")
	fmt.Println("Endpoint Hit: homePage")
}
