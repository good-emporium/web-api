import pytest

from functions import OrganizationModel, organization, search


ORGANIZATION_TEST_DATA = [{
    'id': 'acme-inc',
    'name': 'ACME, Inc.',
    'description': 'Apparently, we make a ton of TNT.',
}, {
    'id': 'pals-forever-llc',
    'name': 'Pals Forever, LLC',
    'description': 'BFFs for life!',
}, {
    'id': 'better-life-for-cats',
    'name': 'Better Life for Cats',
    'description': 'BFFs for life!',
}]

SEARCH_TEST_DATA = (
    ('acme', [ORGANIZATION_TEST_DATA[0]]),
    ('tnt ton', [ORGANIZATION_TEST_DATA[0]]),
    ('life', ORGANIZATION_TEST_DATA[1:]),
)


@pytest.fixture(scope='module')
def organization_full_table():
    if not OrganizationModel.exists():
        OrganizationModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    for entry in ORGANIZATION_TEST_DATA:
        organization.create(entry)
    yield organization_full_table
    OrganizationModel.delete_table()


@pytest.mark.parametrize('terms,expected_results', SEARCH_TEST_DATA)
def test_search(organization_full_table, terms, expected_results):
    assert search.query(terms)['results'] == expected_results
