from unittest import mock

import jwt
import pytest

from functions import auth

PASSING_TEST_DATA = {
    'username': 'test_user',
    'password': 'abc123',
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlciIsImZpcnN0X25hbWUiOiJUZXN0IiwibGF'
             'zdF9uYW1lIjoiVXNlciIsImV4cCI6MTAwMDAwMDAwfQ.yrCnID2Lu8Olh2sc9MqriLOvdac2WTBrSyn1Ez3ZW6c',
}

FAILING_TEST_DATA = (
    ('non_existent_user', 'abc123'),
    ('test_user', 'this_is_the_wrong_password')
)


# TODO add a fixture (add fake user to DB)
@pytest.mark.parametrize("username,password", FAILING_TEST_DATA)
def test_non_existent_user_raises_exception(username, password):
    with pytest.raises(auth.AuthenticationError):
        auth.encode_token(username, password)


@mock.patch.object(auth, '_token_expiration_time')
def test_get_jwt_token(test_exp_time):
    test_exp_time.return_value = 100000000
    token = auth.encode_token(PASSING_TEST_DATA['username'], PASSING_TEST_DATA['password'])
    assert token == {'token': PASSING_TEST_DATA['token']}


@mock.patch.object(auth, '_token_expiration_time')
def test_decode_token_is_expired(test_exp_time):
    test_exp_time.return_value = 100000000
    with pytest.raises(jwt.ExpiredSignatureError):
        auth.decode_token(PASSING_TEST_DATA['token'].encode())
