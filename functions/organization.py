import json
import logging
from datetime import datetime

from functions import OrganizationModel, dynamodb


def ls():
    """Return all of the organizations in the DB."""
    return dynamodb.ls(OrganizationModel)


def _prep_body(body):
    name = body['name'].strip() if 'name' in body else None
    description = body['description'].strip() if 'description' in body else None
    if not _validate_organization(body):
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
def _validate_organization(body):
    return True


def create(body):
    body = _prep_body(body)
    body['created_at'] = datetime.now()
    return dynamodb.create(OrganizationModel, body)


def retrieve(key):
    return dynamodb.retrieve(OrganizationModel, key)


def update(key, body):
    return dynamodb.update(OrganizationModel, key, body)


def delete(key):
    return dynamodb.delete(OrganizationModel, key)
