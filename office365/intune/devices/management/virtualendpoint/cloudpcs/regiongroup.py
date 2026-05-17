from enum import Enum


class CloudPcRegionGroup(Enum):
    default = "0"
    australia = "1"
    canada = "2"
    usCentral = "3"
    usEast = "4"
    usWest = "5"
    france = "6"
    germany = "7"
    europeUnion = "8"
    unitedKingdom = "9"
    japan = "10"
    asia = "11"
    india = "12"
    southAmerica = "13"
    euap = "14"
    usGovernment = "15"
    usGovernmentDOD = "16"
    unknownFutureValue = "20"
    norway = "17"
    switzerland = "18"
    southKorea = "19"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcRegionGroup"
