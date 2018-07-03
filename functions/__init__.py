import os
import re
from datetime import datetime

from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class OrganizationModel(Model):
    class Meta:
        table_name = os.getenv('TABLE_ORGANIZATIONS')

        env = os.getenv('ENVIRONMENT', 'd')
        if env == 'p':
            region = os.getenv('REGION')
            host = f'https://dynamodb.{region}.amazonaws.com'
        else:
            host = 'http://localhost:8000'

    id = UnicodeAttribute(hash_key=True)
    active = BooleanAttribute()
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    createdAt = UTCDateTimeAttribute(default=datetime.now())
    updatedAt = UTCDateTimeAttribute()

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(OrganizationModel, self).save()

    @staticmethod
    def get_slug(name):
        """
        The slug is a URL-friendly identifier for an organization.

        Converts 'My Cool Company' into 'my-cool-company'
        """
        name = name.lower()
        return re.sub(r'[\W_]+', '-', name)
