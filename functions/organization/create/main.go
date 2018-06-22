package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"

	"github.com/good-emporium/web-api/pkg/datastore"
	"github.com/good-emporium/web-api/pkg/helpers"
	"github.com/good-emporium/web-api/pkg/model"
)

type repository interface {
	Store(*model.Organization) error
}

type handler struct {
	repository
}

// Handler is our lambda handler
func (h handler) Handler(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	var organization *model.Organization
	// Marshal request bodt into our client model
	if err := json.Unmarshal([]byte(request.Body), &organization); err != nil {
		return helpers.ErrResponse(err, http.StatusInternalServerError)
	}

	// Call our repository and store our client
	if err := h.repository.Store(organization); err != nil {
		return helpers.ErrResponse(err, http.StatusInternalServerError)
	}

	// Return a success response
	return helpers.Response(map[string]bool{
		"success": true,
	}, http.StatusCreated)
}

func main() {
	conn, err := datastore.CreateConnection(os.Getenv("REGION"))
	if err != nil {
		log.Panic(err)
	}
	repository := &model.ClientRepository{Conn: conn}
	h := handler{repository}
	lambda.Start(h.Handler)
}
