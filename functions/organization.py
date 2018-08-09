import json
import logging
from datetime import datetime

from functions import OrganizationModel, dynamodb


def ls():
    """Return all of the organizations in the DB."""
    return dynamodb.ls(OrganizationModel)


def _prep(organization):
    name = organization['name'].strip() if 'name' in organization else None
    description = organization['description'].strip() if 'description' in organization else None
    if not _validate(organization):
        logging.error(f"'{name}' didn't pass validation")
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': f"'{name}' didn't pass validation"})
        }

    return {
        'id': OrganizationModel.get_slug(name),
        'name': name,
        'description': description
    }


# TODO add validation
def _validate(organization):
    return True


def create(body):
    organization = _prep(body)
    organization['created_at'] = datetime.now()
    return dynamodb.create(OrganizationModel, organization)


def create_many(body):
    if len(body) > 100:
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'Only 100 organizations can be created at a time'})
        }

    if not isinstance(body, list):
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'This endpoint requires a list of organizations'})
        }

    for organization in body:
        organization = _prep(organization)
        organization['created_at'] = datetime.now()
        r = dynamodb.create(OrganizationModel, organization)

        if r['statusCode'] != 201:
            return r

    return {
        'statusCode': 201
    }


def retrieve(key):
    return dynamodb.retrieve(OrganizationModel, key)


def update(key, body):
    return dynamodb.update(OrganizationModel, key, body)


def delete(key):
    return dynamodb.delete(OrganizationModel, key)
