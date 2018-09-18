import os
import re
from datetime import datetime

from pynamodb.attributes import BooleanAttribute, NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute, \
    UnicodeSetAttribute
from pynamodb.models import Model


class GenericModel(Model):
    created_at = UTCDateTimeAttribute(default=datetime.now())
    updated_at = UTCDateTimeAttribute()

    # TODO add a try/except here and return the error (rather than fail)
    def save(self, condition=None, conditional_operator=None, **expected_values):
        self.updated_at = datetime.now()
        super(GenericModel, self).save()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))


class GenericMeta:
    env = os.getenv('CLOUD_ENV')
    if env:
        region = os.getenv('CLOUD_REGION')
        host = f'https://dynamodb.{region}.amazonaws.com'
    else:
        host = 'http://localhost:8000'


class OrganizationModel(GenericModel):
    class Meta(GenericMeta):
        table_name = os.getenv('TABLE_ORGANIZATIONS', 'd-organizations')
        
    columns = (
        ('id', UnicodeAttribute(hash_key=True)),
        # ('active', BooleanAttribute()),
        ('name', UnicodeAttribute()),
        ('classification', UnicodeAttribute(null=True)),
        ('logo', UnicodeAttribute(null=True)),
        ('description', UnicodeAttribute(null=True)),
        ('motto', UnicodeAttribute(null=True)),
        ('mission_statement', UnicodeAttribute(null=True)),
        ('founded', UnicodeAttribute(null=True)),
        ('ceo', UnicodeAttribute(null=True)),
        ('annual_net_income', NumberAttribute(null=True)),
        ('net_profit', NumberAttribute(null=True)),
        ('annual_sales_actual', NumberAttribute(null=True)),
        ('net_worth', NumberAttribute(null=True)),
        ('email', UnicodeAttribute()),
        ('address', UnicodeAttribute(null=True)),
        ('company_type', UnicodeAttribute(null=True)),
        ('duns_number', NumberAttribute(null=True)),
        ('num_employees_this_site', NumberAttribute(null=True)),
        ('num_employees_all_sites', NumberAttribute(null=True)),
        ('one_year_employee_growth', NumberAttribute(null=True)),
        ('company_website', UnicodeAttribute(null=True)),
        ('irs_ein', UnicodeAttribute(null=True)),
        ('latitude', NumberAttribute(null=True)),
        ('longitude', NumberAttribute(null=True)),
        ('location_type', UnicodeAttribute(null=True)),
        ('year_of_founding', NumberAttribute(null=True)),
        ('minority_or_women_owned', BooleanAttribute(null=True)),
        ('phone_number', UnicodeAttribute(null=True)),
        ('prescreen_score', UnicodeAttribute(null=True)),
        ('primary_industry', UnicodeAttribute(null=True)),
        ('primary_naics_code', UnicodeAttribute(null=True)),
        ('primary_sic_code', UnicodeAttribute(null=True)),
        ('subsidiary_status', BooleanAttribute(null=True)),
        ('tags', UnicodeSetAttribute(null=True)),
        ('examples', UnicodeSetAttribute(null=True)),
        ('sdg_keys', UnicodeSetAttribute(null=True)),
        ('similar_companies', UnicodeSetAttribute(null=True)),
    )
    for column in columns:
        locals()[column[0]] = column[1]

    @staticmethod
    def get_slug(name):
        """
        The slug is a URL-friendly identifier for an organization.

        Converts 'My Cool Company' into 'my-cool-company'
        """
        name = name.lower()
        name = re.sub(r'[\W_]$', '', name)
        return re.sub(r'[\W_]+', '-', name)


class UserModel(GenericModel):
    class Meta(GenericMeta):
        table_name = os.getenv('TABLE_USERS', 'd-users')

    columns = (
        ('username', UnicodeAttribute(hash_key=True)),
        ('active', BooleanAttribute(null=True)),
        ('first_name', UnicodeAttribute(null=True)),
        ('middle_name', UnicodeAttribute(null=True)),
        ('last_name', UnicodeAttribute(null=True)),
        ('email', UnicodeAttribute()),
        ('bio', UnicodeAttribute(null=True)),
        ('phone', UnicodeAttribute(null=True)),
        ('street_address', UnicodeAttribute(null=True)),
        ('city', UnicodeAttribute(null=True)),
        ('state', UnicodeAttribute(null=True)),
        ('zip_code', UnicodeAttribute(null=True)),
        ('user_roles', UnicodeSetAttribute(null=True)),
    )
    for column in columns:
        locals()[column[0]] = column[1]
