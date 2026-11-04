from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AuthoringSchemaFeatureVersion(ClientValue):
    Name: Optional[str] = None
    Version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AuthoringSchemaFeatureVersion"
