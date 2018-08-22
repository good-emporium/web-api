import pytest

from functions import UserModel, user


USER_TEST_DATA = [{
    'username': 'dash',
    'first_name': 'Dashiel',
    'last_name': 'Lopez Mendez',
    'email': 'dash@ge.com',
    'bio': 'Busy little beaver.',
}, {
    'username': 'jen',
    'first_name': 'Jen',
    'email': 'jen@ge.com',
    'bio': 'New backender!',
}]

UPDATE_TEST_DATA = (
    ('acme-inc', {'name': 'Cool Summer Breeze, LLC'}),
    ('pals-forever-llc', {'id': 'sweet-nectar'}),
)

EMAIL_CHANGE_TEST_DATA = (
    ['dash', {'email': 'beav@ge.com'}],
    ('jen', {'email': 'backender@ge.com'}),
)


@pytest.fixture
def user_empty_table():
    if not UserModel.exists():
        UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    yield user_empty_table
    UserModel.delete_table()


@pytest.fixture(scope='module')
def user_full_table():
    if not UserModel.exists():
        UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    for entry in USER_TEST_DATA:
        user.create(entry)
    yield user_full_table
    UserModel.delete_table()


@pytest.mark.parametrize('entry', USER_TEST_DATA)
def test_create(user_empty_table, entry):
    assert user.create(entry)['statusCode'] == 201


@pytest.mark.parametrize('entry', EMAIL_CHANGE_TEST_DATA)
def test_email_change(user_full_table, entry):
    assert user.change_email(entry[0], entry[1])['statusCode'] == 200


def test_email_change_must_have_a_valid_email_address(user_full_table):
    assert user.change_email('jen', {})['statusCode'] == 422
