import pytest

from functions import OrganizationModel, organization


ORGANIZATION_TEST_DATA = [{
    # slug: acme-inc
    'name': 'ACME, Inc.',
    'description': 'Apparently, we make a ton of TNT.',
    'annual_net_income': 300000,
    'net_profit': 300000,
    'annual_sales_actual': 300000,
    'net_worth': 300000,
    'email': 'hi@acme.com',
    'address': '6633 E HWY 290, Suite 212 Austin, TX 78723',
    'company_type': 'Non-Public',
    'duns_number': 624031824,
    'num_employees_this_site': 10,
    'num_employees_all_sites': 20,
    'one_year_employee_growth': 0,
    'companywebsite': 'http://acme-inc.com',
    'irs_ein': '54-2767876',
    'latitude': 30.5784,
    'longitude': -97.257423,
    'location_type': 'Single Location',
    'year_of_founding': 2005,
    'minority_or_women_owned': False,
    'phone_number': '543-567-8643',
    'prescreen_score': 'High Risk',
    'primary_industry': 'Social Assistance',
    'primary_naics_code': '624190: Other Individual and Family Services',
    'primary_sic_code': '83220600: General counseling services',
    'subsidiary_status': False,
}, {
    # slug: pals-forever-llc
    'name': 'Pals Forever, LLC',
    'description': 'BFFs for life!',
    'annual_net_income': 500000,
    'net_profit': 500000,
    'annual_sales_actual': 500000,
    'net_worth': 500000,
    'email': 'support@pals-forever.com',
    'address': '1640-A E. 2nd Street Austin, TX 78702',
    'company_type': 'Non-Public',
    'duns_number': 631824,
    'num_employees_this_site': 15,
    'num_employees_all_sites': 30,
    'one_year_employee_growth': 0.24,
    'companywebsite': 'bff.com',
    'irs_ein': '54-2467476',
    'latitude': 30.97358,
    'longitude': -97.2458534,
    'location_type': 'Headquarters',
    'year_of_founding': 1894,
    'minority_or_women_owned': True,
    'phone_number': '502-469-4179',
    'prescreen_score': 'Low Risk',
    'primary_industry': 'Mental Health & Substance Abuse Services',
    'primary_naics_code': '623220: Residential Mental Health and Substance Abuse Facilities',
    'primary_sic_code': '83610302: Mentally handicapped home',
    'subsidiary_status': True,
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

UPDATE_MANY_TEST_DATA = [
    {'id': 'acme-inc', 'properties': {'name': 'Cool Summer Breeze, LLC'}},
    {'id': 'pals-forever-llc', 'properties': {'description': 'sweet-nectar'}},
]


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


def test_create_many_returns_failed_entries(organization_empty_table):
    entries = ORGANIZATION_TEST_DATA + [
        {'no_name_field': 'This should fail'},
        {'no_name_field_two': 'This should also fail'}
    ]
    r = organization.create_many(entries)
    assert r['statusCode'] == 422
    assert len(r['failedEntries']) == 2


@pytest.mark.parametrize('entry', (ORGANIZATION_TEST_DATA[0], 'arbitrary_string'))
def test_create_many_requires_a_list(organization_empty_table, entry):
    assert organization.create_many(entry)['statusCode'] == 422


# def test_update_many(organization_full_table):
#     assert organization.update_many(UPDATE_MANY_TEST_DATA)['statusCode'] == 201
#
#
# @pytest.mark.parametrize('entry', (UPDATE_MANY_TEST_DATA[0], 'arbitrary_string'))
# def test_update_many_requires_a_list(organization_full_table, entry):
#     assert organization.update_many(entry)['statusCode'] == 422


def test_ls(organization_full_table):
    assert organization.ls()['statusCode'] == 200


def test_retrieve(organization_full_table):
    assert organization.retrieve('acme-inc')['statusCode'] == 200


@pytest.mark.parametrize('key,new_body_element', UPDATE_TEST_DATA)
def test_update(organization_full_table, key, new_body_element):
    assert organization.update(key, new_body_element)['statusCode'] == 200


def test_delete(organization_full_table):
    assert organization.delete('acme-inc')['statusCode'] == 204
