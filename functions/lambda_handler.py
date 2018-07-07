import json

from functions import auth, organization


def token(event, context):
    """Receive a username and password, and return a JWT token"""
    username = event['query']['username']
    password = event['query']['password']

    return auth.encode_token(username, password)


def list_organizations(event, context):
    """Return all of the organizations in the DB."""
    return organization.ls()


def create_organization(event, context):
    raw_body = json.loads(event['body'])
    body = {
        'name': raw_body['body']['name'],
        'description': raw_body['body']['name'],
    }
    return organization.create(body)


def replace_organization(event, context):
    raw_body = json.loads(event['body'])
    body = {
        'name': raw_body['body']['name'],
        'description': raw_body['body']['name'],
    }
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
