package main

import (
	"net/http"
	"testing"

	"github.com/good-emporium/web-api/pkg/model"
	"github.com/aws/aws-lambda-go/events"
	"github.com/stretchr/testify/assert"
)

type fakeRepo struct{}

func (repo fakeRepo) Store(*model.Organization) error {
	return nil
}

func TestCanStoreClient(t *testing.T) {
	request := events.APIGatewayProxyRequest{
		Body: `{"name": "Save Puppies, inc.", "description": "Saving the world, one puppy at a time."}`,
	}
	h := &handler{fakeRepo{}}
	response, err := h.Handler(request)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusCreated, response.StatusCode)
}
