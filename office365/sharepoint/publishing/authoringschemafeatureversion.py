from typing import Optional

from office365.runtime.client_value import ClientValue


class AuthoringSchemaFeatureVersion(ClientValue):
    Name: Optional[str] = None
    Version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AuthoringSchemaFeatureVersion"
