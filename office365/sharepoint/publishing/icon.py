from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class Icon(ClientValue):
    Color: Optional[str] = None
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.Icon"
