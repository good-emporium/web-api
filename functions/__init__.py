import os
import re
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
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

    id = UnicodeAttribute(hash_key=True)
    # active = BooleanAttribute()
    name = UnicodeAttribute()
    description = UnicodeAttribute()

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

    username = UnicodeAttribute(hash_key=True)
    # active = BooleanAttribute()
    display_name = UnicodeAttribute()
    email = UnicodeAttribute()
    bio = UnicodeAttribute()
