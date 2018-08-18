import json
from datetime import datetime

from functions import UserModel, dynamodb


def _validate_and_prep(user):
    userid = user['id'].strip() if 'id' in user else None
    if not userid:
        return {'error_message': 'Missing the username'}

    display_name = user['display_name'].strip() if 'display_name' in user else None
    email = user['email'].strip() if 'email' in user else None
    bio = user['bio'].strip() if 'bio' in user else None

    return {
        'id': userid,
        'display_name': display_name,
        'email': email,
        'bio': bio,
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


def change_email(key, body):
    # get email from body
    pass

