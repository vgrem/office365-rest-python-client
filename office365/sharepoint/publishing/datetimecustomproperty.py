from typing import Optional

from office365.runtime.client_value import ClientValue


class DateTimeCustomProperty(ClientValue):
    CustomPropertyName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.DateTimeCustomProperty"
