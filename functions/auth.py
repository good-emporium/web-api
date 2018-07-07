import os
from datetime import datetime, timedelta

import jwt

JWT_ALGORITHM = 'HS256'
JWT_SECRET = os.getenv('JWT_SECRET', 'secret')
JWT_EXP_DELTA_SECONDS = 3600


class AuthenticationError(BaseException):
    pass


# TODO check user info against Users table in DynamoDB
def _authenticate_user(username, password):
    if username == 'test_user' and password == 'abc123':
        return {
            'username': username,
            'first_name': 'Test',
            'last_name': 'User',
        }
    else:
        raise AuthenticationError


def _token_expiration_time():
    return datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)


def encode_token(username, password):
    """Receives a username and password, and returns a JWT token"""
    user = _authenticate_user(username, password)

    claims = {
        **user,
        'exp': _token_expiration_time(),
    }

    return {'token': jwt.encode(claims, JWT_SECRET, JWT_ALGORITHM).decode()}


def decode_token(token):
    claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return claims
