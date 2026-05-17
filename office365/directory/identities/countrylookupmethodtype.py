from enum import Enum


class CountryLookupMethodType(Enum):
    clientIpAddress = "0"
    authenticatorAppGps = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CountryLookupMethodType"
