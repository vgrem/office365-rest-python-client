from enum import Enum


class VolumeType(Enum):
    operatingSystemVolume = "1"
    fixedDataVolume = "2"
    removableDataVolume = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VolumeType"
