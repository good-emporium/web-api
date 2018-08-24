import os
import re
from datetime import datetime

from pynamodb.attributes import BooleanAttribute, NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute, UnicodeSetAttribute
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
        ('description', UnicodeAttribute()),
        ('annual_net_income', NumberAttribute()),
        ('net_profit', NumberAttribute()),
        ('annual_sales_actual', NumberAttribute()),
        ('net_worth', NumberAttribute()),
        ('email', UnicodeAttribute()),
        ('address', UnicodeAttribute()),
        ('company_type', UnicodeAttribute()),
        ('duns_number', NumberAttribute()),
        ('num_employees_this_site', NumberAttribute()),
        ('num_employees_all_sites', NumberAttribute()),
        ('one_year_employee_growth', UnicodeAttribute()),
        ('companywebsite', UnicodeAttribute()),
        ('irs_ein', UnicodeAttribute()),
        ('latitude', NumberAttribute()),
        ('longitude', NumberAttribute()),
        ('location_type', UnicodeAttribute()),
        ('year_of_founding', NumberAttribute()),
        ('minority_or_women_owned', BooleanAttribute()),
        ('phone_number', UnicodeAttribute()),
        ('prescreen_score', UnicodeAttribute()),
        ('primary_industry', UnicodeAttribute()),
        ('primary_naics_code', UnicodeAttribute()),
        ('primary_sic_code', UnicodeAttribute()),
        ('subsidiary_status', BooleanAttribute()),
    )

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
        ('username', UnicodeAttribute(hash_key=True))
        # ('active', BooleanAttribute())
        ('first_name', UnicodeAttribute())
        ('middle_name', UnicodeAttribute())
        ('last_name', UnicodeAttribute())
        ('email', UnicodeAttribute())
        ('bio', UnicodeAttribute())
        ('phone', UnicodeAttribute())
        ('street_address', UnicodeAttribute())
        ('city', UnicodeAttribute())
        ('state', UnicodeAttribute())
        ('zip_code', UnicodeAttribute())
        ('user_roles', UnicodeSetAttribute(null=True))
    )
