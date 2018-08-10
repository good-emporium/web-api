import pytest

from functions import OrganizationModel, organization


ORGANIZATION_TEST_DATA = [{
    # slug: acme-inc
    'name': 'ACME, Inc.',
    'description': 'Apparently, we make a ton of TNT.',
}, {
    # slug: pals-forever-llc
    'name': 'Pals Forever, LLC',
    'description': 'BFFs for life!',
}]

SLUG_TEST_DATA = (
    ('My Cool Company', 'my-cool-company'),
    ('Tall Castles, Inc.', 'tall-castles-inc'),
    ('Oohs-n-Ahhs,LLC', 'oohs-n-ahhs-llc'),
)

UPDATE_TEST_DATA = (
    ('acme-inc', {'name': 'Cool Summer Breeze, LLC'}),
    ('pals-forever-llc', {'id': 'sweet-nectar'}),
)


@pytest.mark.parametrize('formal_name,expected', SLUG_TEST_DATA)
def test_slug_generation(formal_name, expected):
    assert OrganizationModel.get_slug(formal_name) == expected


@pytest.fixture
def organization_empty_table():
    if not OrganizationModel.exists():
        OrganizationModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    yield organization_empty_table
    OrganizationModel.delete_table()


@pytest.fixture(scope='module')
def organization_full_table():
    if not OrganizationModel.exists():
        OrganizationModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    for entry in ORGANIZATION_TEST_DATA:
        organization.create(entry)
    yield organization_full_table
    OrganizationModel.delete_table()


@pytest.mark.parametrize('entry', ORGANIZATION_TEST_DATA)
def test_create(organization_empty_table, entry):
    assert organization.create(entry)['statusCode'] == 201


def test_create_many(organization_empty_table):
    assert organization.create_many(ORGANIZATION_TEST_DATA)['statusCode'] == 201


@pytest.mark.parametrize('entry', (ORGANIZATION_TEST_DATA[0], 'arbitrary_string'))
def test_create_many_requires_a_list(organization_empty_table, entry):
    assert organization.create_many(entry)['statusCode'] == 422


def test_ls(organization_full_table):
    assert organization.ls()['statusCode'] == 200


def test_retrieve(organization_full_table):
    assert organization.retrieve('acme-inc')['statusCode'] == 200


@pytest.mark.parametrize('key,new_body_element', UPDATE_TEST_DATA)
def test_update(organization_full_table, key, new_body_element):
    assert organization.update(key, new_body_element)['statusCode'] == 200


def test_delete(organization_full_table):
    assert organization.delete('acme-inc')['statusCode'] == 204
