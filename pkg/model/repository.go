package model

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/satori/go.uuid"
)

type ClientRepository struct {
	Conn *dynamodb.DynamoDB
}

func (repository *ClientRepository) Store(organization *Organization) error {
	id := uuid.NewV4()
	organization.ID = id.String()
	av, err := dynamodbattribute.MarshalMap(organization)
	if err != nil {
		return err
	}
	input := &dynamodb.PutItemInput{
		Item:      av,
		TableName: aws.String("Organizations"),
	}
	_, err = repository.Conn.PutItem(input)
	if err != nil {
		return err
	}
	return err
}

func (repository *ClientRepository) Fetch(key string) (*Organization, error) {
	var organization *Organization
	result, err := repository.Conn.GetItem(&dynamodb.GetItemInput{
		TableName: aws.String("Organizations"),
		Key: map[string]*dynamodb.AttributeValue{
			"ID": {
				S: aws.String(key),
			},
		},
	})
	if err != nil {
		return nil, err
	}
	if err := dynamodbattribute.UnmarshalMap(result.Item, &organization); err != nil {
		return nil, err
	}
	return organization, nil
}
