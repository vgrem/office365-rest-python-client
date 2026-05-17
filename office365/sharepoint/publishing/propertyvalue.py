from typing import Optional

from office365.runtime.client_value import ClientValue


class PropertyValue(ClientValue):
    def __init__(self, term_id: Optional[str] = None, value: Optional[str] = None):
        self.TermId = term_id
        self.Value = value

    @property
    def entity_type_name(self):
        return "SP.Publishing.PropertyValue"
