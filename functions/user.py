import json
from datetime import datetime

from functions import UserModel, dynamodb, utils, errors


def _validate_and_prep(user):
    fields = [c[0] for c in UserModel.columns]
    clean_values = utils.validate_and_prep(user, fields)

    if 'username' not in clean_values or not clean_values['username']:
        return {'error_message': 'Missing the username'}
    if 'email' not in clean_values or not clean_values['email']:
        return {'error_message': 'Missing the email'}
    return clean_values



def create(body):
    user = _validate_and_prep(body)
    if 'error_message' in user:
        return errors.BaseError(422, user['error_message']).to_dict()
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': user['error_message']})
        }
    except ValueError as e:
        return errors.CreateRecordError(f"Error in creating user: {str(e)}").to_dict()
    except UserModel.DoesNotExist:
        return errors.NotFoundError(f"'{username}' does not exist").to_dict()

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
