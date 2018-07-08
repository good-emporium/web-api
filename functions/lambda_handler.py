import json

from functions import auth, organization


def encode_token(event, context):
    """Receive a username and password, and return a JWT token"""
    username = event['query']['username']
    password = event['query']['password']
    return auth.encode_token(username, password)


def authorize(event, context):
    return auth.authenticate_user(event['headers']['Authorization'])


def list_organizations(event, context):
    """Return all of the organizations in the DB."""
    return organization.ls()


def create_organization(event, context):
    body = json.loads(event['body'])
    return organization.create(body)


def retrieve_organization(event, context):
    key = event['path']['id']
    return organization.retrieve(key)


def update_organization(event, context):
    key = event['path']['id']
    body = json.loads(event['body'])
    return organization.update(key, body)


def delete_organization(event, context):
    key = event['path']['id']
    return organization.delete(key)
