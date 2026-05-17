from enum import Enum


class AuthenticationPhoneType(Enum):
    mobile = "0"
    alternateMobile = "1"
    office = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationPhoneType"
