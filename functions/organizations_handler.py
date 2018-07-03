import json
import logging
from datetime import datetime

from pynamodb.exceptions import DoesNotExist, DeleteError

from functions import OrganizationModel


# TODO add pagination
# TODO return just the columns needed, vs everything
def ls(event, context):
    """Returns all of the organizations in the DB."""

    results = OrganizationModel.scan()

    return {
        'statusCode': 200,
        'body': json.dumps({'items': [dict(result) for result in results]})
    }


def create(event, context):
    data = json.loads(event['body'])

    # TODO add data validation
    # if not validate_organization(data):
    #     logging.error('')
    #     return {
    #         'statusCode': 422,
    #         'body': json.dumps({'error_message': ''})
    #     }

    organization = OrganizationModel(id=OrganizationModel.get_slug(data['name']),
                                     active=True,
                                     name=data['name'],
                                     description=data['description'],
                                     createdAt=datetime.now())
    organization.save()

    return {
        'statusCode': 201
    }


def retrieve(event, context):
    try:
        organization = OrganizationModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Organization not found'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(dict(organization))
    }


def update(event, context):
    data = json.loads(event['body'])

    # TODO add data validation
    # if not validate_organization(data):
    #     logging.error('')
    #     return {
    #         'statusCode': 422,
    #         'body': json.dumps({'error_message': ''})
    #     }

    try:
        organization = OrganizationModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Organization not found'})
        }

    todo_changed = False
    if 'name' in data and data['name'] != organization.name:
        # TODO change the slug. Since it's the hash key, old entry needs to be deleted & a new one created.
        # When recreating, use the original creation date
        organization.name = data['name']
        todo_changed = True
    if 'description' in data and data['description'] != organization.description:
        organization.description = data['description']
        todo_changed = True

    if todo_changed:
        organization.save()
    else:
        logging.info('Nothing changed, not updating')

    return {
        'statusCode': 200
    }


def delete(event, context):
    try:
        organization = OrganizationModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Organization not found'})
        }

    try:
        organization.delete()
    except DeleteError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error_message': 'Unable to delete the organization'})
        }

    return {
        'statusCode': 204
    }
