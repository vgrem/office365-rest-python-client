from enum import Enum


class LocationUniqueIdType(Enum):
    unknown = "0"
    locationStore = "1"
    directory = "2"
    private = "3"
    bing = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.LocationUniqueIdType"
