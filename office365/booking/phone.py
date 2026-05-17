from typing import Optional

from office365.booking.phonetype import PhoneType
from office365.runtime.client_value import ClientValue


class Phone(ClientValue):
    def __init__(
        self,
        language: Optional[str] = None,
        number: Optional[str] = None,
        region: Optional[str] = None,
        type_: Optional[PhoneType] = None,
    ):
        self.language = language
        self.number = number
        self.region = region
        self.type = type_

    @property
    def entity_type_name(self):
        return "microsoft.graph.Phone"
