import os
import re
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class OrganizationModel(Model):
    class Meta:
        table_name = os.getenv('TABLE_ORGANIZATIONS', 'dev-organizations')
        env = os.getenv('ENVIRONMENT', 'd')

        if env == 'p':
            region = os.getenv('REGION')
            host = f'https://dynamodb.{region}.amazonaws.com'
        else:
            host = 'http://localhost:8000'

    id = UnicodeAttribute(hash_key=True)
    # active = BooleanAttribute()
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.now())
    updated_at = UTCDateTimeAttribute()

    def save(self, condition=None, conditional_operator=None, **expected_values):
        self.updated_at = datetime.now()
        super(OrganizationModel, self).save()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))

    @staticmethod
    def get_slug(name):
        """
        The slug is a URL-friendly identifier for an organization.

        Converts 'My Cool Company' into 'my-cool-company'
        """
        name = name.lower()
        name = re.sub(r'[\W_]$', '', name)
        return re.sub(r'[\W_]+', '-', name)
