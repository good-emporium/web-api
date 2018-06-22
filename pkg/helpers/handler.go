package helpers

import (
	"encoding/json"

	"github.com/aws/aws-lambda-go/events"
)

func Response(data interface{}, code int) (events.APIGatewayProxyResponse, error) {
	body, _ := json.Marshal(data)
	return events.APIGatewayProxyResponse{
		Body:       string(body),
		StatusCode: code,
	}, nil
}

func ErrResponse(err error, code int) (events.APIGatewayProxyResponse, error) {
	data := map[string]string{
		"err": err.Error(),
	}
	body, _ := json.Marshal(data)
	return events.APIGatewayProxyResponse{
		Body:       string(body),
		StatusCode: code,
	}, err
}
