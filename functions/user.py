import json
from datetime import datetime

from functions import UserModel, dynamodb, utils


def _validate_and_prep(user):
    username = user['username'].strip() if 'username' in user else None
    email = user['email'].strip() if 'email' in user else None
    if not username:
        return {'error_message': 'Missing the username'}
    if not email:
        return {'error_message': 'Missing the email address'}

    email = user['email'].strip() if 'email' in user else None
    bio = user['bio'].strip() if 'bio' in user else None
    first_name = user['first_name'].strip() if 'first_name' in user else None
    middle_name = user['middle_name'].strip() if 'middle_name' in user else None
    last_name = user['last_name'].strip() if 'last_name' in user else None
    phone = user['phone_number'].strip() if 'phone_number' in user else None
    street_address = user['street_address'].strip() if 'street_address' in user else None
    city = user['city'].strip() if 'city' in user else None
    state = user['state'].strip() if 'state' in user else None
    zip_code = user['zip_code'].strip() if 'zip_code' in user else None

    return {
        'username': username,
        'email': email,
        'bio': bio,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'phone': phone,
        'street_address': street_address,
        'city': city,
        'state': state,
        'zip_code': zip_code,
    }


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
    pass


def update(key, body):
    pass


def delete(key):
    pass


def change_email(username, body):
    email = body['email'] if 'email' in body else None
    if not email:
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'Email needs to be included'})
        }

    return dynamodb.update(UserModel, username, body)
