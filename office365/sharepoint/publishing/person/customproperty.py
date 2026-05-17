from typing import Optional

from office365.runtime.client_value import ClientValue


class PersonCustomProperty(ClientValue):
    def __init__(self, custom_property_name: Optional[str] = None):
        self.CustomPropertyName = custom_property_name

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonCustomProperty"
