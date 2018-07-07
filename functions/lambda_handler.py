import json

from functions import auth, organization


def token(event, context):
    """Receives a username and password, and returns a JWT token"""
    username = event['query']['username']
    password = event['query']['password']

    return auth.token(username, password)


def list_organizations(event, context):
    """Returns all of the organizations in the DB."""
    return organization.ls()


def create_organization(event, context):
    body = json.loads(event['body'])
    return organization.create(body)


def replace_organization(event, context):
    body = json.loads(event['body'])
    return organization.replace(body)


def retrieve_organization(event, context):
    org_id = event['path']['id']
    return organization.retrieve(org_id)


def update_organization(event, context):
    org_id = event['path']['id']
    return organization.retrieve(org_id)


def delete_organization(event, context):
    org_id = event['path']['id']
    return organization.delete(org_id)
