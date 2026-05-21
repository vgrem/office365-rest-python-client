from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PropertyValue(ClientValue):
    TermId: Optional[str] = None
    Value: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PropertyValue"
