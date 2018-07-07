import pytest

from functions import auth


# TODO add fixture + check a non-existent user
def test_nonexistent_user_raises_exception():
    pass


# TODO with a fixture, test against a fake user adn check that a string is returned
def test_get_jwt_token():
    assert auth.token('username', 'password') == 'jwt_token'
