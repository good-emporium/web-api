import json

from functions import auth, organization, user, utils


def encode_token(event, context):
    """Receive a username and password, and return a JWT token"""
    username = event['queryStringParameters']['username']
    password = event['queryStringParameters']['password']

    response = auth.encode_token(username, password)
    response = utils.add_cors_headers(response)
    return response


def authorize(event, context):
    response = auth.authenticate_user(event['headers']['Authorization'])
    response = utils.add_cors_headers(response)
    return response


def list_organizations(event, context):
    """Return all of the organizations in the DB."""
    response = organization.ls()
    response = utils.add_cors_headers(response)
    return response


def create_organization(event, context):
    body = json.loads(event['body'])

    response = organization.create(body)
    response = utils.add_cors_headers(response)
    return response


def create_organizations(event, context):
    body = json.loads(event['body'])

    response = organization.create_many(body)
    response = utils.add_cors_headers(response)
    return response


def retrieve_organization(event, context):
    key = event['pathParameters']['id']
    response = organization.retrieve(key)
    response = utils.add_cors_headers(response)
    return response


def update_organization(event, context):
    key = event['pathParameters']['id']
    body = json.loads(event['body'])

    response = organization.update(key, body)
    response = utils.add_cors_headers(response)
    return response


def delete_organization(event, context):
    key = event['pathParameters']['id']

    response = organization.delete(key)
    response = utils.add_cors_headers(response)
    return response


def create_user(event, context):
    body = json.loads(event['body'])

    response = user.create(body)
    response = utils.add_cors_headers(response)
    return response


def change_email(event, context):
    username = event['pathParameters']['username']
    body = json.loads(event['body'])

    response = user.change_email(username, body)
    response = utils.add_cors_headers(response)
    return response
