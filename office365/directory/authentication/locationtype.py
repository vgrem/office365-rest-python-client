from enum import Enum


class LocationType(Enum):
    default = "0"
    conferenceRoom = "1"
    homeAddress = "2"
    businessAddress = "3"
    geoCoordinates = "4"
    streetAddress = "5"
    hotel = "6"
    restaurant = "7"
    localBusiness = "8"
    postalAddress = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.LocationType"
