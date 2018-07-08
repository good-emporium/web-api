import pytest

from functions import OrganizationModel, organization

TEST_DATA = [
    {
        'name': 'ACME, Inc.',
        'description': 'Apparently, we make a ton of TNT.',
    },
    {
        'name': 'Pals Forever, LLC',
        'description': 'BFFs for life!',
    },
]

SLUG_TEST_DATA = (
    ('My Cool Company', 'my-cool-company'),
    ('Tall Castles, Inc.', 'tall-castles-inc'),
    ('Oohs-n-Ahhs,LLC', 'oohs-n-ahhs-llc')
)


@pytest.mark.parametrize("formal_name,expected", SLUG_TEST_DATA)
def test_slug_generation(formal_name, expected):
    assert OrganizationModel.get_slug(formal_name) == expected


def test_create():
    pass
