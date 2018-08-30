import json
from datetime import datetime

from functions import UserModel, dynamodb, utils


def _validate_and_prep(user):
    fields = (
        'username',
        'email',
        'bio',
        'first_name',
        'middle_name',
        'last_name',
        'phone',
        'street_address',
        'city',
        'state',
        'zip_code',
    )

    clean_values = utils.validate_and_prep(user, fields)

    if 'username' not in clean_values and not clean_values['username']:
        return {'error_message': 'Missing the username'}

    if 'email' not in clean_values and not clean_values['email']:
        return {'error_message': 'Missing the email address'}

    return clean_values


def create(body):
    user = _validate_and_prep(body)
    if 'error_message' in user:
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': user['error_message']})
        }

    user['created_at'] = datetime.now()
    return dynamodb.create(UserModel, user)


def retrieve(key):
    return dynamodb.retrieve(UserModel, key)


def update(key, body):
    return dynamodb.update(UserModel, key, body)


def delete(key):
    return dynamodb.delete(UserModel, key)


def change_email(username, body):
    email = body['email'] if 'email' in body else None
    if not email:
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'Email needs to be included'})
        }

    return dynamodb.update(UserModel, username, body)
