package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/adamyodinsky/Flock/flock_deployer/controllers"
	"github.com/gorilla/mux"
)

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/", controllers.Health)
	myRouter.HandleFunc("/deploy", controllers.Deploy).Methods("POST")
	log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func main() {
	fmt.Println("Rest API v2.0 - Mux Routers")
	handleRequests()
}
