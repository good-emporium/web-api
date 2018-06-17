package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

type Organization struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// TODO remove test code
var orgs []Organization

func Health(w http.ResponseWriter, _ *http.Request, _ httprouter.Params) {
	w.WriteHeader(http.StatusOK)
}

func GetOrganizations(w http.ResponseWriter, _ *http.Request, _ httprouter.Params) {
	// TODO pull all orgs from db
	json.NewEncoder(w).Encode(orgs)
}

func GetOrganization(w http.ResponseWriter, _ *http.Request, _ httprouter.Params) {
	// TODO pull specific org from db
	//id := ps.ByName("id")
	json.NewEncoder(w).Encode(orgs[0])
}

func main() {
	router := httprouter.New()
	router.GET("/health", Health)
	router.GET("/organizations", GetOrganizations)
	router.GET("/organization/:id", GetOrganization)

	// TODO remove test code
	orgs = append(orgs, Organization{ID: 1, Name: "Test Organization"})

	log.Fatal(http.ListenAndServe(":8080", router))
}
