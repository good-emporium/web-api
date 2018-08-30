import json
from datetime import datetime

from functions import OrganizationModel, dynamodb, utils


def ls():
    """Return all of the organizations in the DB."""
    return dynamodb.ls(OrganizationModel)


def _validate_and_prep(organization):
    fields = (
        'name',
        'description',
        'annual_net_income',
        'net_profit',
        'annual_sales_actual',
        'net_worth',
        'email',
        'address',
        'company_type',
        'duns_number',
        'num_employees_this_site',
        'num_employees_all_sites',
        'one_year_employee_growth',
        'companywebsite',
        'irs_ein',
        'latitude',
        'longitude',
        'location_type',
        'year_of_founding',
        'minority_or_women_owned',
        'phone_number',
        'prescreen_score',
        'primary_industry',
        'primary_naics_code',
        'primary_sic_code',
        'subsidiary_status',
    )

    clean_values = utils.validate_and_prep(organization, fields)

    if 'name' not in clean_values and not clean_values['name']:
        return {'error_message': 'Organization is missing a name'}

    clean_values['id'] = OrganizationModel.get_slug(clean_values['name'])

    return clean_values


def create(body):
    organization = _validate_and_prep(body)
    if 'error_message' in organization:
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': organization['error_message']})
        }

    organization['created_at'] = datetime.now()
    return dynamodb.create(OrganizationModel, organization)


def create_many(body):
    if len(body) > 100:
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'Only 100 organizations can be created at a time'})
        }

    if not isinstance(body, list):
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'This endpoint requires a list of organizations'})
        }

    failed_entries = []
    for organization in body:
        r = create(organization)

        if r['statusCode'] != 201:
            print(r['body'])
            failed_entries.append({
                'organization': organization['name'] if 'name' in organization else '',
                'error_message': r['body']
            })

    if failed_entries:
        return {
            'statusCode': 422,
            'failedEntries': failed_entries,
        }

    return {
        'statusCode': 201
    }


def retrieve(key):
    return dynamodb.retrieve(OrganizationModel, key)


def update(key, body):
    return dynamodb.update(OrganizationModel, key, body)


def delete(key):
    return dynamodb.delete(OrganizationModel, key)
