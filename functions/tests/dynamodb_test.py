import pytest
from pynamodb.attributes import BooleanAttribute, NumberAttribute, UnicodeAttribute

from functions import GenericModel, dynamodb


class SupervillainModel(GenericModel):
    class Meta:
        table_name = 'd-supervillains'
        host = 'http://localhost:8000'

    columns = (
        ('id', UnicodeAttribute(hash_key=True)),
        ('active', BooleanAttribute()),
        ('name', UnicodeAttribute()),
        ('powers', UnicodeAttribute(null=True)),
        ('num_minions', NumberAttribute(null=True)),
        ('score', NumberAttribute(null=True)),
    )
    for column in columns:
        locals()[column[0]] = column[1]


SUPERVILLAIN_TEST_DATA = ({
    'id': '37',
    'active': False,
    'name': 'Repo Man',
    'num_minions': 12,
    'score': -160,
}, {
    'id': '42',
    'active': True,
    'name': 'Dr. Horrible',
    'powers': 'Vlogging, looks like Neil Patrick Harris',
})

UPDATE_TEST_DATA = (
    {'active': False},
    {'id': '102'},
)


@pytest.fixture
def supervillain_empty_table():
    if not SupervillainModel.exists():
        SupervillainModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    yield supervillain_empty_table
    SupervillainModel.delete_table()


@pytest.fixture(scope='module')
def supervillain_full_table():
    if not SupervillainModel.exists():
        SupervillainModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    for entry in SUPERVILLAIN_TEST_DATA:
        dynamodb.create(SupervillainModel, entry)
    yield supervillain_full_table
    SupervillainModel.delete_table()


@pytest.mark.parametrize('entry', SUPERVILLAIN_TEST_DATA)
def test_create(supervillain_empty_table, entry):
    assert dynamodb.create(SupervillainModel, entry)['statusCode'] == 201


def test_ls(supervillain_full_table):
    assert dynamodb.ls(SupervillainModel)['statusCode'] == 200


def test_retrieve(supervillain_full_table):
    assert dynamodb.retrieve(SupervillainModel, '37')['statusCode'] == 200


@pytest.mark.parametrize('new_body_element', UPDATE_TEST_DATA)
def test_update(supervillain_full_table, new_body_element):
    assert dynamodb.update(SupervillainModel, '37', new_body_element)['statusCode'] == 200


def test_delete(supervillain_full_table):
    assert dynamodb.delete(SupervillainModel, '42')['statusCode'] == 204
