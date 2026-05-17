from typing import Optional

from office365.runtime.client_value import ClientValue


class Icon(ClientValue):
    def __init__(self, color: Optional[str] = None, name: Optional[str] = None):
        self.Color = color
        self.Name = name

    @property
    def entity_type_name(self):
        return "SP.Publishing.Icon"
