from office365.booking.phonetype import PhoneType
from office365.runtime.client_value import ClientValue


class Phone(ClientValue):
    def __init__(self, language: str = None, number: str = None, region: str = None, type_: PhoneType = PhoneType.none):
        self.language = language
        self.number = number
        self.region = region
        self.type = type_

    @property
    def entity_type_name(self):
        return "microsoft.graph.Phone"
