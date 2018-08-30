import pytest

from functions import utils

# SLUG_TEST_DATA = (
#     ('My Cool Company', 'my-cool-company'),
#     ('Tall Castles, Inc.', 'tall-castles-inc'),
#     ('Oohs-n-Ahhs,LLC', 'oohs-n-ahhs-llc'),
# )
#
# UPDATE_TEST_DATA = (
#     ('acme-inc', {'name': 'Cool Summer Breeze, LLC'}),
#     ('pals-forever-llc', {'id': 'sweet-nectar'}),
# )
#
#
# @pytest.mark.parametrize('key,new_body_element', UPDATE_TEST_DATA)
# def test_get_value(organization_full_table, key, new_body_element):
#     assert utils.get_value(key, new_body_element)['statusCode'] == 200
#
#
# def test_validate_and_prep(organization_full_table):
#     assert utils.validate_and_prep('acme-inc')['statusCode'] == 204


# def get_value(raw_data, field):
#     try:
#         raw_data[field] = raw_data[field].strip()
#     finally:
#         return raw_data[field] if field in raw_data else None
#
#
# def validate_and_prep(raw_data, fields):
#     clean_values = {}
#     for field in fields:
#         value = get_value(raw_data, field)
#         if value:
#             clean_values[field] = value
#     return clean_values
